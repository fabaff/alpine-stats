#!/env/python
# This simple script is collecting details about the packages in Alpine Linux.
#
# This script can be used to do stuff for the Trivia page.
# http://wiki.alpinelinux.org/wiki/Trivia
# 
# Licensed under GPLv2
# 
# Copyright (c) 2012-2018 Fabian Affolter <fabian at affolter-engineering.ch>

import os
import sys
import urllib2
import tarfile

def grab(url):
    """Create the data."""
    data = urllib2.urlopen(url)
    localFile = open('APKINDEX.tar.gz', 'w')
    localFile.write(data.read())
    localFile.close()

    tar = tarfile.open('APKINDEX.tar.gz')
    tar.extract('APKINDEX', path=".")
    tar.close()

    countStd = 0
    countDev = 0
    countDoc = 0
    countLib = 0
    countCom = 0
    total = 0

    fobj = open('APKINDEX', 'r')
    for line in fobj:
        if line.startswith('P'):
            if line[len(line)-4:len(line)-1] == 'dev':
                countDev = countDev + 1
            elif line[len(line)-4:len(line)-1] == 'doc':
                countDoc = countDoc + 1
            elif line[len(line)-5:len(line)-1] == 'libs':
                countLib = countLib + 1
            else:
                countStd = countStd + 1
    fobj.close()
    total = countStd + countDev + countDoc + countLib 
    numbers = (countStd, countDev, countDoc, countLib, total)
    return numbers

def clean():
    """Clean up after a run."""
    os.remove('APKINDEX.tar.gz')
    os.remove('APKINDEX')

def main(argv):
    """The main part of the script."""
    url = 'http://nl.alpinelinux.org/alpine/v%s/main/x86_64/APKINDEX.tar.gz' % argv
    #url = 'http://ancient.alpinelinux.org/alpine/v%s/apks/INDEX.md5.gz' % argv
    numbers = grab(url)

    print "| '''%s'''\n| %s\n| %s\n| %s\n| %s\n| %s\n|-" \
        % (argv, numbers[4], numbers[0], numbers[1], numbers[2], numbers[3])
    
    clean()

if __name__ == "__main__":
    main(sys.argv[1])
