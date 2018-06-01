#!usr/bin/python

import glob
import gzip
import re

#Opens file to see if it contains the RegExp phrase
def checkFile(file, phrases):
    #file's txt is stored in txt
    f = open(file)
    txt = f.readlines()

    #looks at the 1rst phrase of RegExp phrases and returns if true or false if it is it
    for phrase in phrases:
        for line in txt:
            if phrase.search(line):
                f.close()
                return True
    f.close()
    return False



def main():
    #looks at all files
    thefiles = glob.glob('../corpus/*.rdf')

    #compiles p in to a RegExpObj regexes
    regexes = [re.compile(p) for p in ['IC/nmtl.plas']]
    for file in thefiles:
        if checkFile(file,regexes):
            print file
if __name__ == '__main__':
    main()
