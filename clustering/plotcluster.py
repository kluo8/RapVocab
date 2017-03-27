
import matplotlib.pyplot as plt
import math
import numpy as np
import re
'''
Created on Mar 18, 2017

@author: arno
'''

COLORS = ['b', 'c', 'y', 'm', '#AF7FB5', '#4F6D27', '#D0A94C', '#794044', '#871606']

'''
plot 2D cluster
result entry format: Row(label=1.6114804284613683e+18, features=SparseVector(2, {0: 778.0, 1: 438.0}), prediction=3)
clusterCenters: coordinates of centroids
'''
def plot2DSparkCluster(result, clusterCenters, xAxis="x", yAxis="y", title=''):
    color=[]
    x=[]
    y=[]
    area=[]

    for r in result:
        vector = r['features']
        c = r['prediction']
        xx = vector[0]
        yy = vector[1]
        color.append(COLORS[int(c)])
        area.append(math.pi*6**2)
        x.append(xx)
        y.append(yy)

    plt.scatter(x,y,c=color,s=area)
    plt.xlabel(xAxis)
    plt.ylabel(yAxis)
    plt.title(title)

    color=[]
    x=[]
    y=[]
    area=[]

    if clusterCenters is not None:
        for idx, center in enumerate(clusterCenters):
            xx = center[0]
            yy = center[1]
            color.append(COLORS[idx])
            area.append(300)
            x.append(xx)
            y.append(yy)

    plt.scatter(x,y,c=color,s=area, marker='s', linewidths=3.0)


'''
plot clustering of artist songs based on diversity and size
'''
def plotDiversitySizeClustering(result, clusterCenters, xAxis="x", yAxis="y", title=''):

    plot2DSparkCluster(result, clusterCenters, xAxis, yAxis, title)

    # define region
    x = np.array(range(0, 3000))
    y = eval('x')
    plt.plot(x, y, c='white')
    plt.ylim((-50,720))
    plt.xlim((-50,2500))

    y1 = x
    y2 = 1
    plt.fill_between(x, y1, y2, color = 'blue', alpha= '0.1')

    plt.show()



'''
Bar chart
ref: http://matplotlib.org/examples/api/barchart_demo.html
'''
def barChartArtistCountInCluster(artistSongsClustering, clusters):
    clusterNb = len(clusters)
    label = []
    counts = {}
    bars = []
    fig, ax = plt.subplots()

    N = len(artistSongsClustering)
    ind = np.arange(N)
    width = 0.20

    # init dictionary of cluster counts
    for c in range(len(clusters)):
        counts[c] = []

    # add for each artist the count for each cluster
    for artist, clusterCounts in artistSongsClustering.items():
        total = float(sum([int(v) for k, v in clusterCounts.items()]))
        label.append(artist)
        for c, cCount in clusterCounts.items() :
            counts[int(c)].append((cCount/total*100))
    n = 0;
    for cluster, cCount in counts.items():
        bars.append(ax.bar(ind + width*n, cCount, width, color=COLORS[int(cluster)]))
        n+=1

    # add some text for labels, title and axes ticks
    ax.set_ylabel('Percentage of Songs')
    ax.set_title('Artist Song Count for Each Cluster')
    ax.set_xticks(ind + width * clusterNb/2)
    ax.set_xticklabels(artistSongsClustering.keys())
    ax.set_xticklabels(list(map(lambda x: re.sub("(.{5})", "\\1\n", x, 0, re.DOTALL), artistSongsClustering.keys())))
    

    allBars = map(lambda x: x[0], bars)
    ax.legend(allBars, [str(k) + " - " + str(v) for k, v in enumerate(clusters)])

    for bar in bars:
        for rect in bar:
            height = rect.get_height()
            ax.text(rect.get_x() + rect.get_width()/2.,
                     1.05*height,
                    '%d%%' % int(height),
                    ha='center', va='bottom')

    plt.show()








