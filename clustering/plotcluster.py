
import matplotlib.pyplot as plt
import math
import numpy as np
'''
Created on Mar 18, 2017

@author: arno
'''


'''
plot the cluster 
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
        color.append(int(c))
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
    
    for center in clusterCenters:
        xx = center[0]
        yy = center[1]
        color.append("red")
        area.append(300)
        x.append(xx)
        y.append(yy)

    plt.scatter(x,y,c=color,s=area)
    
    x = np.array(range(0, 3000))  
    y = eval('x')
    plt.plot(x, y, c='white')  
    plt.ylim((-50,720))
    plt.xlim((-50,2500))
    
    y1 = x
    y2 = 1
    plt.fill_between(x, y1, y2, color = 'blue', alpha= '0.1')
    
    plt.show()
    
    
    
    
    
    
    