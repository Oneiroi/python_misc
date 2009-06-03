#!/usr/bin/env python
#
#  saiweb_crawler.py
# 
# Basic crawler
# http://saiweb.co.uk

# http://creativecommons.org/licenses/by-sa/2.0/uk/ CC BY-SA
#imports
import urllib2, syslog, base64

TAG='SAIWEB_CRAWLER'

#URL list, DO NOT include http:// prefix
urls = {
            0:{"url":"www.saiweb.co.uk/some/script.php","user":"someuser","pass":"apassword"},
        }

def log(str):
    str = "%s: %s" % (TAG, str)
    #print str
    syslog.syslog(str)
    
def main():
    log("Started")
    ecount = 0;
    ulen = len(urls)
    for i in range(0,ulen):
        url = "http://%s" % (urls[i]["url"])
        req = urllib2.Request(url)
        try:
           res = urllib2.urlopen(req)
           headers = res.info().headers
           data = res.read()
        except IOError, e:
            if hasattr(e, 'reason'):
                err = "%s ERROR(%s)" % (urls[i]["url"],e.reason)
                log(err)
                ecount = ecount+1
            elif hasattr(e, 'code'):
                if e.code != 401:
                    err = "%s ERROR(%s)" % (urls[i]["url"],e.code)
                    log(err)
                    ecount = ecount+1
                #401 = auth required error
                elif e.code == 401:
                    base64string = base64.encodestring('%s:%s' % (urls[i]["user"], urls[i]["pass"]))[:-1]
                    authheader =  "Basic %s" % base64string
                    req.add_header("Authorization", authheader)
                    try:
                        res = urllib2.urlopen(req)
                        headers = res.info().headers
                        data = res.read()
                    except IOError, e:
                        if hasattr(e, 'reason'):
                            err = "%s:%s@%s ERROR(%s)" % (urls[i]["user"],urls[i]["pass"],urls[i]["url"],e.reason)
                            log(err)
                            ecount = ecount+1
                        elif hasattr(e, 'code'):
                            err = "%s:%s@%s ERROR(%s)" % (urls[i]["user"],urls[i]["pass"],urls[i]["url"],e.code)
                            log(err)
                            ecount = ecount+1
                    else:
                        err = "%s query complete" % (urls[i]["url"])
                        log(err)   
        else:
            err = "%s query complete" % (urls[i]["url"])
            log(err)
    err = "Completed %s Errors %s" % (ulen,ecount)
    log(err)
    
    
if __name__ == "__main__":
    main()
