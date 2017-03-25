#!/usr/bin/env python

import sys
sys.path.append('../')
from plotdata import plotMetadata
from libs import iohelper
import re
import os
from pyspark import SparkContext, SparkConf
import nltk

# Spark Requirements
SPARK_CONF = SparkConf().setAppName("wordcount").setMaster("local")
SPARK_CONTEXT = SparkContext(conf=SPARK_CONF)

# IO Sources
HDFS_LOCAL_ACCESS = "file://"

WORKING_DIR = os.getcwd()
DATA_PATH = WORKING_DIR + "/../data"
DATA_AZLYRICS_PATH = DATA_PATH + "/azlyrics/"
WORD_COUNT_OUTPUT = WORKING_DIR + "/output/counts/"
OUTPUT = WORKING_DIR + "/output/"
DIVERSITY_REGULAR_FILE = OUTPUT + 'diversity_regular.txt'
SONG_VERCTOR = OUTPUT + 'song_vectors.txt'
SONG_VERCTOR_PY_CLUSTERING = OUTPUT + 'song_vectors_pyclustering.txt'
ARTIST_ID_TABLE = OUTPUT + 'artist_id.txt'


def countTotal(counts):
    sum = 0
    for w in counts.collect():
        sum+=int(w[1])
    return sum
        

# Count occurences of each different word an artist uses
def wordCountByArtist(artist, filePath, version='regular'):

    outputFile = ''.join([HDFS_LOCAL_ACCESS, WORD_COUNT_OUTPUT, version, '_', artist])

    counts = SPARK_CONTEXT.textFile(HDFS_LOCAL_ACCESS + filePath).\
        flatMap(lambda x: x.encode('utf-8').split()).\
        map(lambda x: (x, 1)).\
        reduceByKey(lambda x, y: x + y).\
        sortBy(lambda (word, count): count, False)

    totalWords = countTotal(counts)

    counts.saveAsTextFile(outputFile)
    return (artist, str(counts.count()), str(totalWords))

# Process data from a lyrics directory
def processData(path):

    ID = 1
    artistIdTable = {}
    diversity = {}

    idFile = open(ARTIST_ID_TABLE, 'w')
    diversityFile = open(DIVERSITY_REGULAR_FILE, 'w')
    files = iohelper.listDirectoryContent(path, True)
    for f in files:
        artist = re.sub(r'\.txt', '', f)

        if artist not in artistIdTable:
            artistIdTable[artist] = ID
            idFile.write(''.join([artist, " ", str(ID), '\n']))
            ID+=1

        wordsTuple = wordCountByArtist(artist, ''.join([DATA_AZLYRICS_PATH, f]))
        nbSongs = songProcessing(artist, artistIdTable[artist], ''.join([DATA_AZLYRICS_PATH, f]))
        diversityFile.write(''.join([artist, ':', str(wordsTuple[1]), ';',wordsTuple[2], ";", str(nbSongs), '\n']))
        diversity[artist] = {'nbUniqueTokens': wordsTuple[1], 'nbTokens': wordsTuple[2], 'nbSongs': nbSongs}
        
    diversityFile.close()
    idFile.close()
#     plotMetadata(diversity)
    
    


# Analyze songs individually
def songProcessing(artist, artistId, filePath, version='regular'):

    lines = SPARK_CONTEXT.textFile(HDFS_LOCAL_ACCESS + filePath).\
        flatMap(lambda x: x.encode('utf-8').split('\n'))
    lines.foreach(lambda x: buildSongVectorSVM(x, artist, artistId))
    return lines.count()


# Build song vector where dimensions are the following: nb of words, nb unique tokens, profane (eventually
# use libSVM format: <label> <index1>:<value1> <index2>:<value2>
# use song length and diversity
def buildSongVectorSVM(song, artist, artistId):

    song = song.decode('utf-8').lower()
    total_tokens = nltk.word_tokenize(song)
    uniqueToken = set(total_tokens)
    entry = ''.join([str(artistId), ' 1:', str(len(total_tokens)), ' 2:' , str(len(uniqueToken)), '\n'])
    entryPyCl = ''.join([str(len(total_tokens)), ' ' , str(len(uniqueToken)), '\n'])

    f = open(SONG_VERCTOR, 'a')
    fPyCl = open(SONG_VERCTOR_PY_CLUSTERING, 'a')

    f.write(entry)
    fPyCl.write(entryPyCl)

    f.close()
    fPyCl.close()

if __name__ == '__main__':

        # clear diversity and vector files
    f = open(SONG_VERCTOR, 'w')
    f.close()
    f = open(SONG_VERCTOR_PY_CLUSTERING, 'w')
    f.close()

    processData(DATA_AZLYRICS_PATH)




