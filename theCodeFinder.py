#!usr/bin/python
import gzip
import re
import os

#Opens file to see if it contains the RegExp phrase
def checkFiles(file, phrases):
    #file's txt is stored in txt
    f = open('../corpus/'+file)
    txt = f.readlines()

    #looks at the 1rst phrase of RegExp phrases and returns if true or false if it is it
    for phrase in phrases:
        for line in txt:
            if phrase.search(line):
                return True
    return False


def main():
    #looks at all files
    ext = [re.compile(o) for o in ['.rdf']]
    thefiles = os.listdir('../corpus')


    #compiles p in to a RegExpObj regexes
    regexes = [re.compile(p) for p in ['IC/nmtl.plas']]
    for file in thefiles:
        for phrase in ext:
            if(phrase.search(file)):
                if checkFiles(file,regexes):
                    print file
    f.close()
if __name__ == '__main__':
    main()
