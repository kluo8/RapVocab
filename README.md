# RapVocab
Lyrics Analysis of Famous Rappers

## How to Crawl
Requires BeautifulSoup

1. Run `python crawler.py [url]`
  - Example: `python crawler.py http://www.azlyrics.com/k/kendricklamar.html`
2. See lyrics in data/azlyrics/

## How to Wordcont
Requires Apache Spark plus:
* SPARK env var pointing to spark folder location: SPARK=<spark-location> (for linux)
* Add following path to PATH env variable: export PATH=$PATH:${SPARK}/bin: (for linux)

Run `wc_execute_standalone.sh` if on linux or:

1. Create directory `output` in the `wordcount` package and make sure it is empty before running the next command
2. Run `./wordcount.py`
3. Word count for each artist is in the `output` dir and  the file `diversity_*.txt` in the `wordcount` package contains the nb of diff lyrics for each artist

## How to Filter
Format: `python filter.py [filter]`

Usage:
* `python filter.py L` (L = lemmatization)
  * Requires nltk's wordnet package to be installed. 
  * In the python environment, run `nltk.download()`. The NLTK downloader will pop up, under the Packages tab select the wordnet package for installation.
* `python filter.py P` (P = profanity)



