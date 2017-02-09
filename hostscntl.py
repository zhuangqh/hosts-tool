#!/usr/bin/env python
import requests
import sys
import os

guide = '''
update\tupdate hosts
add\tadd a source
'''

configPath = os.path.join(os.getenv("HOME"), '.hostscntl')
hostsPath = '/etc/hosts'

def getCommand():
  if len(sys.argv) < 2:
    print guide
  else:
    cmd = sys.argv[1]
    if cmd == 'update':
      updateHosts()
    elif cmd == 'add':
      addSource()
    else:
      print 'undefined command'
      print guide

def updateHosts():
  try:
    with open(configPath, 'r') as configFile:
      sources = configFile.read().splitlines()
      print sources
  except OSError as err:
    print 'no config file %s' % err

  hostsBuffer = ''

  for source in sources:
    try:
      hosts = requests.get(source)
      hostsBuffer += hosts.text
    except:
      print 'fail to update %s' % source

  # save new hosts
  try:
    with open(hostsPath, 'w') as hostsFile:
      hostsFile.write(hostsBuffer)
  except Exception as e:
    print 'fail to save hosts\n%s' % e

def addSource():
  if len(sys.argv) < 3:
    print 'invalid command'
    return

  source = sys.argv[2]

  try:
    with open(configPath, 'rw') as configFile:
      sources = configFile.read().splitlines()
      if source in sources:
        print 'source exists'
        return

    with open(configPath, 'a') as configFile:
      configFile.write(source + '\n')
      print 'successfully add source %s' % source
  except Exception as err:
    print 'cannot open config file:\n%s' % err

getCommand()
