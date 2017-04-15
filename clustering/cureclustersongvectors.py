#!/usr/bin/env python3

'''
Created on Mar 22, 2017
@author: arno


Experiment the cure clustering algorithm on the song 2D vector (diversity, size)

'''

from pyclustering.cluster.cure import cure;
from pyclustering.cluster import cluster_visualizer;
from pyclustering.utils import read_sample;


SONG_VECTORS_FILE = "../wordcount/output/song_vectors_pyclustering_regular.txt"


# read data for clustering from some file
input_data = read_sample(SONG_VECTORS_FILE);

# create instance of cure algorithm for cluster analysis
cure_instance = cure(input_data, 5, 8, 0.7, False);

# run cluster analysis
cure_instance.process();

# get results of clustering
clusters = cure_instance.get_clusters();


visualizer = cluster_visualizer();
visualizer.append_clusters(clusters);
visualizer.show();