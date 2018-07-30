#!usr/bin/python

import MySQLdb
import os
import re
import argparse
from fabric.api import *

def placeFile(machine, file, path, user, why):
    if re.search(r'.mmu',machine):
        machine+='.acquiremedia.com'
    elif re.search(r'.labs',machine):
        machine+='.acquiremedia.com'
    else:
        machine+='.mmu.acquiremedia.com'

    if machine == 'njdev6.labs.acquiremedia.com':
        return 0

    with settings(host_string=machine, user = "nadmin", password="nadmin"):
        fileName = os.path.basename(file)
        thePath = os.path.join(path,'putTmp')
        run('mkdir -p ' +thePath)
        put(file,thePath)
        run('/nwsys/release/bin/nwinstall -s -i '+user+' -w '+'\''+why+'\''+' '+path+' '+ os.path.join(thePath,fileName) )
        run('rm -rf '+ thePath )


def main():
    global args
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', dest = 'dev', action = 'store_true', help = "Devs",default = False )
    parser.add_argument('-o', dest = 'other', action = 'store_true', help = "Prods",default = False )
    parser.add_argument('-p', dest = 'prod', action = 'store_true', help = "Others",default = False )
    parser.add_argument('-t', dest = 'path',type = str, help = "Temporary directory/path for file, places in /pool/home/nadmin",default = '/pool/home/nadmin' )
    parser.add_argument('-f', dest = 'file',type = str, help = "File wished to be transfered",default = '' )
    parser.add_argument('-i', dest = 'user',type = str, help = "User for nwinstall",default = 'nadmin' )
    parser.add_argument('-w', dest = 'why',type = str, help = "Why-the-change for nwsintall",default = 'Unknown' )


    args = parser.parse_args()


    db = MySQLdb.connect(user= 'live',passwd='live123',host = 'monitor.mmu.acquiremedia.com',db = 'metabot_config', port =3306 )
    c = db.cursor()
    c.execute("""SELECT server_name, deployGroup FROM mbot_servers WHERE deployGroup='PROD' OR deployGroup='DEV' OR deployGroup='Other'""")
    c.fetchall()

    if not os.path.isfile(args.file):
        print("Error: Files specified does not exist")
        return 0

    for current in c:
        if not (args.dev or args.other or args.prod) and current[1] == 'DEV':
            print current
            if not (args.file == ''):
                placeFile(current[0],args.file,args.path,args.user,args.why)
        else:
            if (args.dev and current[1] == 'DEV'):
                print current
                if not (args.file == ''):
                    placeFile(current[0],args.file,args.path,args.user,args.why)
            if (args.prod and current[1] == 'PROD'):
                print current
                if not (args.file == ''):
                    placeFile(current[0],args.file,args.path,args.user,args.why)
            if (args.other and current[1] == 'Other'):
                print current
                if not (args.file == ''):
                    placeFile(current[0],args.file,args.path,args.user,args.why)


if __name__ == '__main__':
    main()
