#!/usr/bin/env python3
# -*-coding:Latin-1 -*

# Imports #############################################################################################################

from sys import argv, exit
from requests import get
from os.path import basename
from os import popen, unlink
from bs4 import BeautifulSoup
import re

import warnings
warnings.filterwarnings("ignore")

# Settings ############################################################################################################

VERBOSE = 1

class bcolors:
  HEADER = '\033[95m'
  BLUE = '\033[94m'
  GREEN = '\033[92m'
  WARNING = '\033[93m'
  FAIL = '\033[91m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

http_proxy  = "" # "http://10.10.1.10:3128"
https_proxy = "" # "https://10.10.1.11:1080"
ftp_proxy   = "" # "ftp://10.10.1.10:3128"

proxy_dict  = { 
              "http"  : http_proxy, 
              "https" : https_proxy, 
              "ftp"   : ftp_proxy
            }

rows, columns = popen('stty size', 'r').read().split()

headers = {"Range": "bytes=0-1024"}  # first 1024 bytes

# Functionz ###########################################################################################################

def usage():
  print("\nUsage: %s [-d|-v|-c|-r|-t|-T] <url>\n" % (basename(argv[0]),))
  print("  -v : return HTTP headers")
  print("  -d : return HTTP headers with colors")
  print("  -c : return HTTP status code")
  print("  -r : return HTTP reason (Not Found (404), OK (200), ...)")
  print("  -t : return text")
  print("  -T : return title (<title>.+</title>)\n")
  exit(0)

def get_title(htmldata):
  htmlstruct = BeautifulSoup(htmldata,features="html.parser")
  t = ""
  try:
    t = htmlstruct('title')[0]
    t = str(t.prettify()).split("\n")[1].strip()
  except:
    pass
  return(t)

def get_timestamp():
  return( popen("date +%s").read().strip() )

def get_mime(data):
  temp_file = "/tmp/wgetping-%s.tmp" % get_timestamp()
  open(temp_file,"w").write(str(data)[:8192])
  ftype = popen("file -b %s" % temp_file,"r").read().strip()
  unlink(temp_file)
  return(ftype)

# Main ################################################################################################################

if __name__ == '__main__':

  #--------------------------------------------------------------------------------------------------------------------
  ok=0
  if len(argv) >= 2 :
    ok=1
    url = argv[1]

  #--------------------------------------------------------------------------------------------------------------------
  result = "-c"
  if len(argv) == 3 :
    ok=1
    result = argv[1]
    url = argv[2]

  #--------------------------------------------------------------------------------------------------------------------
  if ok == 0:
    usage()

  #--------------------------------------------------------------------------------------------------------------------
  if not re.match(r'^\w+://',url) :
    usage()

  #--------------------------------------------------------------------------------------------------------------------
  try:
    r = get( url , headers=headers , proxies=proxy_dict , verify=False )
  except:
    print("Unreachable host")
    # if VERBOSE:
    #   get( url , headers=headers , proxies=proxy_dict , verify=False )
    exit()

  #--------------------------------------------------------------------------------------------------------------------
  # Number of spaces for full info
  n_s = 0
  m_s = 0
  ok=0
  for h in  r.headers:
    if( n_s < len(h) + 1 ):
      n_s = len(h) + 1
      m_s = n_s

  #--- json -----------------------------------------------------------------------------------------------------------
  if result == "-j":
    ok=1
    n_s =-1 # number of spaces
    m_s = 0 # max of spaces
    for h in  r.headers:
      if( n_s < len(h) + 1 ):
        n_s = len(h) + 1
        m_s = n_s
    res = "{"

    regex = re.compile(r"</?title>", flags=re.I)
    title = " "
    try:
      title = regex.split( r.text )[1].strip()
    except:
      pass

    for h in  r.headers:
      res += "\n  \"" + h + "\":\"" + r.headers[h].replace('"',"\\\"").strip() + "\","
    res += "\n  \"" + "Status-Code" + "\":\"" + str(r.status_code) + "\","
    res += "\n  \"" + "Reason" + "\":\"" + str(r.reason) + "\","
    res += "\n  \"" + "Encoding" + "\":\"" + str(r.encoding) + "\","
    res += "\n  \"" + "URL" + "\":\"" + str(r.url) + "\","
    res += "\n  \"" + "Title" + "\":\"" + title + "\","
    res += "\n  \"" + "Mime-Type" + "\":\"" + get_mime(r.text) + "\","
    res = res[:-1] + "\n}\n"
    print(res)

  #--- verbose (table) -------------------------------------------------------------------------------------------------
  if result == "-v":
    ok=1
    print("\n",end='')
    h = "HTTP Code"   ; print("%s : %s" % ( (h + " " * (m_s - len(h)) , r.status_code)))
    h = "HTTP Reason" ; print("%s : %s" % ( (h + " " * (m_s - len(h)) , r.reason)))
    for h in  r.headers:
      print("%s : %s" % (h + " " * (m_s - len(h)) , r.headers[h]) )
    h = "Title"
    print("%s : %s" % (h +  " " * (m_s - len(h)),get_title(r.text)) )
    h = "Mime-Type"
    print("%s : %s" % (h +  " " * (m_s - len(h)),get_mime(r.text)) )

    print("\n",end='')

  #--- verbose + color (dump) -------------------------------------------------------------------------------------------
  if result == "-d":
    ok=1
    print("\n",end='')
    h = "HTTP Code"   ; print("%s : %s" % ( (bcolors.GREEN+h+bcolors.ENDC + " " * (m_s - len(h)) , r.status_code)))
    h = "HTTP Reason" ; print("%s : %s" % ( (bcolors.GREEN+h+bcolors.ENDC + " " * (m_s - len(h)) , r.reason)))
    for h in  r.headers:
      print("%s : %s" % (bcolors.GREEN + h + bcolors.ENDC + " " * (m_s - len(h)),r.headers[h]) )
    h = "Title"
    print("%s : %s" % (bcolors.GREEN+h+bcolors.ENDC + " " * (m_s - len(h)),get_title(r.text)) )
    h = "Mime-Type"
    print("%s : %s" % (bcolors.GREEN+h+bcolors.ENDC + " " * (m_s - len(h)),get_mime(r.text)) )
    print("\n",end='')

  #--- code ------------------------------------------------------------------------------------------------------------
  if result == "-c":
    ok=1
    print(r.status_code)

  #--- reason ----------------------------------------------------------------------------------------------------------
  if result == "-r":
    ok=1
    print(r.reason)

  #--- text (html) ------------------------------------------------------------------------------------------------------
  if result == "-t":
    ok=1
    r = get(url)
    print(r.text)


  if result == "-T":
    ok=1
    t = get_title(r.text)
    print(t)


  if ok == 0:
    usage()

