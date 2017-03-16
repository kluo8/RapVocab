#!/usr/bin/env python


from libs import iohelper

STOP_WORDS_DIR = "data/stopwords"


if __name__ == '__main__':
    
    stopWords = set()
    
    stopWordsFiles = iohelper.listDirectoryContent(STOP_WORDS_DIR, True)
    print(stopWordsFiles)
    for fileName in stopWordsFiles:
        path = STOP_WORDS_DIR + '/' + fileName
        f = open(path, 'r')
        content = f.read()
        content = str(content).lower().split()
        print(len(content))
        stopWords.update(content)
        
    print(len(stopWords))
        
        
        
    

