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


def getSourceList():
  if not os.path.isfile(configPath):
    print 'warning: config file dont exists'
    return []
  
  try:
    with open(configPath, 'r') as configFile:
      sources = configFile.read().splitlines()
      return sources
  except Exception as err:
    print 'unknown error\n %s' % err
    return []


def updateHosts():
  sources = getSourceList()

  # dont overwrite origin hosts if sources is empty
  if len(sources) == 0:
    return

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

  sources = getSourceList()

  if source not in sources:
    with open(configPath, 'a') as configFile:
      configFile.write(source + '\n')
      print 'successfully add source %s' % source
  else:
    print 'source `%s` exists' % source

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
    hasRemove = False
    for l in sources:
      if l != sourceToDel:
        configFile.write(l)
      else:
        hasRemove = True
    configFile.truncate()

    if hasRemove:
      print 'remove `%s` successfully' % sys.argv[2]
    else:
      print 'source `%s` dont exists' % sys.argv[2]

if __name__ == '__main__':
  getCommand()
