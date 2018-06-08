#!usr/bin/python
from collections import Counter
import os
import re
import gzip
import argparse


#checks if the file is an xml file
#returns true if it is
def checkFileName(file):
    r = re.compile('\.xml$')
    if re.search( r ,file):
        return True
    return False



# Takes in the path of the output file, the dictionary with companies and frequency
# Opens the output file and writes each company and their freq in the file
def writeFreq(Companies,freq,out):
    f = open(out,'w')

    #writes the company in the file
    for c in Companies:
        if Companies[c] in freq:
            s = c +" " +str(freq[Companies[c]])+"\n"
            f.write(s)
        else:
            s = c +" " +'0'+"\n"
            f.write(s)
    f.close()


def makeDictOfFiles(corpus):
    listOfFiles = os.listdir(corpus)
    curr = Counter()
    final = Counter()

    for file in listOfFiles:
        if checkFileName(file):
            f = open(corpus+'/'+file, 'r')
            text = f.read().lower()
            listOfText = re.split(r'\W',text)
            curr = Counter(listOfText)
            final +=curr
            f.close()

    return final


# Takes in the path of the Input file
# Opens file and places each line in the dictionary with the symbol
# Returns the new Dictionary
def makeKeysForComp(filePath):
    #The company key to the dictionary for frequencies
    compKeys = {}

    #Opens input file and puts each line in the variable company
    f = open(filePath, 'r')
    companies = f.readlines()

    #RegEx for the symbol since it is the 1rst quotes we will see will use a re.search()
    pattern = re.compile('\"[^"]*\"')

    #Place each symbol in from companies in the dictionary symbols
    for c in companies:
        x = (re.search(pattern,c).group().lower())

        compKeys[c.rstrip()] = x[1:-1]

    f.close()

    return compKeys


# Will take an input file with information on specific words
# Example of input: Australia:8CO, "and" # "Orig strip"
# Will look for the freq of the symbol (1rst word in quotes)
# Write the output on specified doc based of the given Path
# Call: python wordCounter.py corpusFiles inputFile outputFile
def main():
    #Creates the arguments for the program
    global args
    parser = argparse.ArgumentParser('''
    Takes the path of corpus, input and outpu files
    ''')

    #Path of the corpus files
    parser.add_argument('corpus', type = str, help = "Path of the corpus",default = '' )
    #Path of the input file
    parser.add_argument('input', type = str, help = "Path of the input file" )
    #Path of the output file
    parser.add_argument('output', type = str, help = "Path and name of the output file" )

    args = parser.parse_args()

    #Creates a dictionary of all the companies(key) with the symbol as their value
    theDict = makeKeysForComp(args.input)

    #Create a dictionary with the companies values as keys and the value of 0 for them

    words = makeDictOfFiles(args.corpus)

    #Writes the requested output
    writeFreq(theDict,dict(words),args.output)

if __name__ == '__main__':
    main()
