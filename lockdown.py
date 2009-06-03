#!/usr/bin/env python

# Created by David Busby http://saiweb.co.uk
# with thanks to Matthew Ife from uKFast for re-introducing me to Python and the Gamin package, and writing a test script to get me started with this!
# License: http://creativecommons.org/licenses/by-nc-sa/2.0/uk
# This script is designed to monitor webroots to enforce permissions in a shared hosting environment
# This should be used in conjuction with mod_suexec or suPHP
# REQ: Gamin package


import gamin, os, re, stat
from time import sleep
from socket import *

#listen stack
watch = []
watch.append('/var/www');
#ignore stack
ignore = []

#sleep
short_sleep=0.5
long_sleep=1
#listen socket
listen_sock = 40000
#file chmods
dir_chmod = 0711
php_chmod = 0600
misc_chmod = 0644

def mode_check(path, expected_mode):
    info = os.stat(path)
    if oct(info[stat.ST_MODE] & 0777) == oct(expected_mode & 0777):
        return True
    else:
        return False

# EVENTS (from /usr/lib64/python2.4/site-packages/gamin.py 01/05/09)
#
# the type of events provided in the callbacks.
#
# GAMChanged=1
# GAMDeleted=2
# GAMStartExecuting=3
# GAMStopExecuting=4
# GAMMoved=6
# GAMCreated=5
# GAMExists=8
# GAMAcknowledge=7
# GAMEndExist=9

def lockdown_event(path, event, which):
    full_path = os.path.join(which, path)
    #new file/dir created
    if event == gamin.GAMCreated:
        if os.path.isdir(full_path):
            #is directory add to listen stack
            print "Directory-created (%s)" % (full_path)
            mon.watch_directory(full_path,lockdown_event)
            watch.append(full_path)
            #chmod if perms incorrect
            if mode_check(full_path, dir_chmod) == False:
                print "Directory-created (%s) incorrect chmod (%s) setting to (%s)" % (full_path, oct(os.stat(full_path)[stat.ST_MODE] & 0777), oct(dir_chmod & 0777))
                os.chmod(full_path,dir_chmod)
        elif os.full_path.isfile(full_path):
            #is file created chmod correctly
            print "File-created (%s) created" % (full_path)
            if re.search('\.php$',full_path):
                #chmod if perms incorrect
                if mode_check(full_path, php_chmod) == False:
                    print "File-created (%s) incorrect chmod (%s) setting to (%s)" % (full_path, oct(os.stat(full_path)[stat.ST_MODE] & 0777), oct(php_chmod & 0777))
                    os.chmod(full_path, php_chmod)
            else:
                #chmod if perms incorrect
                if mode_check(full_path, misc_chmod) == False:
                    print "File-created (%s) incorrect chmod (%s) setting to (%s)" % (full_path, oct(os.stat(full_path)[stat.ST_MODE] & 0777), oct(misc_chmod & 0777))
                    os.chmod(full_path, misc_chmod)
    #deleted event            
    elif event == gamin.GAMDeleted:
        #if the full_path is in the listen stack, stop listenging and remove it from stack
        if full_path in watch:
            print "Deleted (%s)"
            mon.stop_watch(full_path)
            watch.remove(full_path)   
    #only care about the chnaged or moved event, probably don't even care about moved  
    elif event == gamin.GAMChanged or event == gamin.GAMMoved:
       
        #php file
        if re.search('\.php$',full_path):
            #chmod if perms incorrect
            if mode_check(full_path, php_chmod) == False:
                print "File-changed (%s) incorrect chmod (%s) setting to (%s)" % (full_path, oct(os.stat(full_path)[stat.ST_MODE] & 0777), oct(php_chmod & 0777))
                os.chmod(full_path, php_chmod)
        else:
            #chmod if perms incorrect
            if mode_check(full_path, misc_chmod) == False:
                print "File-changed (%s) incorrect chmod (%s) setting to (%s)" % (full_path, oct(os.stat(full_path)[stat.ST_MODE] & 0777), oct(misc_chmod & 0777))
                os.chmod(full_path, misc_chmod)
    else:
        print "Unhandled event (%s) on (%s)" % (str(event), full_path)

#setup the watch monitor
mon = gamin.WatchMonitor()
mon.watch_directory('/var/www', lockdown_event, '/var/www')

#listen socket, to be used for nagios monitoring
#fork off a child thread
parent = os.fork()
if not parent:
    sock = socket(AF_INET, SOCK_STREAM)
    sock.bind(('localhost', listen_sock))
    sock.listen(4)
    while 1:
        conn, addr = sock.accept()
        print "Connection from", addr
        conn.send("OK")
        conn.close()
else: 
    #program loop
    while True:
        if mon.event_pending():
            print "Got Events, processing now"
            sleep(short_sleep) #small sleep time just incase more events queue up during the handle_events() call, otherwise cpu load will go through the roof
            mon.handle_events()
        else:
            print "No events sleeping for %s" %(str(long_sleep))
            #must have a sleep event if nothing to handel otherwise program loops way too fast causing 100% cpu load
            sleep(long_sleep) #increase/decrease as required (remember a very short sleep time will result in faster changes but higher cpu load)