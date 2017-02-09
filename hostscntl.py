#!/usr/bin/env python
import requests
import sys
import shutil
import os

guide = '''NAME
\thosts-tool - The hosts file controller

COMMANDS
\tadd [url]
\t\tadd a new hosts source
\tbackup [path]
\t\tbackup current hosts file
\tremove [url]
\t\tremove a hosts source
\tupdate
\t\tupdate hosts according to sources
'''

configPath = os.path.join(os.getenv("HOME"), '.hostscntl')
hostsPath = '/etc/hosts'

def getCommand():
  if len(sys.argv) < 2:
    print guide
  else:
    cmd = sys.argv[1]
    if cmd == 'add':
      addSource()
    elif cmd == 'backup':
      backupHosts()
    elif cmd == 'remove':
      removeSource()
    elif cmd == 'update':
      updateHosts()
    else:
      print 'unknown command: %s' % cmd

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

def backupHosts():
  if len(sys.argv) < 3:
    print 'invalid command'
    return

  backupPath = sys.argv[2]

  shutil.copy(hostsPath, backupPath)

def removeSource():
  if len(sys.argv) < 3:
    print 'invalid command'
    return

  sourceToDel = sys.argv[2] + '\n'

  with open(configPath, 'r+') as configFile:
    sources = configFile.readlines()
    configFile.seek(0)
    for l in sources:
      if l != sourceToDel:
          configFile.write(l)
    configFile.truncate()

if __name__ == '__main__':
  getCommand()
