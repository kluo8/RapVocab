import sys
import os
sys.path.append('../')
from libs import iohelper
import re

'''
Created on Mar 29, 2017
@author: arno

Take the first 26K lyrics of each rapper.
Essential to perform diversity comparison
'''


WORKING_DIR = os.getcwd()
DATA_PATH = WORKING_DIR + "/../data"
DATA_AZLYRICS_PATH = DATA_PATH + "/azlyrics/"
DATA_LEMMATIZE_PATH = DATA_PATH + "/lemmatization/"
DATA_PROFANITY_PATH = DATA_PATH + "/profanity/"
DATA_26K_PATH = DATA_PATH + "/26k/"

def cutTo26K(path, destination):
    files = iohelper.listDirectoryContent(path, True)
    for f in files:
        lyricsFile = open(''.join([path, f]))
        content = lyricsFile.read()
        content = re.sub('\n', '', content)
        content = content.split()
        print(f, len(content))
        newContent = ''
        for i, token in enumerate(content):
            if i > 26150:
                break
            
            newContent = ' '.join([newContent, token])
        print(len(newContent))
        truncatedLyrics = open(''.join([DATA_26K_PATH, destination,  f]), 'w')
        truncatedLyrics.write(newContent)
        truncatedLyrics.close()
        lyricsFile.close()
    
cutTo26K(DATA_AZLYRICS_PATH, "azlyrics/")
cutTo26K(DATA_LEMMATIZE_PATH, "lemmatization/")
cutTo26K(DATA_PROFANITY_PATH, "profanity/")



