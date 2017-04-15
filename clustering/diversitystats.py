#!/usr/bin/env python
'''
Created on Mar 22, 2017
@author: arno

Analyze rappers'songs with a boxplot analysis on the lyrics diversity
Plot the resuts in a 2D graph with clusters representing different
ranges of of song size and diversity

Display a bar chart for the percentage of each rapper's songs in each category

*** Requires wordcount.py from wordcount package to be run beforehand ***

'''

import os
import sys
sys.path.append('../')
from pyspark.sql import SparkSession
from clustering.plotcluster import plotDiversitySizeClustering
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
from clustering.kmeansclustersongvectors import centroidArtistSongCount

# mpl.use('agg')

WORKING_DIR = os.getcwd()
HDFS_LOCAL_ACCESS = "file://"
SONG_VECTORS_FILE = "../wordcount/output/song_vectors_pyclustering_regular.txt"
SONG_VECTORS_FILE_SPARK = WORKING_DIR + "/../wordcount/output/song_vectors_regular.txt"

MAX_SIZE = 0

CLUSTERS = [["< Median", "1/2"], ["< Median", "2/2"],
            ["> Median", "1/2"], ["> Median", "2/2"]]

def gatherSongsDiversity():
    
    maxSize = 0
    data = []
    
    for line in open(SONG_VECTORS_FILE):
        line = line.rstrip('\n').split()
        if float(line[1]) == 0 or float(line[0]) == 0:
            continue
        data.append(float(line[1])/float(line[0]))
        if line[0] > maxSize: 
            maxSize = line[0]
    return [data, maxSize]


def generateBoxPlot(data):
    
    fig, ax = plt.subplots()
    bp = ax.boxplot(data)
    ax.set_title("Song Lexical Richness Boxplot")
    whiskers = sorted(list(bp["whiskers"][0].get_ydata()) + list(bp["whiskers"][1].get_ydata()) + [np.median(list(data))])
    plt.show()
    plt.cla()
    plt.clf()
    return whiskers


def assignCluster(point, boxPlot, maxSize):
    median = boxPlot[2]
    if point[0] == 0:
        return 0
    diversity = point[1]/point[0]
    clstr = 6;
    if diversity < median:
        clstr = 0
    else:
        clstr = 2
        
    sizePartitions = np.arange(maxSize, step=maxSize/2)
    
    if point[0] < sizePartitions[1]:
        clstr+=0
    else:
        clstr+=1
        
    return clstr
        

def bPlotCluster(dataset, boxPlot, maxSize):
    result=[]
    for d in dataset.collect():
        entry = {}
        entry["features"] = d["features"]
        entry["prediction"] = assignCluster(d["features"], boxPlot, maxSize)
        entry["label"] = d['label']
        result.append(entry)
    return result
    
    

if __name__ == '__main__':
    MAX_SIZE = 0
    data, MAX_SIZE = gatherSongsDiversity()
    bPlot = generateBoxPlot(data)
    print("Max size: " + str(MAX_SIZE))
    
    print("Initialize Spark session")
    spark = SparkSession \
        .builder \
        .appName("Lab session") \
        .getOrCreate()

    print("Read dataset")
    dataset = spark.read.format("libsvm").load(HDFS_LOCAL_ACCESS + SONG_VECTORS_FILE_SPARK)
    
    result = bPlotCluster(dataset, bPlot, int(MAX_SIZE))
    
    plotDiversitySizeClustering(result, None, "Size", "Diversity", "Song Analysis by Size and Diversity with Box Plot Stats")
    centroidArtistSongCount(result, CLUSTERS)
    
    
    
    
    
    
    
    