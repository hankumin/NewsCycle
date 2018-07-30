#!usr/bin/python


#PURPOSE OF SCRIPT
#phraseCounter takes in a input file of symbols or a working directory of metabot and
#finds the frequency of these symbols within a corpus of stories


import os
import re
import gzip
import argparse
import csv
#Keeps track of any symbols that did not have a acorn in ticker_secid_name
errorMessage = ''


#synonymsCreator takes in the work directory, people flag, locations flag and word Flag
#Creates the dictionary of the all symbols that need to be counted within the documents
#Returns dictionary with the symbol and other info as key, and its value as just the symbol
#Dictionary [fullSymbol] = symbol
def synonymsCreator(directory,people,locations,words):
    stringNames = []

    if not os.path.isdir(os.path.join(directory,'noah')):
        print("Error: Not a working directory containing Noah directory")
        return {}
    if not os.path.isfile(os.path.join(directory,'mapper/ticker_secid_name.map')):
        print("Error: Not a working directory containing mapper/ticker_secid_name.map")
        return {}

    if people or not (people or locations or words):

        if not os.path.isfile(os.path.join(directory,'noah/peoplenames')):
            print("Error: File peoplenames does not exist")
            return {}

        fNames = open(os.path.join(directory,'noah/peoplenames'),'r')
        allNames = fNames.read().upper()
        stringNames += re.findall(r'lastname, "([^"]*)"',allNames,re.IGNORECASE)
        stringNames += re.findall(r'firstname, "([^"]*)"',allNames,re.IGNORECASE)
        fNames.close()

    if locations or not (people  or locations or words):

        if not os.path.isfile(os.path.join(directory,'noah/locations')):
            print("Error: File locations does not exist")
            return {}

        fLocation = open(os.path.join(directory,'noah/locations'),'r')
        allLocations = fLocation.read().upper()
        stringNames += re.findall(r', "([^"]*)"',allLocations,re.IGNORECASE)
        fLocation.close()

    if words or not (people or locations or words):

        if not os.path.isfile('lemme-derived-forms-2018-06-13.txt'):
            print("Error: File lemme-derived-forms-2018-06-13.txt does not exist")
            return {}

        fWords = open('lemme-derived-forms-2018-06-13.txt','r')
        allWords = fWords.read().upper()
        stringNames += re.findall(r'(\w*).*',allWords,re.IGNORECASE)
        fWords.close()

    if stringNames == []:
        return {}


    stringNames = set(stringNames)

    dictOfSymbols = {}

    file1 = open(os.path.join(directory,'noah/symbols'),'r')
    stringDict = file1.readlines()
    for l in stringDict:
        if l:
            currentSymbol = re.search(r'"[^"]*"', l)
            if currentSymbol:
                if currentSymbol.group().upper()[1:-1] in stringNames:
                    dictOfSymbols[l.rstrip()] =  tuple(re.split(r'[^a-zA-Z0-9_-]',currentSymbol.group().lower()[1:-1]))
                elif currentSymbol.group().upper() in stringNames:
                    dictOfSymbols[l.rstrip()] = tuple(re.split(r'[^a-zA-Z0-9_-]',currentSymbol.group().lower()))


    file1.close()

    return dictOfSymbols


#checkFileName takes in a file name
#Checks if the file tag is an xml type
#Returns true if the file is an xml else false
def checkFileName(file):
    r = re.compile('\.xml$')
    if re.search( r ,file):
        return True
    return False


#makeKeysForComp takes in the path of an inputfile(file with problematic symbols)
#Creates the dictionary of the all symbols that need to be counted within the documents
#Returns dictionary with the symbol and other info as key, and its value as just the symbol
#Dictionary [fullSymbol] = symbol
def makeKeysForComp(filePath):
    #The company key to the dictionary for frequencies
    compKeys = {}

    #Opens input file and puts each line in the variable company
    f = open(filePath, 'r')
    companies = f.readlines()

    #RegEx for the symbol since it is the 1rst quotes we will see will use a re.search()

    #Place each symbol in from companies in the dictionary symbols
    for c in companies:
        x = re.search(r'"[^"]*"',c)
        if x:
            compKeys[c.rstrip()] = tuple(re.split(r'[^a-zA-Z0-9_-]',(x).group().lower()[1:-1]))

    f.close()

    return compKeys


#makeFreqDict takes in dictionary created by synonymsCreator or makeKeysForComp
#Creates dictionary that will hold frequency of each symbols
#Returns a 2D Dictionary with the symbols length as keys and a the value a dictionary of all the
#words with a frequency of 0
#Dictionary[symbolLength] = {Symbol:0}
def makeFreqDict(Sym):
    freqDict = {}

    for s in Sym:
        currentPhrase = Sym[s]
        if str(len(currentPhrase)) in freqDict:
            freqDict[str(len(currentPhrase))][currentPhrase] = 0
        else:
            freqDict[str(len(currentPhrase))] = {currentPhrase:0}

    return freqDict


