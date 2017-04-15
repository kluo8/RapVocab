# RapVocab
Apply big data analytics methods and algorithms to analyze and compare famous Rappers based on their lyrics.
The different comparison methods used rely on terms frequency and diversity (number of unique words).
We use classical word counts algoriths, TF.IDF scores, cosine similarity, statistics and clustering.


## How to Crawl
Requires BeautifulSoup

1. Run `python crawler.py [url]`
  - Example: `python crawler.py http://www.azlyrics.com/k/kendricklamar.html`
2. See lyrics in data/azlyrics/

## How to Filter the crawled lyrics
Format: `python filter.py [filter]`

Usage:
* `python filter.py L` (L = lemmatization)
  * Requires nltk's wordnet package to be installed. 
  * In the python environment, run `nltk.download()`. The NLTK downloader will pop up, under the Packages tab select the wordnet package for installation.
* `python filter.py P` (P = profanity)

## How to Perform the Different Analysys
This section uses different libraries such as Spark. In addition to having the libraries installed the following is required
* SPARK env var pointing to spark folder location: SPARK=<spark-location> (for linux)
* Add following path to PATH env variable: export PATH=$PATH:${SPARK}/bin: (for linux)
* Add add SPARK's python libs to the python path: PYTHONPATH=${SPARK}/python (for linux)

Running the different analysis:

1. Run `wordcount.py` from the wordcount package first. The result are found in the output subfoler of the package. Those results are necessary for other analysis.
2. For 2D analysys/clustering of the songs (dimensions are: diversity and size), you can either run `cureclustersongvectors.py`, `diversitystats.py` or `kmeansclustersongvectors.py` from the `clustering` package. Refer to each module documentation for more details.
3. For Vocabulary set based classification, run `classification.py` from the `classification` package. Refer to the module documentation for more information





