#!/usr/bin/env python

import operator
import matplotlib.pyplot as plt
import math
import numpy as np

'''
Created on Mar 25, 2017

@author: arno
'''

COLORS = ['b', 'c', 'y', 'm', '#AF7FB5', '#4F6D27', '#D0A94C', '#794044', '#871606']

def plotMetadata(data, desiredMetadata, title, yaxis):
    
    fig, ax = plt.subplots()
    
    dataToPlot = {}
    for artist, metadata in data.items():
        dataToPlot[artist] = metadata[desiredMetadata]
        
    sortedtoplot = sorted(dataToPlot.items(), key=operator.itemgetter(1), reverse=True)

    print(sortedtoplot)
    ind = np.arange(len(sortedtoplot))
    width = 0.20
    margin = 0.5
    
    bars = ax.bar(margin + ind, list(map(lambda x: int(x[1]), sortedtoplot)), width, color='b')

    # add some text for labels, title and axes ticks
    ax.set_ylabel(yaxis)
    ax.set_xlabel('Rappers')
    ax.set_title(title)
    ax.set_xticks(margin + ind + width/2)
    ax.set_xticklabels(list(map(lambda x: x[0], sortedtoplot)))

    for rect in bars:
        height = rect.get_height()
        ax.text(rect.get_x() + rect.get_width()/2.,
                 1.01*height,
                '%d' % int(height),
                ha='center', va='bottom')

    plt.show()



if __name__ == '__main__':
    
    metadata = {}
    for line in open('output/diversity_regular.txt'):
        linesplit = line.split(":")
        artist = linesplit[0]
        metada = linesplit[1].split(";")
        metadata[artist] = {'nbUniqueTokens': int(metada[0]), 'nbTokens': int(metada[1]), 'nbSongs': int(metada[2])}
    
    plotMetadata(metadata, 'nbUniqueTokens', "Number of Unique tokens per Rapper", "Unique Tokens")
    plotMetadata(metadata, 'nbTokens', "Number of Tokens per Rapper", "Tokens")
        
        
        
