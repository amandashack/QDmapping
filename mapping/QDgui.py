import tkinter as tk
# from tkinter import *  # bad idea... but I did it
from tkinter import messagebox, ttk, Frame, Scrollbar, Canvas, LEFT, VERTICAL, RIGHT, FALSE, TRUE, BOTH, NW, Toplevel, Y
from tkinter import filedialog
from tkinter import *
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib import path
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
from matplotlib.widgets import LassoSelector
from matplotlib.patches import Polygon
from matplotlib.collections import PatchCollection
import itertools

from skimage import draw
from skimage.morphology import binary_erosion

from sunpy import sun, time

from mapping.fileio import Outgest
from mapping.config import Config

import numpy as np
import time
import scipy.ndimage

# inter-dot distance and assign to the label
# average grain diameter - area histogram, longest and shortest diameter to get a shape
# geometry of the grain
# correlation between defects and grain shape
# define vector get in plane rotations
# real space distance or fft


class VerticalScrolledFrame(Frame):
    """
    A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


class CustomToolbar(NavigationToolbar2TkAgg):
    """
    A custom Matplotlib toolbar that allows for a lasso selection when no tool is selected
    """
    def __init__(self, canvas_, parent_, edit_frame, app):
        self.parent_frame = parent_
        self.edit_frame = edit_frame
        self.toolitems = (
            ('Home', "Reset zoom", 'home', 'home'),
            ('Back', 'Undo one zoom step', 'back', 'back'),
            ('Forward', 'Redo one zoom step', 'forward', 'forward'),
            (None, None, None, None),
            (None, None, None, None),
            (None, None, None, None),
            ('Pan', 'Activate pan', 'move', 'pan'),
            ('Zoom', 'Activate zoom', 'zoom_to_rect', 'zoom'),
            # ("Lasso", "Activate lasso", "hand", "lasso")
        )
        self.app = app
        NavigationToolbar2TkAgg.__init__(self, canvas_, parent_)

    def pan(self):
        NavigationToolbar2TkAgg.pan(self)
        if self._active:
            self.edit_frame.config(background='white', text='Pan')
        else:
            self.edit_frame.config(background='red', text='Draw')
            self.app.change_class()

    def zoom(self):
        NavigationToolbar2TkAgg.zoom(self)
        if self._active:
            self.edit_frame.config(background='white', text='Zoom')
        else:
            self.edit_frame.config(background='red', text='Draw')
            self.app.change_class()


class App(tk.Tk):
    """
    The main gui app for the annotating solar images,
    supports two regions: one for data preview and one for the thematic map
    """

    def __init__(self, data, output, config_path, blank=True, relabel=None, resizable=True):
        """
        initialize the gui object
        :param data: channel data for solar images
        :type data: a dictionary of (m,n) numpy arrays, keyed by the product name
        :param output: the directory the resulting thematic map is saved
        :type output: string
        :param headers: all headers associated with data
        :type headers: a dictionary of FITS headers, keyed by product name, should match data
        :param config_path: the path to the configuration json file
        :type config_path: string
        :param blank: if true, will not draw suggestion thematic map with limb, quiet sun, and outer space
        :type blank: bool
        :param relabel: if valued, will use that as the input thematic map to relabel
        :type relabel: None or (m,n) numpy array
        :param resizable: if true, the gui is resizable
        :type resizable: bool
        """
        self.config_path = config_path
        self.config = Config(config_path)
        self.history = []  # the history of regions drawn for undo feature, just a list of (m,n) thematic maps
        #self.header = headers[self.config.products_map[self.config.default['header']]]  # get the reference header
        #self.headers = headers  # store headers for later outgest in thematic map
        self.blank = blank
        self.relabel = relabel

        self.region_patches = []  # a list of drawn contours around selected thematic map regions

        tk.Tk.__init__(self)
        #self.single_color_theme = 'yellow'  # color used for the single color menus
        self.real_theme = 'yellow'
        self.canvas_size = (10, 5)  # size of the canvas frame (in inches)
        self.subplot_grid_spec = {'wspace': 0, 'hspace': 0, 'left': 0, 'bottom': 0, 'right': 1,
                                  'top': 1}  # spacing of subplots in canvas
        self.output = output  # where to save the trained fits image
        self.shape = (data.shape[0], data.shape[1])
        #self.data = data
        self.image = data
        self.title("The QD Mapping Utility")
        self.geometry("1200x800")
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.resizable(resizable, resizable)
        self.make_gui()  # set up all the gui canvases
        # if no default is requested, blank the thematic map, otherwise draw suggested
        if blank:
            self.selection_array[:, :] = self.config.QD_class_index['unlabeled']
        else:  # make default
            self.draw_default()
            self.fig.canvas.draw()

        if self.relabel:  # use a previously drawn map
            self.selection_array = self.relabel

    def interpret_header(self):
        """
        Read pertinent information from the image headers,
         especially location and radius of the Sun to calculate the default thematic map
        :return: setes self.date, self.cy, self.cx, and self.sun_radius_pixel
        """
        # handle special cases since date-obs field changed names
        if 'DATE_OBS' in self.header:
            self.date = self.header['DATE_OBS']
        elif 'DATE-OBS' in self.header:
            self.date = self.header['DATE-OBS']
        else:
            raise Exception("Image does not have a DATE_OBS or DATE-OBS field")

        self.cy, self.cx = self.header['CRPIX1'], self.header['CRPIX2']
        sun_radius_angular = sun.solar_semidiameter_angular_size(t=time.parse_time(self.date)).arcsec
        arcsec_per_pixel = self.header['CDELT1']
        self.sun_radius_pixel = (sun_radius_angular / arcsec_per_pixel)

    def save(self):
        print("Save the mapped image first as .csv and put it in \'maps\' folder. Name e.g. DD/MM/YY_2PbSe_PbI2_map.csv")
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.asksaveasfilename()
        np.savetxt(filepath, self.selection_array, delimiter = ',')
        print('Now save the statistics file as .csv into the same folder. Name e.g. DD/MM/YY_2PbSe_PbI2_stat.csv')
        root = tk.Tk()
        root.withdraw()
        filepath = filedialog.asksaveasfilename()
        f = open(filepath, 'w')

        # need to fix formatting here
        a = []
        for i in range(len(self.config.QD_class_index.keys())):
            a.append((self.selection_array == i).sum())
        for i in range(len(list(self.config.QD_class_index.keys()))):
            f.write('percent ' + list(self.config.QD_class_index.keys())[i] 
                    + ' = ' +  str((a[i]/(self.shape[0]*self.shape[1]))*100))
            print('percent ' + list(self.config.QD_class_index.keys())[i] 
                    + ' = ' +  str((a[i]/(self.shape[0]*self.shape[1]))*100))
        f.close()
        #out = Outgest(self.output, self.selection_array.astype('uint8'), self.config_path)
        #out.save()
        #out.upload()

    def on_exit(self):
        """When you click to exit, this function is called, prompts whether to save"""
        answer = messagebox.askyesnocancel("Exit", "Do you want to save as you quit the application?")
        if answer:
            self.save()
            self.quit()
            self.destroy()
        elif answer is None:
            pass # the cancel action
        else:
            self.quit()
            self.destroy()

    def make_topmost(self):
        """ Makes this window the topmost window """
        self.lift()
        self.attributes("-topmost", 1)

    def make_gui(self):
        """  Setups the general structure of the gui, the first function called """
        #print(self.config.QD_classes, self.config.QD_class_index)
        self.option_window = Toplevel()
        self.option_window.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.canvas_frame = tk.Frame(self, height=500)
        self.option_frame = tk.Frame(self.option_window, height=300)
        self.canvas_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.option_frame.pack(side=tk.RIGHT, fill=None, expand=False)
        self.make_options_frame()
        self.make_canvas_frame()
        #self.disable_reciprocal()
    
    def configure_image(self):
    #def configure_threecolor_image(self):
        """ 
        configures the three color image according to the requested parameters 
        :return: nothing, just updates self.image
        """
        self.editim = self.image #### this may be source of error
        edit_options = ['erode/dil',  'open/close', 'blackhat/tophat']
        for editor in edit_options:
            self.editim = cv2.morphologyEx(self.editim, getattr(cv2, 'MORPH_ERODE'), 
                                      cv2.getStructuringElement(getattr(cv2, 'MORPH_ELLIPSE'),
                                      (self.editorop[editor].get()-10,self.editorop[editor].get()-10)), 
                                      iterations=self.editoriter[editor].get())
            self.editim = cv2.morphologyEx(self.editim, getattr(cv2, 'MORPH_TOPHAT'), 
                                      cv2.getStructuringElement(getattr(cv2, 'MORPH_ELLIPSE'), 
                                      (self.editorop[editor].get()-10,self.editorop[editor].get()-10)), 
                                      iterations=self.editoriter[editor].get())
            self.editim = cv2.morphologyEx(self.editim, getattr(cv2, 'MORPH_OPEN'), 
                                      cv2.getStructuringElement(getattr(cv2, 'MORPH_ELLIPSE'), 
                                      (self.editorop[editor].get()-10,self.editorop[editor].get()-10)), 
                                      iterations=self.editoriter[editor].get())
        self.image = self.editim
        '''#order = {'red': 0, 'green': 1, 'blue': 2}
        #self.image = np.zeros((self.shape[0], self.shape[1], 3))
        #for color, var in self.multicolorvars.items():
        ############### this kind of thing will need to be done if you want to create the dropdown menu
        #    channel = var.get()  # determine which channel should be plotted as this color
            #self.image[:, :, order[color]] = self.data[channel]

            # scale the image by the power
            #self.image[:, :, order[color]] = np.power(self.image[:, :, order[color]],
                                                      self.multicolorpower[color].get())

            # adjust the percentile thresholds
            #lower = np.nanpercentile(self.image[:, :, order[color]], self.multicolormin[color].get())
            #upper = np.nanpercentile(self.image[:, :, order[color]], self.multicolormax[color].get())
            #self.image[np.where(self.image[:, :, order[color]] < lower)] = lower
            #self.image[np.where(self.image[:, :, order[color]] > upper)] = upper

        # image values must be between (0,1) so scale image
        #for color, index in order.items():
        #    self.image[:, :, index] /= np.nanmax(self.image[:, :, index])'''

    '''#def configure_reciprocal_image(self, scale=False):
        """
        configures the single color image according to the requested parameters
        :return: nothing, just updates self.image
        """
        
        configures the reciprocal image. First you need to blur it, 
        find the centers of mass, select your region, and then
        let it go into reciprocal space.
        Once it is there it will at first measure the angles and distances
        for you and print it out on the screen

        
        #self.image=data
        # determine which channel to use
        #self.image = self.data[self.singlecolorvar.get()]

        # scale the image by requested power
        #self.image = np.power(self.image, self.singlecolorpower.get())
        # adjust the percentile thresholds
        #lower = np.nanpercentile(self.image, self.singlecolormin.get())
        #upper = np.nanpercentile(self.image, self.singlecolormax.get())
        #self.image[self.image < lower] = lowe
        #self.image[self.image > upper] = upper

        # image values must be between (0,1) so scale image
        #self.image /= np.nanmax(self.image)'''

    def updateArray(self, array, indices, value):
        """
        updates array so that pixels at indices take on value
        :param array: (m,n) array to adjust
        :param indices: flattened image indices to change value
        :param value: new value to assign
        :return: the changed (m,n) array
        """
        lin = np.arange(array.size)
        new_array = array.flatten()
        new_array[lin[indices]] = value
        np.set_printoptions(threshold=np.nan)
        #print(np.asarray(new_array.reshape(array.shape))[0:50, 0:50])
        return new_array.reshape(array.shape)

    def onlasso(self, verts):
        """
        Main function to control the action of the lasso, allows user to draw on data image and adjust thematic map
        :param verts: the vertices selected by the lasso
        :return: nothin, but update the selection array so lassoed region now has the selected theme, redraws canvas
        """
        p = path.Path(verts)
        ind = p.contains_points(self.pix, radius=1)
        self.history.append(self.selection_array.copy())
        self.selection_array = self.updateArray(self.selection_array,
                                                ind,
                                                self.QD_class_var.get())
        np.set_printoptions(threshold=np.nan)
        #print(np.asarray(verts), np.asssarray(verts).shape, np.asarray(p), np.asarray(p).shape)
        self.mask.set_data(self.selection_array)
        self.fig.canvas.draw_idle()

    def make_canvas_frame(self):
        """ Create the data and thematic map images for the first time """
        b = time.time()
        self.fig, (self.imageax, self.previewax) = plt.subplots(ncols=2,
                                                                figsize=self.canvas_size,
                                                                sharex=True, sharey=True,
                                                                gridspec_kw=self.subplot_grid_spec)
        print(time.time() - b)
    
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.canvas_frame)
        self.canvas.mpl_connect('button_press_event', self.onclick)
        self.canvas.mpl_connect('key_press_event', self.onpress)
        # set up the channel data view
        b = time.time()
        #self.configure_threecolor_image()
        self.configure_image()
        print(time.time()-b)
        self.imageplot = self.imageax.imshow(self.image)
        self.imageax.set_xlim([0, self.shape[1]])
        self.imageax.set_ylim([0, self.shape[0]])
        # self.imageax.set_aspect("equal")
        self.imageax.set_axis_off()

        # set up the thematic map view
        self.selection_array = np.zeros(self.shape, dtype=np.uint8)
        if self.blank:
            self.selection_array += self.config.QD_class_index['unlabeled']
        else:
            self.draw_default()
        self.history.append(self.selection_array)
        colortable = [self.config.QD_colors[self.config.QD_class_name[i]]
                      for i in range(len(self.config.QD_classes))]
        cmap = matplotlib.colors.ListedColormap(colortable)
        self.mask = self.previewax.imshow(self.selection_array,
                                          origin='lower',
                                          interpolation='nearest',
                                          cmap=cmap,
                                          vmin=-1, vmax=len(colortable))
        self.previewax.set_xlim([0, self.shape[1]])
        self.previewax.set_ylim([0, self.shape[0]])
        self.previewax.set_aspect("equal")
        self.previewax.set_axis_off()

        # add selection layer for lasso
        #self.pix = np.arange(self.shape[0])  # assumes square image
        #xv, yv = np.meshgrid(self.pix, self.pix)
        self.pix = np.asarray(list(list(reversed(list(elem))) for elem in 
            itertools.product(list(range(self.shape[0])), list(range(self.shape[1])))))

        lineprops = dict(color=self.config.default['lasso_color'],
                         linewidth=self.config.default['lasso_width'])
        self.lasso = LassoSelector(self.imageax, self.onlasso, lineprops=lineprops)

        # display everything
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # add the tool bar
        self.toolbarcenterframe = tk.LabelFrame(self.canvas_frame,
                                                borderwidth=0,
                                                text="Draw: unlabeled",
                                                relief=tk.FLAT,
                                                labelanchor=tk.N,
                                                background='red')
        toolbarframe = tk.Frame(self.toolbarcenterframe)
        toolbar = CustomToolbar(self.canvas, toolbarframe, self.toolbarcenterframe, self)
        toolbar.update()
        self.fig.canvas.toolbar.set_message = lambda x: ""  # remove state reporting
        toolbarframe.pack()
        self.toolbarcenterframe.pack(side=tk.BOTTOM, fill=tk.X)

    def onpress(self, event):
        """
        Reacts to key commands
        :param event: a keyboard event
        :return: if 'c' is pressed, clear all region patches
        """
        if event.key == 'c':
            for patch in self.region_patches:
                patch.remove()
            self.region_patches = []
            self.fig.canvas.draw_idle()
        elif event.key == "u":
            self.undobutton_action()

    def onclick(self, event):
        """
        Draw contours on the data for a click in the thematic map
        :param event: mouse click on thematic map preview
        """
        if event.inaxes == self.previewax:
            y, x = int(event.xdata), int(event.ydata)
            label = self.selection_array[x, y]
            contiguous_regions = scipy.ndimage.label(self.selection_array == label)[0]
            this_region = contiguous_regions == (contiguous_regions[x, y])

            # remove the boundaries so any region touching the edge isn't drawn odd
            this_region[0, :] = 0
            this_region[:, 0] = 0
            this_region[this_region.shape[0]-1, :] = 0
            this_region[:, this_region.shape[1]-1] = 0

            # convert the region mask into just a true/false array of its boundary pixels
            edges = binary_erosion(this_region) ^ this_region

            # convert the boundary pixels into a path, moving around instead of just where
            x, y = np.where(edges)
            coords = np.dstack([x, y])[0]
            path = [coords[0]]
            coords = coords[1:]

            while len(coords):  # and steps < 5:
                dist = np.sum(np.abs(path[-1] - coords), axis=1)

                # neighbor_index = np.where(dist == 1)[0][0]
                neighbor_index = np.argmin(dist)

                if dist[neighbor_index] < 5:
                    path.append(coords[neighbor_index].copy())
                    coords[neighbor_index:-1] = coords[neighbor_index + 1:]
                    coords = coords[:-1]
                    # not_finished = len(coords) != 0
                else:
                    break

            # path.append(path[0].copy())
            path = np.array(path)

            clips = []
            while len(coords) > 5:
                dist = np.sum(np.abs(path[-1] - coords), axis=1)
                neighbor_index = np.argmin(dist)
                clip = [coords[neighbor_index].copy()]
                coords[neighbor_index:-1] = coords[neighbor_index + 1:]
                coords = coords[:-1]
                while len(coords):
                    dist = np.sum(np.abs(clip[-1] - coords), axis=1)
                    # neighbor_index = np.where(dist == 1)[0][0]
                    neighbor_index = np.argmin(dist)
                    if dist[neighbor_index] < 5:
                        # print(coords[neighbor_index], dist[neighbor_index])
                        clip.append(coords[neighbor_index].copy())
                        coords[neighbor_index:-1] = coords[neighbor_index + 1:]
                        coords = coords[:-1]
                        # not_finished = len(coords) != 0
                    else:
                        break
                clips.append(np.array(clip))

            self.region_patches.append(PatchCollection(
                [Polygon(np.dstack([path[:, 1], path[:, 0]])[0], False,
                         fill=False, facecolor=None,
                         edgecolor="black", alpha=1, lw=2.5)] +
                [Polygon(np.dstack([clip[:, 1], clip[:, 0]])[0], False,
                         fill=False, facecolor=None,
                         edgecolor="black", alpha=1, lw=2.0) for clip in clips],
                match_original=True))
            #self.imageax.add_patch(self.region_patches[-1])
            self.imageax.add_collection(self.region_patches[-1])
            self.fig.canvas.draw_idle()

    def make_options_frame(self):
        """ make the frame that allows for configuration and classification"""
        self.tab_frame = ttk.Notebook(self.option_frame, width=800)
        self.tab_configure = tk.Frame(self.tab_frame)
        self.tab_classify = tk.Frame(self.tab_frame)
        self.make_configure_tab()
        self.make_classify_tab()

        self.tab_frame.add(self.tab_configure, text="Configure")
        self.tab_frame.add(self.tab_classify, text="Classify")
        self.tab_frame.pack(fill=tk.BOTH, expand=True)

    def real_space(self):
        """ swap from reciprocal space back to real space"""
        # disable the multicolor image --------- the reciprocal space image
        
        '''
        for color in ['red', 'green', 'blue']:
            self.multicolorscales[color].config(state=tk.DISABLED, bg='grey')
            self.multicolorframes[color].config(bg='grey')
            self.multicolorlabels[color].config(bg='grey')
            self.multicolordropdowns[color].config(bg='grey', state=tk.DISABLED)
            self.multicolorminscale[color].config(bg='grey', state=tk.DISABLED)
            self.multicolormaxscale[color].config(bg='grey', state=tk.DISABLED)

        # enable the single color
        self.realscale.config(state=tk.NORMAL, bg=self.single_color_theme) --------- self.real_theme
        self.realframe.config(bg=self.single_color_theme)
        self.reallabel.config(bg=self.single_color_theme)
        self.realdropdown.config(bg=self.single_color_theme, state=tk.NORMAL)
        self.realminscale.config(bg=self.single_color_theme, state=tk.NORMAL)
        self.singlecolormaxscale.config(bg=self.single_color_theme, state=tk.NORMAL)'''
        for editor in ['erode/dil', 'open/close', 'blackhat/tophat']:
            self.opeditorscale[editor].config(state=tk.NORMAL, bg='red')
            self.itereditorscale[editor].config(state=tk.NORMAL, bg='green')
            self.editorlabels[editor].config()

    '''def disable_real(self):
        """ swap from the single color image to the multicolor image """
        # enable the multicolor ----- the reciprocal
        for color in ['red', 'green', 'blue']:
            self.multicolorscales[color].config(state=tk.NORMAL, bg=color)
            self.multicoloframes[color].config(bg=color)
            self.multicolorlabels[color].config(bg=color)
            self.multicolordropdowns[color].config(bg=color, state=tk.NORMAL)
            self.multicolorminscale[color].config(bg=color, state=tk.NORMAL)
            self.multicolormaxscale[color].config(bg=color, state=tk.NORMAL)

        # disable the singlecolor
        self.singlecolorscale.config(state=tk.DISABLED, bg='grey')
        self.singlecolorframe.config(bg='grey')
        self.singlecolorlabel.config(bg='grey')
        self.singlecolordropdown.config(bg='grey', state=tk.DISABLED)
        self.singlecolorminscale.config(bg="grey", state=tk.DISABLED)
        self.singlecolormaxscale.config(bg="grey", state=tk.DISABLED)'''

    '''def update_button_action(self):
        """ when update button is clicked, refresh the data preview"""
        if self.mode.get() == 3:  # threecolor ---- real
            self.configure_real()
        elif self.mode.get() == 1:  # singlecolor ---- reciprocal
            self.configure_reciprocal()
        else:
            raise ValueError("mode can only be singlecolor or threecolor")

        self.imageplot.set_data(self.image)
        if self.mode.get() == 1:  # singlecolor ------ reciprocal
            self.imageplot.set_cmap('gist_gray')
        self.fig.canvas.draw_idle()'''

    def make_configure_tab(self):
        """ initial set up of configure tab"""
        # Setup the choice between single and multicolor
        modeframe = tk.Frame(self.tab_configure)
        self.mode = tk.IntVar()
        real = tk.Radiobutton(modeframe, text="no editor", variable=self.mode,
                                     value=3, command=lambda: self.real_space())
        #reciprocal = tk.Radiobutton(modeframe, text="Reciprocal", variable=self.mode,
        #                            value=1, command=lambda: self.reciprocal_space())
        self.mode.set(3)
        real.pack(side=tk.LEFT)
        #reciprocal.pack(side=tk.LEFT)

        #updatebutton = tk.Button(master=modeframe, text="Update",
        #                         command=self.update_button_action)
        #updatebutton.pack(side=tk.RIGHT)
        modeframe.grid(row=0, column=0)
        #self.setup_multicolor()
        #self.setup_singlecolor()
        self.setup_config_tab()

    def make_classify_tab(self):
        """ initial set up of classification tab"""
        self.pick_frame = tk.Frame(self.tab_classify)
        self.pick_frame2 = tk.Frame(self.tab_classify)

        self.QD_class_var = tk.IntVar()
        self.QD_class_var.set(0)  # initialize to unlabeled
        buttonnum = 0
        frame = [self.pick_frame, self.pick_frame2]
        for text, value in self.config.QD_classes:
            b = tk.Radiobutton(frame[buttonnum % 2], text=text,
                               # b = tk.Radiobutton(frame[buttonnum%2].interior, text=text,
                               variable=self.QD_class_var,
                               value=value, background=self.config.QD_colors[text],
                               indicatoron=0, width=50, height=2, command=self.change_class)
            b.pack(fill=tk.BOTH, expand=1)
            buttonnum += 1


        self.pick_frame.grid(row=0, column=0, rowspan=5, sticky=tk.W + tk.E + tk.N + tk.S)
        self.pick_frame2.grid(row=0, column=1, rowspan=5, sticky=tk.W + tk.E + tk.N + tk.S)

        undobutton = tk.Button(master=self.tab_classify, text="Undo",
                               command=self.undobutton_action)
        undobutton.grid(row=6, column=0, columnspan=2, sticky=tk.W + tk.E)

    
    ''' def setup_config_tab(self):
        """ initial setup of single color options and variables"""
        #self.singlecolorframe = tk.Frame(self.tab_configure, bg=self.single_color_theme)
        self.eframe = tk.Frame(self.tab_configure, bg=self.real_theme)
        self.oframe = tk.Frame(self.tab_configure, bg=self.real_theme)
        self.bframe = tk.Frame(self.tab_configure, bg=self.real_theme)
        edit_options = ['erode/dilate',  'open/close', 'blackhat/tophat']
        #channel_choices = sorted(list(self.data.keys()))
        #self.singlecolorlabel = tk.Label(self.singlecolorframe, text="single", bg=self.single_color_theme, width=10)
        self.erodedialabel = tk.Label(self.eframe, text = "erode/dilate", bg=self.real_theme, width=10)
        self.opencloselabel = tk.Label(self.oframe, text = "open/close", bg=self.real_theme, width=10)
        self.blackhatlabel = tk.Label(self.bframe, text = "blackhat/tophat", bg=self.real_theme, width=10)
        #self.singlecolorvar = tk.StringVar()
        ###this is for the dropdown menu self.realvar = tk.StringVar()
        #self.singlecolorpower = tk.DoubleVar()
        self.erodediaop = tk.DoubleVar()
        self.erodediaiter = tk.DoubleVar()
        #self.singlecolormin = tk.DoubleVar()
        self.opencloseop = tk.DoubleVar()
        self.opencloseiter = tk.DoubleVar()
        #self.singlecolormax = tk.DoubleVar()
        self.blackhatop = tk.DoubleVar()
        self.blackhatiter = tk.DoubleVar()
        #self.singlecolordropdown = tk.OptionMenu(self.singlecolorframe, self.singlecolorvar, *channel_choices)
        ##### the dropdown menu does not need to exist
        #self.singlecolorscale = tk.Scale(self.singlecolorframe, variable=self.singlecolorpower,
        #                                 orient=tk.HORIZONTAL, from_=self.config.ranges['single_color_power_min'],
        #                                 bg=self.single_color_theme,
        #                                 to_=self.config.ranges['single_color_power_max'],
        #                                 resolution=self.config.ranges['single_color_power_resolution'],
        #                                 length=200)
        self.erodediaopscale = tk.Scale(self.eframe, variable = self.erodediaop,
                                      orient = tk.HORIZONTAL, from_=self.config.ranges['op_size_min'],
                                      bg = self.real_theme,
                                      to_=self.config.ranges['op_size_max'],
                                      resolution= self.config.ranges['op_size_resolution'],
                                      length=200)
        self.erodediaiterscale = tk.Scale(self.eframe, variable = self.erodediaiter,
                                          orient = tk.HORIZONTAL, from_=self.config.ranges['iters_min'],
                                          bg = self.real_theme,
                                          to_=self.config.ranges['iters_max'],
                                          resolution=self.config.ranges['iters_resolution'],
                                          length = 200)                    
        #self.singlecolorminscale = tk.Scale(self.singlecolorframe, variable=self.singlecolormin,
        #                                    orient=tk.HORIZONTAL, from_=0,
        #                                    bg=self.single_color_theme,
        #                                    to_=self.config.ranges['single_color_vmin'],
        #                                    resolution=self.config.ranges['single_color_vresolution'], length=200)
        self.opencloseopscale = tk.Scale(self.oframe, variable = self.opencloseop,
                                       orient=tk.HORIZONTAL, from_=self.config.ranges['op_size_min'],
                                       bg=self.real_theme,
                                       to_=self.config.ranges['op_size_max'],
                                       length=400)
        self.opencloseiterscale = tk.Scale(self.oframe, variable = self.opencloseiter,
                                          orient = tk.HORIZONTAL, from_=self.config.ranges['iters_min'],
                                          bg = self.real_theme,
                                          to_=self.config.ranges['iters_max'],
                                          resolution=self.config.ranges['iters_resolution'],
                                          length = 200) 
        #self.singlecolormaxscale = tk.Scale(self.singlecolorframe, variable=self.singlecolormax,
        #                                    orient=tk.HORIZONTAL, from_=self.config.ranges['single_color_vmax'],
        #                                    bg=self.single_color_theme,
        #                                    to_=100, resolution=self.config.ranges['single_color_vresolution'],
        #                                    length=200)
        self.blackhatopscale = tk.Scale(self.bframe, variable = self.blackhatop,
                                       orient=tk.HORIZONTAL, from_=self.config.ranges['op_size_min'],
                                       bg=self.real_theme,
                                       to_=self.config.ranges['op_size_max'],
                                       length=400)
        self.blackhatiterscale = tk.Scale(self.bframe, variable = self.blackhatiter,
                                          orient = tk.HORIZONTAL, from_=self.config.ranges['iters_min'],
                                          bg = self.real_theme,
                                          to_=self.config.ranges['iters_max'],
                                          resolution=self.config.ranges['iters_resolution'],
                                          length = 200) 
        #self.singlecolorvar.set(self.config.products_map[self.config.default['single']])
        ##### dont need because we dont need the dropdown
        #self.singlecolorpower.set(self.config.default['single_power'])
        ########### add/change if you want a certain editor to start with a certain value
        #self.singlecolormin.set(0)
        self.erodediaop.set(0)
        #self.singlecolormax.set(100)
        self.opencloseop.set(0)
        self.blackhatop.set(0)
        self.erodediaiter.set(0)
        self.opencloseiter.set(0)
        self.blackhatiter.set(0)
        #self.singlecolordropdown.config(bg=self.single_color_theme, width=10)
        #self.singlecolorlabel.pack(side=tk.LEFT)
        self.erodedialabel.pack(side=tk.LEFT)
        self.erodediaopscale.pack(side=tk.RIGHT)
        self.erodediaiterscale.pack(side=tk.RIGHT)
        self.eframe.grid(row=1,columnspan=3, rowspan=1)

        self.opencloselabel.pack(side=tk.LEFT)
        self.opencloseopscale.pack(side=tk.RIGHT)
        self.opencloseiterscale.pack(self=tk.RIGHT)
        self.oframe.grid(row=2,columnspan=2,rowspan=1)

        self.blackhatlabel.pack(side=tk.LEFT)
        self.blackhatoplabel.pack(side=tk.RIGHT)
        self.blackhatiterscale.pack(side=tk.RIGHT)
        self.bframe.grid(row=3,columnspan=2,rowspan=1)
        
        
        #self.singlecolorscale.pack(side=tk.RIGHT)
        #self.singlecolormaxscale.pack(side=tk.RIGHT)
        #self.singlecolorminscale.pack(side=tk.RIGHT)
        
        #self.singlecolordropdown.pack()
        #self.singlecolorframe.grid(row=4, columnspan=5, rowspan=1)'''

    def setup_config_tab(self):
    ###def setup_multicolor(self):
        ####""" initial setup of multicolor options and variables"""
        # initial setup of reciprocal image
        #### Setup the options for multicolor
        #setup options for reciprocal - will have the same options as real (constrast and such)
        #multicolormasterframe = tk.Frame(self.tab_configure)
        realspacemasterframe = tk.Frame(self.tab_configure)
        #channel_choices = sorted(list(self.data.keys())) 
        edit_options = ['erode/dil',  'open/close', 'blackhat/tophat']
        #rgb = ['red', 'green', 'blue']
        self.editorframe = {editor: tk.Frame(realspacemasterframe) for editor in edit_options}
        #self.multicolorlabels = {color: tk.Label(self.multicolorframes[color], text=color, bg=color, width=10) for color in rgb}
        self.editorlabels = {editor: tk.Label(self.editorframe[editor], width=10) for editor in edit_options}
        #self.multicolorvars = {color: tk.StringVar() for color in rgb}
        self.editorvars = {editor: tk.StringVar() for editor in edit_options}
        self.editorop = {editor: tk.IntVar() for editor in edit_options}
        self.editoriter = {editor: tk.IntVar() for editor in edit_options}
        #self.multicolorpower = {color: tk.DoubleVar() for color in rgb}
        ##### dont need - self.editorpower = {editor: tk.DoubleVar() for editor in edit_options}
        #self.multicolormin = {color: tk.DoubleVar() for color in rgb}

        #self.multicolordropdowns = {color: tk.OptionMenu(self.multicolorframes[color],
        #                                                 self.multicolorvars[color],
        #                                                 *channel_choices) for color in rgb}
        ###### do not need the dropdown menu

        #self.multicolorscales = {color: tk.Scale(self.multicolorframes[color],
        #                                         variable=self.multicolorpower[color],
        #                                         orient=tk.HORIZONTAL,
        #                                         from_=self.config.ranges['multi_color_power_min'],
        #                                         to_=self.config.ranges['multi_color_power_max'], bg=color,
        #                                         resolution=self.config.ranges['multi_color_power_resolution'],
        #                                         length=200) for color in rgb}
        self.opeditorscale = {editor: tk.Scale(self.editorframe[editor],
                                              variable = self.editorop[editor],
                                              orient=tk.HORIZONTAL,
                                              from_=self.config.ranges['op_size_min'],
                                              to_=self.config.ranges['op_size_max'],
                                              bg=self.real_theme, resolution = self.config.ranges['op_size_resolution'],
                                              length = 400) for editor in edit_options}
        self.itereditorscale = {editor: tk.Scale(self.editorframe[editor],
                                                variable = self.editoriter[editor],
                                                orient=tk.HORIZONTAL,
                                                from_=self.config.ranges['iters_min'],
                                                bg = self.real_theme,
                                                to_=self.config.ranges['iters_max'],
                                                resolution = self.config.ranges['iters_resolution'],
                                                length = 200) for editor in edit_options}
        #self.multicolorminscale = {color: tk.Scale(self.multicolorframes[color],
        #                                          variable=self.multicolormin[color],
        #                                           orient=tk.HORIZONTAL, from_=0,
        #                                           to_=self.config.ranges['multi_color_vmin'], bg=color,
        #                                           resolution=self.config.ranges['multi_color_vresolution'],
        #                                           length=200) for color in rgb}
        #self.iterseditorscale = {editor: tk.Scale(self.editorframes[editor],
        #                                      variable = self.editorpower[editor]
        #                                      orient=tk.HORIZONTAL,
        #                                      from_=self.config.ranges['op_size_power_min'],
        #                                      to_=self.config.ranges['op_size_power_max'],
        #                                      bg=editor, resolution = self.config.ranges['op_size_power_resolution'],
        #                                      length = 200) for editor in edit_options}
        #self.multicolormaxscale = {color: tk.Scale(self.multicolorframes[color],
        #                                           variable=self.multicolormax[color],
        #                                           orient=tk.HORIZONTAL, from_=self.config.ranges['multi_color_vmax'],
        #                                           to_=100, bg=color,
        #                                           resolution=self.config.ranges['multi_color_vresolution'],
        #                                           length=200) for color in rgb}

        #for color in rgb:
        for editor in edit_options:
            #self.multicolorvars[color].set(self.config.products_map[self.config.default[color]])
            #self.editorvars[editor].set(self.products_map[self.config.default[editor]])
            ######## will add if want to add dropdown menu
            #self.multicolorpower[color].set(self.config.default[color + "_power"])
            ######## set to 0 for now, might want to add enable/disable here if setting them to 0 is not good
            #self.multicolormin[color].set(0)
            self.editorop[editor].set(15)
            #self.multicolormax[color].set(100)
            self.editoriter[editor].set(2)
            #self.multicolordropdowns[color].config(bg=color, width=10)
            #self.multicolorlabels[color].pack(side=tk.LEFT)
            self.editorlabels[editor].pack(side=tk.LEFT)
            #self.multicolorscales[color].pack(side=tk.RIGHT)
            self.opeditorscale[editor].pack(side=tk.RIGHT)
            #self.multicolormaxscale[color].pack(side=tk.RIGHT)
            self.itereditorscale[editor].pack(side=tk.RIGHT)
            #self.multicolorminscale[color].pack(side=tk.RIGHT)
            #self.multicolordropdowns[color].pack()
            #self.multicolorframes[color].pack(fill=tk.BOTH)
            self.editorframe[editor].pack(fill=tk.BOTH)
        #multicolormasterframe.grid(row=1, column=0, columnspan=5, rowspan=3)
        realspacemasterframe.grid(row=1, column=0, columnspan=3, rowspan=3)

    def undobutton_action(self):
        """ when undo is clicked, revert the thematic map to the previous state"""
        if len(self.history) > 1:
            old = self.history.pop(-1)
            self.selection_array = old
            self.mask.set_data(old)
            self.fig.canvas.draw_idle()

    def change_class(self):
        """ "on changing the classification label, update the "draw" text """
        self.toolbarcenterframe.config(text="Draw: {}".format(self.config.QD_class_name[self.QD_class_var.get()]))
    '''
    def draw_circle(self, center, radius, array, value, mode="set"):
        """
        Draws a circle of specified radius on the input array and fills it with specified value
        :param center: a tuple for the center of the circle
        :type center: tuple (x,y)
        :param radius: how many pixels in radius the circle is
        :type radius: int
        :param array: image to draw circle on
        :type array: size (m,n) numpy array
        :param value: what value to fill the circle with
        :type value: float
        :param mode: if "set" will assign the circle interior value, if "add" will add the value to the circle interior,
            throws exception otherwise
        :type mode: string, either "set" or "add"
        :return: updates input array
        """
        ri, ci = draw.circle(center[0], center[1],
                             radius=radius,
                             shape=array.shape)
        if mode == "add":
            array[ri, ci] += value
        elif mode == "set":
            array[ri, ci] = value
        else:
            raise ValueError("draw_circle mode must be 'set' or 'add' but {} used".format(mode))
        return ri, ci, array[ri,ci]'''
    '''
    def draw_annulus(self, center, inner_radius, outer_radius, array, value, mode="set"):
        """
        Draws an annulus of specified radius on the input array and fills it with specified value
        :param center: a tuple for the center of the annulus
        :type center: tuple (x,y)
        :param inner_radius: how many pixels in radius the interior empty circle is, where the annulus begins
        :type inner_radius: int
        :param outer_radius: how many pixels in radius the larger outer circle is, where the annulus ends
        :typde outer_radius: int
        :param array: image to draw annulus on
        :type array: size (m,n) numpy array
        :param value: what value to fill the annulus with
        :type value: float
        :param mode: if "set" will assign the circle interior value, if "add" will add the value to the circle interior,
            throws exception otherwise
        :type mode: string, either "set" or "add"
        :return: updates input array and then returns it with the annulus coordinates as a tuple
        """
        if mode == "add":
            self.draw_circle(center, outer_radius, array, value)
            self.draw_circle(center, inner_radius, array, -value)
        elif mode == "set":
            ri, ci, existing = self.draw_circle(center, inner_radius, array, -value)
            self.draw_circle(center, outer_radius, array, value)
            array[ri, ci] = existing
        else:
            raise ValueError("draw_annulus mode must be 'set' or 'add' but {} used".format(mode))'''

    def draw_default(self, inside=5, outside=15):
        """
        Draw suggested sun disk, limb, and empty background
        :param inside: how many pixels from the calculated solar disk edge to go inward for the limb
        :param outside: how many pixels from the calculated solar disk edge to go outward for the limb
        :return: updates the self.selection_array
        """
        # fill everything with empty outer space
        self.selection_array[:, :] = self.config.QD_class_index['unlabeled']

