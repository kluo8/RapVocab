#!/usr/bin/env python

import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

mpl.use('agg')
'''
Created on Mar 22, 2017

@author: arno
'''

SONG_VECTORS_FILE = "../wordcount/output/song_vectors_pyclustering.txt"



def gatherSongsDiversity():
    
    data = []
    
    for line in open(SONG_VECTORS_FILE):
        line = line.rstrip('\n').split()
        if float(line[1]) == 0 or float(line[0]) == 0:
            continue
        data.append(float(line[1])/float(line[0]))
    return data



if __name__ == '__main__':
    data = gatherSongsDiversity()
    dMean = np.average(data)
    stdDev = np.std(data)
    
    print(dMean, stdDev)
    
    fig, ax = plt.subplots()
    
    # Create the boxplot
    bp = ax.boxplot(data)
    whiskers = sorted(list(bp["whiskers"][0].get_ydata()) + list(bp["whiskers"][1].get_ydata()))
    
    print(whiskers)
    fig.savefig('fig1.png', bbox_inches='tight')