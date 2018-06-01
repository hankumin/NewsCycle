#!usr/bin/python
import gzip
import re
import os

#returns true when word has aeiou in this order
def vowelWord(word,vowels):
    return vowels.search(word)

def main():
    theDict = open('/usr/share/dict/words')
    theWordexp = re.compile('^[qwrtypsdfghjklzxcvbnm]*a[qwrtypsdfghjklzxcvbnm]*e[qwrtypsdfghjklzxcvbnm]*i[qwrtypsdfghjklzxcvbnm]*o[qwrtypsdfghjklzxcvbnm]*u[qwrtypsdfghjklzxcvbnm]*$')

    theWords = theDict.readlines()

    for word in theWords:
        if (vowelWord(word,theWordexp)):
            print word

    theDict.close()

if __name__ == '__main__':
  main()
