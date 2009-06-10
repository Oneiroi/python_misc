#!/usr/bin/env python
"""
    Author: David Busby (http://saiweb.co.uk)
    Program: Python Subversion hook for Saiweb, sends updates to twitter
    Copyright: David Busby 2009. All rights reserved.
    License: http://creativecommons.org/licenses/by-sa/2.0/uk/
"""

import urllib2, base64, sys, os, syslog, getopt, re
from urllib import urlencode

class updater:
    
    def __init__(self, usr, pwd, revision, repo):
        self.usr = usr
        self.pwd = pwd
        self.url = 'http://twitter.com/statuses/update.json'
        self.tag = 'SVN_TWEETER'
        
        self.rev = revision
        self.repo = repo
    
    def _exec(self, cmd):
        prg = os.popen(cmd,"r")
        str = ''
        for line in prg.readlines():
            str += line    
        return str
    
    def _get_author(self):
        cmd = 'svnlook author -r %s %s' % (self.rev,self.repo)
        return self._exec(cmd)
        
    def _get_log(self):
        cmd = 'svnlook log -r %s %s' % (self.rev,self.repo)
        return self._exec(cmd)
    
    def _get_date(self):
        cmd = 'svnlook date -r %s %s' % (self.rev,self.repo)
        return self._exec(cmd)
    
    def _get_changed(self):
        cmd = 'svnlook changed -r %s %s' % (self.rev,self.repo)
        return self._exec(cmd)
    def _get_project(self):
        """ matches first valid folder, will return folder name if not branches or 2nd foldername if branches """
        str = self._get_changed()
        m = re.match('.*? ([^/]+)',str)
        
        if m != None:
            """ we have matches """
            if m.group(1).lstrip(' ') == 'branches':
                m = re.match('.*?branches/([^/]+)',str)
                if m != None:
                    """ we have matches """
                    return m.group(1)
                else:
                    return ''
            else:
                return m.group(1).lstrip(' ')
        
    def log(self,str):
        str = '%s: %s' % (self.tag, str)
        syslog.syslog(str)
        
    def update(self,update):
       """ adapted from: http://www.saiweb.co.uk/python/python-urllib2-basic-http-authentication """
       req = urllib2.Request(self.url)
       try:
           res = urllib2.urlopen(req,urlencode({"status":update}))
           headers = res.info().headers
           data = res.read()
       except IOError, e:
            if hasattr(e, 'reason'):
                err = "%s ERROR(%s)" % (self.url,e.reason)
                print err
            elif hasattr(e, 'code'):
                if e.code != 401:
                    err = "%s ERROR(%s)" % (self.url,e.code)
                    self.log(err)
                #401 = auth required error
                elif e.code == 401:
                    base64string = base64.encodestring('%s:%s' % (self.usr, self.pwd))[:-1]
                    authheader =  "Basic %s" % base64string
                    req.add_header("Authorization", authheader)
                    try:
                        res = urllib2.urlopen(req)
                        headers = res.info().headers
                        data = res.read()
                    except IOError, e:
                        if hasattr(e, 'reason'):
                            err = "%s:%s@%s ERROR(%s)" % (self.usr,self.pwd,self.url,e.reason)
                            self.log(err)
                        elif hasattr(e, 'code'):
                            err = "%s:%s@%s ERROR(%s)" % (self.usr,self.pwd,self.url,e.code)
                            self.log(err)
                    else:
                        err = "%s query complete" % (self.url)
                        self.log(err)
       else:
            err = "%s query complete" % (self.url)
            self.log(err)
        
    
def usage():
    print "Usage: ",sys.argv[0]," [-u username][-p password][-r revision][-s /path/to/svn]"
    print "-u Twitter username"
    print "-p Twitter password"
    print "-r revision"
    print "-s /path/to/repo"
    sys.exit(0)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "hu:p:r:s:", ["help", "output="])
    except getopt.GetoptError, err:
        print str(err)
        usage()
        sys.exit(2)
    
    usr = ""
    pwd = ""
    rev = 0
    repo = ""
    
    for o, a in opts:
        if o in ("-h", "--help"):
           usage()
        elif o == "-u":
            usr = a
        elif o == "-p":
            pwd = a
        elif o == "-r":
            rev = a
        elif o == "-s":
            repo = a
        else:
            assert False, "unhandled option"
            
    if(len(usr) == 0):
        print "User not supplied ..."
        usage()
    if(len(pwd) == 0):
        print "Password not supplied ..."
        usage()
    if(rev == 0):
        print "Revision not supplied ..."
        usage()
    if(len(repo) == 0):
        print "Subversion repository not supplied ..."
        usage()
        
    upd = updater(usr,pwd,rev,repo)
    
    update = "[SVN] Commit (%s) r%s by %s: %s" % (upd._get_project(), rev, upd._get_author(), upd._get_log())
    
    if(len(update) > 140):
        update = "%s..." % (update[0:137])
    
    upd.update(update)
    
if __name__ == "__main__":
    main()