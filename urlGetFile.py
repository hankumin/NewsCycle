#!/usr/bin/env python

from bs4 import BeautifulSoup
import urllib2
import os
import argparse
from subprocess import call
import re


#splitXml takes in the content from specifed url
#Looks for the xml story between the <nitf> tags
#Returns the content of xml file but also returns failed if <nitf> tags do not exist
#Will prompt user no <nitf> tag
def splitXml(content):
    content = re.sub(r'<document>',"",content)
    content = re.sub(r'</document>',"",content)

    content = re.search(r'<nitf>.*</nitf>',content, re.DOTALL)

    if not content:
        return 'FAILED'

    content = content.group()[6:-7]

    content = '<?xml version="1.0"?>\n'+content
    return content


#splitRdf takes in the content from specifed url
#Looks for the rdf story after the <nitf> tags
#Returns the content of rdf file but also returns failed if <nitf> tags do not exist
#Will prompt user no <nitf> tag
def splitRdf(content):
    content = re.sub(r'<document>',"",content)
    content = re.sub(r'</document>',"",content)

    content = re.search(r'</nitf>.*',content, re.DOTALL)

    if not content:
        return 'FAILED'

    content = content.group()[7:]

    content = '<?xml version="1.0"?>\n'+content

    return content


#printCodes takes in the flags for specific codes
#Will check subject, industry, location, company codes and print them
#Return false if any of the flags are toggled and will prevent the default print option
def printCodes(content,s,l,i,c):
    flag = True

    #Checks the flags and prints the appropriate code based off flag
    #Will toggle flag if any code flag is true thus prevent the entire article being printed out
    if s:
        subjects = re.findall(r'<xn:subjectCode>.*</xn:subjectCode>', content)
        if len(subjects) == 0:
            print 'No Subjects'
        for line in subjects:
            print line
        flag = False

    if l:
        locations = re.findall(r'<xn:locationCode>.*<xn:locationCode>', content)
        if len(locations) == 0:
            print 'No Locations'
        for line in locations:
            print line
        flag = False

    if i:
        industry = re.findall(r'<xn:industryCode>.*</xn:industryCode>', content)
        if len(industry) == 0:
            print 'No industries'
        for line in industry:
            print line
        flag = False

    if c:
        company = re.findall(r'<xn:companyCode>.*</xn:companyCode>', content)
        if len(company) == 0:
            print 'No Companies'
        for line in company:
            print line
        flag = False

    return flag


#printSpecifiedCodes takes in a user defined code
#Will check for specified code tags and print them out
#Return 0 if subject code is not specified or if misspelled
def printSpecifiedCodes(content,spec):
    if spec == '':
        return 0

    code = re.findall(r'<xn:'+spec+'>.*</xn:'+spec+'>', content, re.IGNORECASE)
    if len(code) == 0:
        print 'Specified code was empty (also maybe misspelling)'
        return 0

    for l in code:
        print l


def main():
    global args

    parser = argparse.ArgumentParser('Returns the the file or writes file from the given RID')

    #Different Flag input
    parser.add_argument('-t', dest = 'target', type = str, help = "Path of the target directory",default = '' )
    parser.add_argument('--spec', type = str, help = "Specific code",default = '' )
    parser.add_argument('-m', dest = 'make', action = 'store_true', help = "Make new directory at requested target directory",default = False )
    parser.add_argument('-s', dest = 'sub', action = 'store_true', help = "Prints subject codes",default = False )
    parser.add_argument('-l', dest = 'loc', action = 'store_true', help = "Prints company codes",default = False )
    parser.add_argument('-i', dest = 'ind', action = 'store_true', help = "Prints industry codes",default = False )
    parser.add_argument('-c', dest = 'comp', action = 'store_true', help = "Prints locations",default = False )

    parser.add_argument('code', type = str, help = "Code for the url")
    args = parser.parse_args()

    #Checks RID on this url and reads the content of the url
    response = urllib2.urlopen('http://dev-opens-apache-vir.gcloud.acquiremedia.com/getxmlnews/returnXmlnews.php?nneURL='+args.code)
    html = response.read()

    #Checks the html of the url
    soup = BeautifulSoup(html, "lxml")

    #Looks for 'pre' tags within the html and returns error stating it is not a proper rid if it could not find it
    tabulka = soup.find("pre")
    if not tabulka:
        print 'Error: No pre tags in article (Check if RID is correct or exists)'
        return 0

    #Places the html into content
    content =  tabulka.get_text()

    #Prints the content or writes content onto the directory based of flags
    if args.target == '':
        printSpecifiedCodes(content,args.spec)
        if printCodes(content,args.sub,args.loc,args.ind, args.comp) and args.spec == '':
            print content
    else:
        if args.make:

            call('mkdir -p '+args.target, shell = True)

            f = open(os.path.join(args.target,args.code)+'.xml','w')
            content = content.encode('utf-8')

            xml = splitXml(content)
            rdf = splitRdf(content)

            if xml  == 'FAILED':
                print 'Error: Could not find nitf tag'
                return 0

            if rdf  == 'FAILED':
                print 'Error: Could not find nitf tag'
                return 0

            f.write(xml)

            f.close()

            f = open(os.path.join(args.target,args.code)+'.rdf','w')

            f.write(rdf)

            printSpecifiedCodes(content,args.spec)
            printCodes(content,args.sub,args.loc,args.ind, args.comp)

            f.close()

        elif os.path.isdir(args.target):

            f = open(os.path.join(args.target,args.code)+'.xml','w')
            content = content.encode('utf-8')

            xml = splitXml(content)
            rdf = splitRdf(content)

            if xml  == 'FAILED':
                print 'Error: Could not find nitf tag for xml'
                return 0

            if rdf  == 'FAILED':
                print 'Error: Could not find nitf tag for xml'
                return 0

            f.write(xml)

            f.close()

            f = open(os.path.join(args.target,args.code)+'.rdf','w')

            f.write(rdf)

            printSpecifiedCodes(content,args.spec)
            printCodes(content,args.sub,args.loc,args.ind, args.comp)

            f.close()

        else:
            print 'Error: Invalid directory'
            return 0





if __name__ == '__main__':
    main()
