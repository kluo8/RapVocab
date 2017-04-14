'''
Created on Mar 25, 2017

Bar chart of the classification of the simililarity of an item

@author: arno
'''

import matplotlib.pyplot as plt
import numpy as np
import operator
import re


def plotItemClassification(similars, item, key, title, limit = -1):
    similars.pop(key)

    sortedSim = sorted(similars.items(), key=operator.itemgetter(1), reverse=True)
    
    if limit > -1:
        sortedSim = sortedSim[0:limit]

    fig, ax = plt.subplots()

    ind = np.arange(len(sortedSim))

    width = 0.3
    margin = 0.5

    bars = ax.bar(margin+ind, list(map(lambda x: float(x[1]), sortedSim)), width, color='blue')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Cosine Similarity')
    ax.set_title(title)
    ax.set_xticks(margin + ind + width/2)
    ax.set_xticklabels(list(map(lambda x: re.sub("(.{5})", "\\1\n", x[0], 0, re.DOTALL), sortedSim)))


    for bar in bars:
        ax.text(bar.get_x() + bar.get_width(),
                     1.01 * float(bar.get_height()),
                    '%03.3f%%' % float(bar.get_height()),
                    ha='center', va='bottom')

    axes = plt.gca()
    axes.set_ylim([0, 1.10])

    fig.set_size_inches(22.5, 10.5)
    fig.savefig("plots/" + item + ".png", dpi=100)
    plt.close(fig)


