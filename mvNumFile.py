#!usr/bin/python
from fabric.api import *
import os
import re


def checkFileType(file, phrase):

    if phrase.search(file):
        return True
    return False

def checkFileName(file, provider):

    if provider.search(file):
        return True
    return False

#Takes in number of files, the old directory, new directory, type of file and the TheProvider
#code that that needs to be moved and transfered
def mvFiles(num,oldPath,newPath, ext, provider):

    #creates the list of files in the old directory
    Files = os.listdir(oldPath)

    #initiates the list that will contain all the files we want to look at
    listOfFiles =[]

    #looks for files with correct ext and provider
    if (ext == 'all' or ext == "All") and (provider == "none" or provider == "None"):
        listOfFiles = Files
    elif (ext != 'all' or ext != "All") and (provider == "none" or provider == "None"):
        TheExt = re.compile("."+ext)
        TheProvider = re.compile("^[0-9]{12}"+provider)
        count = 0
        for file in Files:
            if checkFileType(file,TheExt):
                listOfFiles.append(file)
            count+=1
    elif (ext == 'all' or ext == "All") and (provider != "none" or provider != "None"):
        TheProvider = re.compile("^[0-9]{12}"+provider)
        count = 0
        for file in Files:
            if checkFileName(file,TheProvider) :
                listOfFiles.append(file)
            count+=1
    else:
        TheExt = re.compile("."+ext)
        TheProvider = re.compile("^[0-9]{12}"+provider)
        count = 0
        for file in Files:
            if checkFileType(file,TheExt) and checkFileName(file,TheProvider):
                listOfFiles.append(file)
            count+=1

    #Turns num into an int called number and checks if it is a negative num
    number = int(num)
    if number < 0:
        number =0

    #resets count back to zero
    count =0

    #indicate if enough files are there
    flag = False

    #transfers files using local call from the old to the new path
    for i in listOfFiles:
        if count > number-1:
            break
        count+=1
        local("cp "+oldPath+"/"+i+" "+newPath)

    if count >number-1:
        flag = True

    if flag:
        print "Files transfered: Enough files were provided."
    else:
        print  "Files transfered: Not enough files for the request, only transferd "\
        +str(count)+" file."
