#!usr/bin/python

import glob
import gzip

#checks if x is null and returns false if it is else true
def checkFile(file, phrase):
    f = open(file)
    txt = f.readlines()
    count = 0
    limit = len(txt)
    while(count<limit):
        if phrase in txt[count] :
            close(f)
            return True
        else:
            count = count+1
    f.close()
    return False



def main():
    thefiles = glob.glob('../corpus/*.rdf')
    # thefiles = glob.glob('dummy.txt')
    count = 0
    limit = len(thefiles)
    while(count<limit):
        if (checkFile(thefiles[count],'IC/nmtl.plas')):
            print thefiles[count]
            count = count+1
        else:
            count = count+1
if __name__ == '__main__':
    main()
