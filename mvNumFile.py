#!usr/bin/python
from fabric.api import *
import os
import re


def checkFileType(file, phrase):

    if phrase.search(file):
        return True
    return False


def mvFiles(num,oldPath,newPath, ext):

    #creates the list of files in the old directory
    Files = os.listdir(oldPath)

    #initiates the list that will contain all the files we want to look at
    listOfFiles =[]

    #looks for files with correct ext
    if ext == 'none' or ext == "None":
        listOfFiles = Files
    else:
        TheExt = re.compile("."+ext)
        count = 0
        for file in Files:
            if checkFileType(file,TheExt):
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
        print  "Files transfered: Not enough files for the request, only transferd "+str(count)+\
        " file."
