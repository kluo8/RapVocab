import nltk
import sys
import string
import os
import re
from nltk.stem import WordNetLemmatizer

def main(filter):
    custom_badwords = load_badwords()

    path = 'data/azlyrics/'

    for filename in os.listdir(path):
        lyric_file = open("data/azlyrics/" + filename, encoding="utf8")
        content = lyric_file.read()
        # Makes all words lowercase
        content = str(content).lower()
        # Removes all punctuation
        content= ''.join(c for c in content if c not in string.punctuation)
        # Removes numbers
        content = re.sub(r'\d+', '', content)
        # Removes unicode
        content = re.sub(r'[^\x00-\x7F]+', ' ', content)

        tokens = []
        # Tokenizes entire text
        tokens = nltk.word_tokenize(content)
        print (filename + "\t" + str(len(tokens)))
        if filter == "L":
            # Lemmatizes only the nouns
            tokens = [WordNetLemmatizer().lemmatize(x) for x in tokens]
            filter_folder = "lemmatization"
        elif filter == "P":
            # Removes profanity
            tokens = [x for x in tokens if x not in custom_badwords]
            filter_folder = "profanity"

        output_file = open("data/" + filter_folder + "/" + filename, "w")
        num = 0
        for t in tokens:
            num += 1
            # Only prints 100 words per line
            if num % 100 == 0:
                output_file.write(t + "\n")
            else: 
                output_file.write(t + " ")

        lyric_file.close()
        output_file.close()

def load_badwords():
    with open("custom_badwords.txt") as f:
        content = f.readlines()
    content = [x.strip() for x in content]
    return content


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print ("No filter chosen.")
    else:
        valid_filters = ["L", "P", "N"]
        filter = str(sys.argv[1])

        if filter in valid_filters:
            main(filter)
        else:
            print ("Filter not valid.")

    sys.exit()