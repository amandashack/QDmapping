import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import time
import sys
import os

x = [1024, 2048, 4096]
y = list()
for i in range(len(x)):
    start = time.time()
    os.system(sys.argv[1] + " " + str(x[i]))
    y.append(time.time()-start)

gra = np.average(np.exp(np.diff(np.log(y))) - 1)
#print(y, np.exp(np.diff(np.log(y)))-1)
if gra <= 0:
    print('O(1)')
elif gra > 0 and gra < .5:
    print('O(log n)')
elif gra >.5 and gra <= 1:
    print('O(n)')
elif gra > 1 and gra <= 1.5:
    print('O(n log n)')
elif gra > 1.5 and gra <= 3:
    print('O(n^2)')
else:
    print('O(n^3)')

    
    """x = [1024, 2048, 4096]
start = time.time()
#call((sys.argv[1], "2048"))
os.system(sys.argv[1] + " 2048")
#timeit.Timer(lambda : call(sys.argv[1], 1024)).timeit()
call((j, i) for j in sys.argv for i in x)
print(time.time()-start)


#print(timeit(timeit.Timer(lamba : call("cs23_as10_linear", 1024))))
#x = array([1024, 2048, 4096])
"""