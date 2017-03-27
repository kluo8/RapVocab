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
HDFS_LOCAL_ACCESS = "file://"

WORKING_DIR = os.getcwd()
DATA_PATH = WORKING_DIR + "/../data"
DATA_AZLYRICS_PATH = DATA_PATH + "/azlyrics/"
DATA_LEMMATIZE_PATH = DATA_PATH + "/lemmatization/"
DATA_PROFANITY_PATH = DATA_PATH + "/profanity/"
WORD_COUNT_OUTPUT = WORKING_DIR + "/output/counts/"
OUTPUT = WORKING_DIR + "/output/"
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
def processData(path, version):

    ID = 1
    artistIdTable = {}
    diversity = {}

    idFile = open(ARTIST_ID_TABLE, 'w')
    diversityFile = open(''.join([OUTPUT, '/diversity_', version, '.txt']), 'w')
    files = iohelper.listDirectoryContent(path, True)
    for f in files:
        artist = re.sub(r'\.txt', '', f)
        print("processing: " + artist + " " + version)

        if artist not in artistIdTable:
            artistIdTable[artist] = ID
            idFile.write(''.join([artist, " ", str(ID), '\n']))
            ID+=1

        wordsTuple = wordCountByArtist(artist, ''.join([path, f]), version=version)
        nbSongs = songProcessing(artist, artistIdTable[artist], ''.join([path, f]), version=version)
        print(wordsTuple)
        print("nb songs: " + str(nbSongs))
        diversityFile.write(''.join([artist, ':', str(wordsTuple[1]), ';',wordsTuple[2], ";", str(nbSongs), '\n']))
        diversity[artist] = {'nbUniqueTokens': wordsTuple[1], 'nbTokens': wordsTuple[2], 'nbSongs': nbSongs}
        
    diversityFile.close()
    idFile.close()
#     plotMetadata(diversity)
    

# Analyze songs individually
def songProcessing(artist, artistId, filePath, version='regular'):

    lines = SPARK_CONTEXT.textFile(HDFS_LOCAL_ACCESS + filePath).\
        flatMap(lambda x: x.encode('utf-8').split('\n'))
    lines.foreach(lambda x: buildSongVectorSVM(x, artist, artistId, version))
    return lines.count()


# Build song vector where dimensions are the following: nb of words, nb unique tokens, profane (eventually
# use libSVM format: <label> <index1>:<value1> <index2>:<value2>
# use song length and diversity
def buildSongVectorSVM(song, artist, artistId, version):

    song = song.decode('utf-8').lower()
    total_tokens = nltk.word_tokenize(song)
    uniqueToken = set(total_tokens)
    entry = ''.join([str(artistId), ' 1:', str(len(total_tokens)), ' 2:' , str(len(uniqueToken)), '\n'])
    entryPyCl = ''.join([str(len(total_tokens)), ' ' , str(len(uniqueToken)), '\n'])

    f = open(''.join([OUTPUT,'song_vectors_', version, '.txt']), 'a')
    fPyCl = open(''.join([OUTPUT,'song_vectors_pyclustering_', version,'.txt']), 'a')

    f.write(entry)
    fPyCl.write(entryPyCl)

    f.close()
    fPyCl.close()

if __name__ == '__main__':

    #Note that output directory is cleaned beforehand if ran through shell script
    
    processData(DATA_AZLYRICS_PATH, "regular")
    processData(DATA_LEMMATIZE_PATH, "lemmatize")
    processData(DATA_PROFANITY_PATH, "profanity")
    
    



