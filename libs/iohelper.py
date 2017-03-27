import os
import re

# Extract artist lyrics file names from a directory path
# path: path for a directory
# file: whether we are listing files
'''
Extract content of directory, either files or subdirectories
resulting list sorted in alphabetical order

'''
def listDirectoryContent(path, isFile):
    if(os.path.exists(path)):
        dirContent = sorted(os.listdir(path))
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


def artistName(lyricsFileName):
    return re.sub("\..*$", "", lyricsFileName)
