#!/usr/bin/env python
"""
ideone.com paster
"""
 
from sys import stdin, stderr
from SOAPpy import WSDL
import sys, getopt
 
 
#settings
IDEONE_SERVICE = 'http://ideone.com/api/1/service.wsdl'
USER = 'test'
PASS = 'test'
LANG = 'text'
 
 
#language code tables
LANGS_CODE = {
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
 
def getLangCode(lang):
    if LANGS_CODE.has_key(lang):
        return LANGS_CODE[lang]
    return LANGS_CODE['default']
 
 
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
 
 
#options handling
USAGE = """
cat somefile | ideone.py [KEY]...
or
ideone.py file1 file2 file3
 
    KEYS:
    -h      - this usage
    -u 'user' - set ideone's username to 'user'
    -p 'pass' - set ideone's password to 'pass'
    -l 'lang' - set code's language to 'lang'
"""
 
def usage():
    print USAGE
    exit(0)
 
def changeUser(newUser):
    global USER
    USER = newUser
 
def changePass(newPass):
    global PASS
    PASS = newPass
 
def changeLang(newLang):
    global LANG
    LANG = newLang
 
CHANGE_ARGS = {
        '-u': changeUser,
        '-p': changePass,
        '-l': changeLang
}
 
FLAG_ARGS = {
        '-h': usage
}
 
def parseArgs(args):
    copts = CHANGE_ARGS.keys()
    fopts = FLAG_ARGS.keys()
    return getopt.getopt(args,
            ''.join(map(lambda arg: arg.replace('-', '') + ':', copts)) +
            ''.join(map(lambda arg: arg.replace('-', ''), fopts)))
 
def applyOpts(optlist):
    for opt in optlist:
        if opt[1] != '':
            CHANGE_ARGS[opt[0]](opt[1])
        else:
            FLAG_ARGS[opt[0]]()
 
#ideone wsdl client
IDEONE = WSDL.Proxy(IDEONE_SERVICE)
 
def paste(file):
    source = file.read()
    response = IDEONE.createSubmission(USER, PASS, source, getLangCode(LANG), '', False, False)
    res = ''
    if isError(response):
        printErrorAndDie(getErrorCode(response))
    else:
        return "http://ideone.com/%s" % (response['item'][1]['value'])
 
 
optlist, filelist = parseArgs(sys.argv[1:])
applyOpts(optlist)
 
if filelist == []:
    print paste(stdin)
else:
    for filename in filelist:
        file = open(filename, "r")
        print paste(file)
        file.close()
 
