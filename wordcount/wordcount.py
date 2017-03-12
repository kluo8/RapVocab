#!/usr/bin/env python

import re
import os
from pyspark import SparkContext, SparkConf

# Spark Requirements
SPARK_CONF = SparkConf().setAppName("wordcount").setMaster("local")
SPARK_CONTEXT = SparkContext(conf=SPARK_CONF)

# IO Sources
WORKING_DIR = os.getcwd()
DATA_PATH = WORKING_DIR+"/../data"
DATA_AZLYRICS_PATH = DATA_PATH+"/azlyrics"
WORD_COUNT_OUTPUT = "output"
DIVERSITY_REGULAR_FILE = "diversity_regular.txt"

# clear diversity files
f = open(DIVERSITY_REGULAR_FILE, 'w')
f.close()


# Count occurences of each different word an artist uses
def wordCountByArtist(artist, filePath):
    
    outputFile = ''.join([WORD_COUNT_OUTPUT, '/wordcount_regular_', artist])
    
    counts = SPARK_CONTEXT.textFile(filePath).\
        flatMap(lambda x: x.split()).\
        map(lambda x: (x,1)).\
        reduceByKey(lambda x,y: x+y)
        
    print(counts.count())
    counts.saveAsTextFile(outputFile)
    
    f = open(DIVERSITY_REGULAR_FILE, 'a')
    f.write(''.join([artist, ': ', str(counts.count()), '\n']))
    f.close()
    
# Process data from a lyrics directory
def processData(path):
    files = listDdirectoryContent(path, True)
    for f in files:
        artist = re.sub(r'\.txt', '', f)
        wordCountByArtist(artist, ''.join([DATA_AZLYRICS_PATH, '/', f]))
    

# Extract artist lyrics file names from a directory path
# path: path for a directory
# file: whether we are listing files 
def listDdirectoryContent(path, isFile):
    if(os.path.exists(path)):
        dirContent = os.listdir(path)
        files = []
        for i in dirContent:
            iPath = ''.join([path, '/', i])
            
            if i != '.' and i!= '..' and \
                    ( (os.path.isfile(iPath) and isFile) or \
                      (os.path.isdir(iPath) and not isFile) ):
                files.append(i)
            
        return files
    else:
        raise Exception('Directory not found')





if __name__ == '__main__':
    
    dataDirs = listDdirectoryContent(DATA_PATH, False)
    for d in dataDirs :
        dirPath = ''.join([DATA_PATH, '/', d])
        processData(dirPath)
        
    
    
    
    
    
    