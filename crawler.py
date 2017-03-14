from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlopen
import re
import string
import sys
import time


# Method that finds all links within each url
def findAllLinks(url, links, regex, myFile):
    # Open the URL
    soup = BeautifulSoup(urlopen(url), "html.parser")

    all_song_titles = []

    # Find all anchor tags to retrieve the link
    for link in soup.findAll('a'):


        # Ensures that the anchor tag has an href attribute before continuing
        if link.has_attr('href'):
            path = link['href'].replace("..", "")
            fullURL = baseURL + path

            # Removes anything in () that's part of the song title
            song_title = re.sub(r' \(([^()]+)\)', '', link.text)

            # Verifies that the link matches the given regular expression
            # and verifies that the link does not already exists in the set
            if regex.match(link['href']) and (fullURL not in links) and (song_title not in all_song_titles):
                print (link.text)

                # Extracts text from the given URL
                text = extractText(fullURL, regex)

                # If the URL is redirected to a page out of the scope
                # then None is returned from the extractText method
                if text is not None:
                    links.append(fullURL)
                    all_song_titles.append(song_title)
                    myFile.write(str(text) + "\n")

                # Time delay to prevent getting blacklisted from the lyrics website
                time.sleep(10)
                
            
# Extracts text from each web page
def extractText(url, regex):

    # Open the link
    response = urlopen(url)

    soup = BeautifulSoup(response, "html.parser")
    # Removes script tags
    [s.extract() for s in soup("script")]

    # Finds the div where the lyrics are
    no_class = soup.findAll("div", class_=None)
    no_id = soup.findAll("div", id=None)
    section = list(set(no_class) & set(no_id))
    for main in section:
        main = BeautifulSoup(str(main), "html.parser")
        text = main.find('div').text

    # Removes pattern - e.g. [Singer:]
    text = re.sub(r'\[([A-Za-z0-9\s.:?()"\';:-]+)\]', '', text)
    # Removes all punctuation
    text = ''.join(c for c in text if c not in string.punctuation)
    # Removes numbers
    text = re.sub(r'\d+', '', text)
    # Removes unicode
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)

    format_text = " ".join(line.strip() for line in text.split("\n"))

    return format_text


if __name__ == '__main__':

    if len(sys.argv) < 2:
        print ("No URL to crawl")
    else:
        url = str(sys.argv[1])

        parsedURL = urlparse(url)
        # Gets root of URL
        baseURL = '{uri.scheme}://{uri.netloc}'.format(uri=parsedURL)

        links = []

        pathURL = '{uri.path}'.format(uri=parsedURL)
        artist = re.sub(r'/([A-Za-z0-9-]+)/', '', pathURL)
        artist = re.sub(r'.html', '', artist)

        lyrics_artist_path = "lyrics/" + artist

        if artist:
            regex = re.compile(
                "../" + lyrics_artist_path + "/" + "([A-Za-z0-9/.?=&-]*)")
    
            foldername = "data/"
            my_file = open(foldername + "azlyrics/" +
                          artist + ".txt", "w")

            findAllLinks(url, links, regex, my_file)

            my_file.close()

    sys.exit()
