#!/usr/bin/env python
'''
Current Notes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
- add a big O tester for the marking of the image to get it to run the fastest
- file extentions specific to the program
'''
import argparse
import os
import time
import sys
import urllib.request
from datetime import datetime, timedelta
import cv2
from dateutil import parser as dateparser
import tkinter
from tkinter import filedialog
from tkinter import *
import datetime
from mapping.fileio import get_dates_link, get_dates_file
from mapping.QDguiColor import AppColor
from mapping.QDgui import App
from mapping.config import Config

import numpy as np

import warnings
import multiprocessing as mp

def get_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--verbose", action="store_true", dest='verbose',
                    help="prints detailed status information")
    ap.add_argument("--config",
                    help="path to config file",
                    default="config.json")
    
    ap.add_argument("--blank", action="store_true", help="don't draw suggestions")
    ap.add_argument('--load', help="an old thematic map to load and draw on")
    ap.add_argument('--color', action='store_true', help='using a color image')
    return ap.parse_args()


if __name__ == "__main__":
    warnings.filterwarnings("ignore")
    t0 = time.time()

    args = get_args()
    config = Config(args.config)
    print(args)
    if args.verbose:
        print("Launching trainer")
    
    if args.verbose:
        date = datetime.datetime.today().strftime('%Y-%m-%d')
        print("Running for {}".format(date))

    if args.load and args.blank:
        raise RuntimeError("Cannot specify both an old file to draw on and blank")
    
    if args.color:
        print('The program runs slower with 3 color images, do not include --color if you wish to proceed with a black and white image')

   #this needs to be fixed
    if args.load is not None:
        print("choose the unmarked image first")
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()
        #data = {'QD': cv2.imread(filepath, 0)}
        print('now choose the marked map')
        root = tkinter.Tk()
        root.withdraw()
        filepath = filedialog.askopenfilename()
        old_thmap = {'QD': cv2.imread(filepath, 0)}
        App(data, out_file_name, args.config, relabel=old_thmap).mainloop()
    else:
        if args.color:
            root = tkinter.Tk()
            root.withdraw()
            filepath = filedialog.askopenfilename()
            data = {'QD': cv2.imread(filepath)[:4085,:]}
            out_file_name = 'QDmap.'
            AppColor(data, out_file_name, args.config).mainloop()
        else:
            root = tkinter.Tk()
            root.withdraw()
            filepath = filedialog.askopenfilename()
            print('You are using a black and white image, if you would like to use a color image include --color in the command line.')
            #print(cv2.imread(filepath).shape, cv2.imread(filepath, 0).shape) #------ ((image, 3 channels), (image, 1 channel)) color vs black and white
            data = cv2.imread(filepath, 0)[:4085,:]
            out_file_name = 'QDmap.'
            App(data, out_file_name, args.config).mainloop()
    # Load data and organize input
    #f = Fetcher(date, products=config.products, verbose=args.verbose)
    #results = f.fetch()

    #daa, headers = dict(), dict()
    #for product in results:
    #    head, d  results[product]
    #    data[config.products_map[product]] = d
    #    headers[config.products_map[product]] = head
    #data = {'c94': cv2.imread('180910 FULL_001.tif', 0)[0:1280, 0:1280], 'c131': cv2.imread('180910 FULL_001.tif', 0)[0:1280, 0:1280], 'c171': cv2.imread('180910 FULL_001.tif', 0)[0:1280, 0:1280],
    #       'c195': cv2.imread('180910 FULL_001.tif', 0)[0:1280, 0:1280], 'c284': cv2.imread('180910 FULL_001.tif', 0)[0:1280, 0:1280], 
    #       'c304': cv2.imread('180910 FULL_001.tif', 0)[0:1280, 0:1280], 'halpha': cv2.imread('180910 FULL_001.tif', 0)[0:1280, 0:1280]}
    # the output filenames are structured as the "thmap_[date of observation]_[date of labeling].fits"
    #"thmap_{}_{}.fits".format(date.strftime("%Y%m%d%H%M%S"),datetime.utcnow().strftime("%Y%m%d%H%M%S"))

    if args.verbose:
        print('best of luck!!')
        #print("Training took {:.1f} minutes".format((time.time() - t0)/60.0))
