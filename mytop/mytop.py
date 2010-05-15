#!/usr/bin/env python
"""
 mytop python, by David Busby (saiweb.co.uk)
 Based on the original mytop by Jeremy D. Zawodny (http://jeremy.zawodny.com/mysql/mytop/)
"""

import os,sys,getopt
from optparse import OptionParser,OptionGroup, OptParseError

def usage():
	tmp = 'Usage:',sys.argv[0],'[-h hostname][-u username][-p password][-d update delay]'\
	'-h mySQL host'\
	'-u mySQL username'\
	'-p mySQL password'\
	'-d update delay in seconds'\
	'Note: host,username,password are optional if ~/.my.cnf exists'
	help = ''
	for line in tmp:
		help = "%s\n" % help
	return help
def main():

	parser = OptionParser(usage=usage(),version="%prog 1.0")
	parser.add_option('-o','--host',dest='host',help='mySQL host')
	parser.add_option('-u','--user',dest='usr',help='mySQL user')
	parser.add_option('-p','--password',dest='pwd',help='mySQL password')
	parser.add_option('-d','--delay',dest='delay',help='polling delay in seconds')

	(options,args) = parser.parse_args()

	if os.path.isfile('~/.my.cnf'):
		print 'found .my.cnf file'
	else:		
		print 'I could not find your ~/.my.cnf'
		exit = False
		if options.usr == None:
			print 'Username was not specified, I need this to continue'
			exit = True
		if options.pwd == None:
			print 'Password was not specified, I need this to continue'
			exit = True
		if options.host == None:
			print 'Host was not specified, I am defaulting to localhost'
			host = 'localhost'
		
		if exit:
			usage()
			sys.exit()
		

if __name__ == '__main__':
	main()
