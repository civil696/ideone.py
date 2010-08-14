#!/usr/bin/env python
"""
ideone.com paster
"""
 
import sys
from sys import stdin, stderr
from SOAPpy import WSDL
from optparse import OptionParser
 
#settings
IDEONE_SERVICE = 'http://ideone.com/api/1/service.wsdl'
 
#language code tables
LANGS_CODES = {
        'ada'       : 7,
        'assembler' : 13,
        'awk'       : 104,
        'bash'      : 28,
        'c'         : 11,
        'c++'       : 1,
        'clojure'   : 111,
        'clisp'     : 32,
        'erlang'    : 36,
        'haskell'   : 21,
        'java'      : 10,
        'lua'       : 26,
        'ocaml'     : 8,
        'perl'      : 3,
        'swipl'     : 15,
        'python'    : 4,
        'scala'     : 39,
        'text'      : 62,
        'default'   : 62
}
 
# error handling
ERROR_MESSAGES = {
        'AUTH_ERROR'        : "User name or user's password are invalid.",
        'PASTE_NOT_FOUND'   : "Paste with specified link could not be found.",
        'WRONG_LANG_ID'     : "Language with specified id does not exist."
}
 
def printErrorAndDie(error):
    msg = 'unknown error'
    if ERROR_MESSAGES.has_key(error):
        msg = ERROR_MESSAGES[error]
    print >> stderr, msg
    exit(1)
 
def getErrorCode(resp):
    return resp['item']['value']['item'][0]['value'] 
 
def isError(resp):
    return resp['item'][0] == 'error'
 
 
#ideone wsdl client
IDEONE = WSDL.Proxy(IDEONE_SERVICE)
 
def paste(file):
    source = file.read()
    response = IDEONE.createSubmission(USER,
                                       PASS,
                                       source,
                                       LANGS_CODES.get(LANG, "default"),
                                       '', False, False)
    res = ''
    if isError(response):
        printErrorAndDie(getErrorCode(response))
    else:
        return "http://ideone.com/%s" % (response['item'][1]['value'])
 
USAGE = """
  cat somefile | %prog [OPTIONS]
  %prog [OPTIONS] file1 file2 file3 """
 
DESCRIPTION = """
This is a paster script for Ideone.
 
"Ideone is a... pastebin. But a pastebin like no other on the Internet. More
accurate expression would be online mini IDE and debugging tool."
-- http://ideone.com/about
"""
 
parser = OptionParser(usage=USAGE, description=DESCRIPTION)
parser.add_option("-u", "--user", dest="USER",
                  default="test",
                  help="use username USER when pasting")
parser.add_option("-p", "--password", dest="PASS", metavar="PASSWD",
                  default="test",
                  help="use password PASSWD when pasting")
parser.add_option("-l", "--language", dest="LANG",
                  default="text",
                  help="treat code as having language LANG (for syntax highlighting etc)")
#parser.set_defaults(USER="test", PASS="test", LANG="text)
 
options, args = parser.parse_args()
globals().update(options.__dict__)
filelist = args
 
if filelist == []:
    print paste(stdin)
else:
    for filename in filelist:
        file = open(filename, "r")
        print "%s:\t%s" % (filename, paste(file))
        file.close()
