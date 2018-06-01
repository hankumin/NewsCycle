#!usr/bin/python
import gzip
import re
import os

#returns true when word has aeiou in this order
def vowelWord(word,vowels):
    return vowels.search(word)

def main():
    theDict = open('/usr/share/dict/words')

    #Expressions for words with pattern AEIOU in them
    theWordexp = re.compile('^((?![aeiou]).)*a((?![aeiou]).)*e((?![aeiou]).)*i((?![aeiou]).)*o((?![aeiou]).)*u((?![aeiou]).)*$')

    #places all words in an array
    theWords = theDict.readlines()

    #iterates through each word and checks if the match the pattern and prints
    # the word if they do match
    for word in theWords:
        if (vowelWord(word,theWordexp)):
            print word

    theDict.close()

if __name__ == '__main__':
  main()
