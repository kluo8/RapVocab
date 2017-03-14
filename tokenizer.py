import nltk

files = ["drake.txt", "kendricklamar.txt", "chancetherapper.txt"]

for i in files:
    lyric_file = open("data/azlyrics/" + i)
    content = lyric_file.read()
    # Makes all words lowercase
    content = str(content).lower()

    tokens = []
    # Tokenizes entire text
    tokens = nltk.word_tokenize(content)
    print ("Total Tokens:\t" + str(len(tokens)))
    # Removes duplications
    tokens = set(tokens)
    print ("Unique Tokens:\t" + str(len(tokens)))

    token_file = open("data/tokens/" + i, "w")
    num = 0
    for t in tokens:
        num += 1
        # Only prints 50 words per line
        if num % 50 == 0:
            token_file.write(t + "\n")
        else: 
            token_file.write(t + " ")


    lyric_file.close()
    token_file.close()