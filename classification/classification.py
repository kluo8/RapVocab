#!/usr/bin/env python3
import sys
import os
sys.path.append('../')
from plotclassification import plotArtistClassification
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from libs import iohelper
import re
'''
Created on Mar 23, 2017

@author: arno
'''

WORKING_DIR = os.getcwd()
DATA_LYRICS_PATH = WORKING_DIR + "/../data/azlyrics/"



def gatherSongs():
    files = iohelper.listDirectoryContent(DATA_LYRICS_PATH, True)
    documents = []
    for f in files :
        for line in open(DATA_LYRICS_PATH + f):
            documents.append(open(f).read())
    
    return documents
    
def artistName(filename):
    return re.sub("\..*$", "", filename)

def gatherArtistLyrics():
    
    files = iohelper.listDirectoryContent(DATA_LYRICS_PATH, True)
    documents = {}
    for f in files :
        documents[artistName(f)] = open(DATA_LYRICS_PATH +f).read()
    
    return documents



def artistSimilarity():
    lyrics = gatherArtistLyrics()
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(lyrics.values())
    similarity = cosine_similarity(tfidf_matrix[0:len(lyrics)], tfidf_matrix)
    
    artistNames = list(lyrics.keys())
    
    simMap = {}
    for i, sims in enumerate(similarity):
        artistSim = {}
        for j, sim in enumerate(sims):
            artistSim[artistName(artistNames[j])] = sim
            
        artist = artistName(artistNames[i])
        simMap[artist] = artistSim
        plotArtistClassification(simMap[artist], artist, artist)
            

if __name__ == '__main__':
    
    artistSimilarity()
    
    
    
    
    