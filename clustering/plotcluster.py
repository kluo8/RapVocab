
import matplotlib.pyplot as plt
import math
'''
Created on Mar 18, 2017

@author: arno
'''



# Plot the cluster 
# result entry format: Row(label=1.6114804284613683e+18, features=SparseVector(2, {0: 778.0, 1: 438.0}), prediction=3)
def plot2DSparkCluster(result, xAxis="x", yAxis="y", title=''):
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
    
    plt.show()