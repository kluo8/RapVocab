#!/usr/bin/env python

import sys
sys.path.append('../')
from libs import iohelper
import re
import os
from pyspark import SparkContext, SparkConf
import nltk

# Spark Requirements
SPARK_CONF = SparkConf().setAppName("wordcount").setMaster("local")
SPARK_CONTEXT = SparkContext(conf=SPARK_CONF)

# IO Sources
WORKING_DIR = os.getcwd()
DATA_PATH = WORKING_DIR+"/../data/"
DATA_AZLYRICS_PATH = DATA_PATH+"/azlyrics/"
WORD_COUNT_OUTPUT = "output/counts/"
OUTPUT = "output/"
DIVERSITY_REGULAR_FILE = OUTPUT + 'diversity_regular.txt'
SONG_VERCTOR = OUTPUT+'song_vectors.txt'

# clear diversity and vector files
f = open(DIVERSITY_REGULAR_FILE, 'w')
f.close()
f = open(SONG_VERCTOR, 'w')
f.close()


# Count occurences of each different word an artist uses
def wordCountByArtist(artist, filePath, version='regular'):
    
    outputFile = ''.join([WORD_COUNT_OUTPUT, version, '_', artist])
    
    counts = SPARK_CONTEXT.textFile(filePath).\
        flatMap(lambda x: x.split()).\
        map(lambda x: (x,1)).\
        reduceByKey(lambda x,y: x+y).\
        sortBy(lambda (word, count): count, False)
        
    counts.saveAsTextFile(outputFile)
    f = open(DIVERSITY_REGULAR_FILE, 'a')
    f.write(''.join([artist, ': ', str(counts.count()), '\n']))
    f.close()
    
# Process data from a lyrics directory
def processData(path):
    files = iohelper.listDirectoryContent(path, True)
    for f in files:
        artist = re.sub(r'\.txt', '', f)
        wordCountByArtist(artist, ''.join([DATA_AZLYRICS_PATH, f]))
        songProcessing(artist, ''.join([DATA_AZLYRICS_PATH, f]))


# Analyze songs individually
def songProcessing(artist, filePath, version = 'regular'):
    
    lines = SPARK_CONTEXT.textFile(filePath).\
        flatMap(lambda x: x.split('\n'))
    print("Nb songs for " + artist+ ": ", lines.count())
    lines.foreach(lambda x: buildSongVector(x, artist))
    

# Build song vector where dimensions are the following: nb of words, nb unique tokens, profane (eventually
def buildSongVector(song, artist):
    
    song = str(song).lower()
    total_tokens = nltk.word_tokenize(song)
    uniqueToken = set(total_tokens)
    entry = ''.join([artist, ':', str(len(total_tokens)),',' , str(len(uniqueToken)), '\n'])
    f = open(SONG_VERCTOR, 'a')
    f.write(entry)
    f.close()



if __name__ == '__main__':
    
    processData(DATA_AZLYRICS_PATH)
        
    
    
    
    
    
    