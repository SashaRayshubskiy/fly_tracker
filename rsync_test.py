#!/usr/bin/env python

from subprocess import call
import os

#call(['rsync', '-rite', 'ssh', '/home/sasha/fly_trackball_data/fly26', 'ar296@orchestra:~/data/'])
#FNULL = open(os.devnull, 'w')
#call(['mail', '-s', 'Test subject from python2', 'druzhiche@gmail.com'], stdin=FNULL)
#call(['mail', '-s', 'Test subject from python2', 'druzhiche@gmail.com'])
#FNULL.close()

flyId = os.path.basename('/home/sasha/fly_trackball_data/fly26')
print flyId
