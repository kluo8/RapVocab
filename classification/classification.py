#!/usr/bin/env python3

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
'''
Created on Mar 23, 2017

@author: arno
'''


def gatherSongs():
    documents = (
        "The sky is blue",
        "The sun is bright",
        "The sun in the sky is bright",
        "We can see the shining sun, the bright sun"
        )
    return documents
    
def gatherArtistLyrics():
    documents = (
        "The sky is blue",
        "The sun is bright",
        "The sun in the sky is bright",
        "We can see the shining sun, the bright sun"
        )
    return documents


if __name__ == '__main__':
    
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(gatherArtistLyrics())
    print(tfidf_matrix.shape)
#     print(tfidf_matrix)
    print(tfidf_matrix[0:1])
    simil = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix)
    print(simil)
    
    
    
    
    