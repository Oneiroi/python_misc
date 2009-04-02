#!/usr/bin/env python

# Created by David Busby on 30/03/2009.
# Takes a file and puts it on the destination folder of an FTP server
# http://creativecommons.org/licenses/by-sa/2.0/uk/ CC BY-SA

import sys, getopt
from ftplib import FTP

def usage():
    print "Usage: ",sys.argv[0]," [-h][-s][-u][-p][-f][-d]"
    print "-s server_ip or name"
    print "-u ftp username"
    print "-p ftp password"
    print "-f file to send"
    print "-d destination path"
    sys.exit(0)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hs:u:p:f:d:", ["help", "output="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    
    
    

if __name__ == "__main__":
    main()