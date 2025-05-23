import numpy as np
import csv
import os
from datetime import datetime
from collections import Counter
import matplotlib.pyplot as plt

# LaTeX font
def latex_font(): 
    plt.rc('text', usetex=True)
    plt.rc('font', family='serif', size=12)

def latex_font1(): 
    plt.rcParams.update({
        'text.usetex': True,
        'font.family': 'serif',
        'font.size': 12
    })
latex_font()


xlims = [0,10]
x = np.linspace(*xlims,1000)
y = np.sin(x)
plt.plot(x,y)
plt.xlabel('$x$')
plt.ylabel('$y$', size = 15)
plt.title(r'\textbf{Graph of the motherfucking gate is what it is}')
plt.xlim(*xlims)
plt.xticks(np.arange(0,10+1,1))
plt.grid()
plt.show()