#findFreq takes in the dictionary from makeFreqDict and the path of the Corpus directory
#Finds the frequency of symbol and updates them on a Dictionary
#Returns new updated frequency dictionary
#Dictionary[symbol] = freq
def findFreq(freqDict,Corpus):

    returnDict = {}
    fileCount = 0

    files = os.listdir(Corpus)
    for num in freqDict:
        curDict = freqDict[num]

        for file in files:

            begin = 0
            end = int(num)

            if checkFileName(Corpus+'/'+file):
                fileCount += 1
                f = open(Corpus+'/'+file,'r')
                currentString = f.read().lower()
                currentString = re.split(r'[^a-zA-Z0-9_-]',currentString)

                length = len(currentString)

                while end<=length:

                    x = tuple(currentString[begin:end])

                    if x in curDict:
                        if x in returnDict:
                            returnDict[tuple(currentString[begin:end])]+=1
                        else:
                            returnDict[tuple(currentString[begin:end])]=1

                    begin+=1
                    end+=1

                f.close()

    if fileCount == 0:
        print('Error: Corpus does not contain any xml files')
        return {}

    return returnDict


#writeFreq takes in the work directory, Dictionary of companies and freq, and output file
#Writes the symbol, frequency and acorn of each file onto the output file
def writeFreq(Companies,directory,freq,out):


    #findAcorn takes in the current symbol, exchangesymbol and duns dictionary
    #Finds the current acorn for the symbol
    #returns the acorn
    def findAcorn(es,duns,curr):
        global errorMessage
        x = ''
        currentExchange = re.search(r'ACORN:\d*',curr,re.IGNORECASE)
        if currentExchange:
            x = currentExchange.group()[6:]
            return x

        if not currentExchange:
            currentExchange = re.search(r'DUNS:\d*',curr,re.IGNORECASE)
            if currentExchange:
                x = currentExchange.group()[5:]
                if x in duns:
                    return duns[x]

        if not currentExchange:
            currentExchange = re.search(r'[^,|;]*',curr,re.IGNORECASE)
            if currentExchange:
                x = currentExchange.group()
                if x in es:
                    return es[x]

        errorMessage += 'Error: '+c+'\n'
        return 'ERROR'


    f = open(out,'w')
    exchangeSymbols = {}
    duns = {}
    with open(os.path.join(directory,'mapper/ticker_secid_name.map')) as csvfile:
        doc = csv.DictReader(csvfile, delimiter = '|')
        for row in doc:
            exchangeSymbols[row['Exchange']+':'+row['Symbol']] = row['ACORN']
            duns[row['Duns']] =  row['ACORN']

        csvfile.close()

    #writes the company in the file
    for c in Companies:
        if Companies[c] in freq:
            s = c +' ACORN:'+findAcorn(exchangeSymbols,duns,c)+" Frequency: "+str(freq[Companies[c]])+"\n"
            f.write(s)
        else:
            s = c +' ACORN:'+findAcorn(exchangeSymbols,duns,c)+" Frequency: 0"+"\n"
            f.write(s)

    if not errorMessage == '':
        f.write('"\n'+errorMessage+'"')

    f.close()


def main():
    #Creates the arguments for the program
    global args
    parser = argparse.ArgumentParser('''
    1rst Argument is the Corpus directory
    2nd Argument is the output Directory
    3rd Argument is the Work directory of metabot( this is the -d flag)
    -n: Flag for people's names
    -l: Flag for locations
    -w: Flag for words
    Example: "python phraseCounterE4.py /Corpus/ Output.txt -d /nwsy/metabot/ -n -l"
    Looks for the frequency of names and locations from the Corpus and places them Output.txt,
    the names are found in /nwsys/metabot/
    ''')

    #Path of the corpus files
    parser.add_argument('corpus', type = str, help = "Path of the corpus")
    #Path of the input files
    parser.add_argument('-i', dest = 'input', type = str, help = "Path of the input file containing problematic symbols",default = '' )
    parser.add_argument('-d', dest = 'direct', type = str, help = "Working Directory containing noah",default = '' )
    parser.add_argument('-n', dest = 'name', action = 'store_true', help = "Path of file with names",default = False )
    parser.add_argument('-l', dest = 'locations', action = 'store_true', help = "Path of file with locations",default = False )
    parser.add_argument('-w', dest = 'words', action = 'store_true', help = "Path of file with words",default = False )
    #Path of the output file
    parser.add_argument('output', type = str, help = "Path and name of the output file" )

    args = parser.parse_args()

    if not os.path.isdir(args.corpus):
        print("Error: Corpus directory does not exist")
        return 0

    if not os.path.isdir(args.direct):
        print("Error: Work directory does not exist")
        return 0

    if not args.input =='':
        symbols = makeKeysForComp(args.input)
    elif not args.direct == '' :
        symbols = synonymsCreator(args.direct,args.name,args.locations,args.words)
    else:
        print 'Error: Working directory was not given'
        return 0

    if symbols == {}:
        return 0

    freqDict = makeFreqDict(symbols)

    freq = findFreq(freqDict,args.corpus)

    if freq == {}:
        return 0

    writeFreq(symbols,args.direct,freq,args.output)

    return 1

if __name__ == '__main__':
    main()
