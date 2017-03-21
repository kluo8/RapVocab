#!/usr/bin/env python

import os
import sys
sys.path.append('../')
from pyspark.ml.clustering import KMeans as dfKMeans
from pyspark.sql import SparkSession
from pyspark.mllib.clustering import KMeansModel, KMeans
from pyspark.mllib.linalg import Vectors
from clustering.plotcluster import plot2DSparkCluster

'''
Created on Mar 18, 2017
Use python 2.7

@author: arno
'''

HDFS_LOCAL_ACCESS = "file://"

WORKING_DIR = os.getcwd()
SONG_VECTORS_FILE = WORKING_DIR + "/../wordcount/output/song_vectors.txt"
ARTIST_ID_FILE = WORKING_DIR + "/../wordcount/output/artist_id.txt"

CENTERS = [[1.0, 1.0],
           [2500.0, 1.0],
           [0.0, 700.0],
           [2500.0, 700.0]]

CENTER_VECTORS = map(lambda center: Vectors.dense(center), CENTERS)

ARTIST_ID = {}

def extractArtistId():
    for line in open(ARTIST_ID_FILE):
        line = line.rstrip('\n').split()
        ARTIST_ID[int(line[1])] = line[0]
        print(int(line[1]))

'''
Perform kmeans clustering with an prior estimation of the centroids

:param dataset:
    Dataframe object
:param nClusters:
    nb of clusters desired
'''
def kmeansEstimator(dataset, nClusters):
    print("Fit kmeans model to dataset")
    kmeans = dfKMeans(k=nClusters)
    model=kmeans.fit(dataset)
        
    print("Show centroids")
    centers = model.clusterCenters()
    print(centers)
    
    print("Apply model to data and show result")
    result = model.transform(dataset)
    result.show()
    plot2DSparkCluster(result.collect(), centers, "Size", "Diversity", "Song Analysis by Size and Diversity")
    

''''
Perform Kmeans Clustering with centroids predefined
:param dataset:
    Dataframe object
'''
def kmeansInitialClusters(dataset):
    model = KMeansModel(CENTER_VECTORS)
    vectorsRdd = dataset.rdd.map(lambda data: Vectors.parse(Vectors.stringify(data['features'])))
    trainedModel = KMeans.train(vectorsRdd, 4, initialModel=model)
    result=[]
    for d in dataset.collect():
        entry = {}
        entry["features"] = d["features"]
        entry["prediction"] = trainedModel.predict(Vectors.parse(Vectors.stringify(d['features'])))
        entry["label"] = d['label']
        result.append(entry)
        
    plot2DSparkCluster(result, CENTERS, "Size", "Diversity", "Song Analysis by Size and Diversity")
    centroidArtistSongCount(result, CENTERS)
    
'''
Count the number of songs each artist has for each cluster

:param result:
    collection with following entry format: 
    {label=<artist id>, features=<song vector>, prediction=<cluster index>}

'''
def centroidArtistSongCount(result, centroids):
    artists={}
    
    for entry in result:
        print(int(entry["label"]))
        artist = ARTIST_ID[int(entry["label"])]
        centroid = str(entry["prediction"])
        if artist not in artists:
            artists[artist] = {}
            for i in range(0, len(centroids)):
                artists[artist][str(i)] = 0
        
        artists[artist][centroid]+= 1
    
    for artist, value in artists.items():
        for key, value in value.items():
            print(str(artist) + " - " + str(key) + ": " + str(value))
    

if __name__ == '__main__':
    
    extractArtistId()
    
    print("Initialize Spark session")
    spark = SparkSession \
        .builder \
        .appName("Lab session") \
        .getOrCreate()
    
    print("Read dataset")
    dataset = spark.read.format("libsvm").load(HDFS_LOCAL_ACCESS + SONG_VECTORS_FILE)
    
    kmeansEstimator(dataset, 4)
    kmeansInitialClusters(dataset)
    
    
    spark.stop()
    
    
    
    