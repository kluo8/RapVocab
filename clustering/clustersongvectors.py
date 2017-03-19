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

CENTERS = [[1.0, 1.0],
           [2500.0, 1.0],
           [0.0, 700.0],
           [2500.0, 700.0]]
CENTER_VECTORS = map(lambda center: Vectors.dense(center), CENTERS)



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
    

# Kmeans with initial centers defined
# DataFrame dataset 
def KmeansInitialClusters(dataset):
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
    


if __name__ == '__main__':
    
    print("Initialize Spark session")
    spark = SparkSession \
        .builder \
        .appName("Lab session") \
        .getOrCreate()
    
    print("Read dataset")
    dataset = spark.read.format("libsvm").load(HDFS_LOCAL_ACCESS + SONG_VECTORS_FILE)
    
    kmeansEstimator(dataset, 4)
    KmeansInitialClusters(dataset)
    
    
    spark.stop()
    
    
    
    