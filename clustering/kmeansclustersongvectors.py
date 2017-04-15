#!/usr/bin/env python
'''
Created on Mar 18, 2017
Use python 2.7
@author: arno

Attempt to perform kmeans clustering 
on the songs. Songs are represented by a 
2D vector: (size, diversity)
'''


import os
import sys
sys.path.append('../')
from pyspark.ml.clustering import KMeans as dfKMeans
from pyspark.sql import SparkSession
from pyspark.mllib.clustering import KMeansModel, KMeans
from pyspark.mllib.linalg import Vectors
from clustering.plotcluster import plotDiversitySizeClustering, barChartArtistCountInCluster



HDFS_LOCAL_ACCESS = "file://"

WORKING_DIR = os.getcwd()
SONG_VECTORS_FILE = WORKING_DIR + "/../wordcount/output/song_vectors_regular.txt"
ARTIST_ID_FILE = WORKING_DIR + "/../wordcount/output/artist_id.txt"

CENTERS = [[500.0, 0.0],
           [400.0, 400.0],
           [1500.0, 130.0],
           [1000.0, 500.0]]

CENTER_VECTORS = map(lambda center: Vectors.dense(center), CENTERS)

ARTIST_ID = {}

def extractArtistId():
    mapping = {}
    for line in open(ARTIST_ID_FILE):
        line = line.rstrip('\n').split()
        mapping[int(line[1])] = line[0]
    return mapping

'''
Perform kmeans clustering with an prior estimation of the centroids

:param dataset:
    Dataframe object
:param nClusters:
    nb of clusters desired
'''
def kmeansEstimator(dataset, nClusters):
    kmeans = dfKMeans(k=nClusters)
    model=kmeans.fit(dataset)

    centers = model.clusterCenters()

    result = model.transform(dataset)
    listResult = result.collect()
    plotDiversitySizeClustering(listResult, centers, "Size", "Diversity", "Song Analysis by Size and Diversity with Kmens||")
    centroidArtistSongCount(listResult, centers)

''''
Perform Kmeans Clustering with centroids predefined
:param dataset:
    Dataframe object
'''
def kmeansInitialClusters(dataset):
    model = KMeansModel(CENTER_VECTORS)
    vectorsRdd = dataset.rdd.map(lambda data: Vectors.parse(Vectors.stringify(data['features'])))
    trainedModel = KMeans.train(vectorsRdd, 4, maxIterations=1000, initialModel=model)
    result=[]
    for d in dataset.collect():
        entry = {}
        entry["features"] = d["features"]
        entry["prediction"] = trainedModel.predict(Vectors.parse(Vectors.stringify(d['features'])))
        entry["label"] = d['label']
        result.append(entry)

    plotDiversitySizeClustering(result, CENTERS, "Size", "Diversity", "Song Analysis by Size and Diversity with Initial Clusters")
    centroidArtistSongCount(result, CENTERS)

'''
Count the number of songs each artist has for each cluster

:param result:
    collection with following entry format:
    {label=<artist id>, features=<song vector>, prediction=<cluster index>}

'''
def centroidArtistSongCount(result, centroids):
    artists={}
    
    ARTIST_ID = extractArtistId()
    
    for entry in result:
        artist = ARTIST_ID[int(entry["label"])]
        centroid = str(entry["prediction"])
        if artist not in artists:
            artists[artist] = {}
            for i in range(0, len(centroids)):
                artists[artist][str(i)] = 0

        artists[artist][centroid]+= 1

    barChartArtistCountInCluster(artists, centroids)


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
#     kmeansInitialClusters(dataset)


    spark.stop()



