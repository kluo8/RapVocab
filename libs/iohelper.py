import os

# Extract artist lyrics file names from a directory path
# path: path for a directory
# file: whether we are listing files 
def listDirectoryContent(path, isFile):
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