import matplotlib.pyplot as plt
import numpy as np
import operator

'''
Created on Mar 25, 2017

@author: arno
'''

def plotArtistClassification(similars, artist, key):
    similars.pop(key)

    sortedSim = sorted(similars.items(), key=operator.itemgetter(1), reverse=True)

    fig, ax = plt.subplots()

    ind = np.arange(len(similars))

    width = 0.3
    margin = 0.5

    bars = ax.bar(margin+ind, list(map(lambda x: float(x[1]), sortedSim)), width, color='blue')

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Cosine Similarity')
    ax.set_title('Similarity with Rapper: ' + artist)
    ax.set_xticks(margin + ind + width/2)
    ax.set_xticklabels(list(map(lambda x: x[0], sortedSim)))


    for bar in bars:
        ax.text(bar.get_x() + bar.get_width(),
                     1.01 * float(bar.get_height()),
                    '%03.3f%%' % float(bar.get_height()),
                    ha='center', va='bottom')

    axes = plt.gca()
    axes.set_ylim([0, 1.10])

    fig.set_size_inches(22.5, 10.5)
    fig.savefig("plots/" + artist + ".png", dpi=100)


