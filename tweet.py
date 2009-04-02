#!/usr/bin/env python

# Created by David Busby on 02/02/2009.
# http://saiweb.co.uk
# Uses urllib to post a tweet
# http://creativecommons.org/licenses/by-sa/2.0/uk/ CC BY-SA

import sys, getopt, urllib

def usage():
    print "Usage: ",sys.argv[0]," [-u username][-p password][-t your tweet here][-j][-v]"
    print "-u Twitter username"
    print "-p Twitter password"
    print "-t Tweet"
    print "-j output will return JSON response from twitter server"
    print "-v Verbose output"
    sys.exit(0)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:p:t:v", ["help", "output="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    
    usr = ""
    pwd = ""
    tweet = ""
    verbose = 0
    json = 0
    
    for o, a in opts:
        if o in ("-h", "--help"):
           usage()
        elif o == "-u":
            usr = a
        elif o == "-p":
            pwd = a
        elif o == "-t":
            tweet = a
        elif o == "-v":
            verbose = 1
        elif o == "-j":
            json = 1
        else:
            assert False, "unhandled option"
    
    ltweet = len(tweet)
    if ltweet > 140:
        print "Your tweet is too long %s chars, this must be a maximum of 140 chars" % (ltweet)
        sys.exit(0)
        
    if verbose == 1:
        print "Got tweet of %s length attempting to send" % (ltweet)
    
    
    constring = "http://%s:%s@twitter.com/statuses/update.json" % (usr,pwd)
    tweet = urllib.urlencode({"status":tweet})
    
    f = urllib.urlopen(constring, tweet)
    
    if json == 1:
        print f.read()
    elif verbose == 1:
        print "Tweet sent"
     

if __name__ == "__main__":
    main()