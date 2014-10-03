#!/usr/bin/env python

from optparse import OptionParser
import re
from os import execvp

parser = OptionParser()

parser.add_option('-i', action="store_const", dest='mode', const='i')
parser.add_option('-m', action="store_const", dest='mode', const='m')
parser.add_option('-s', action="store_const", dest='mode', const='s')
parser.add_option('-u', action="store_const", dest='mode', const='u')

parser.set_default('mode', 'd')

(opts, args) = parser.parse_args()

mode = opts.mode

multipliers = {
  "s": 1,  # seconds
  "m": 60,  # minutes
  "h": 60 * 60,  # hours
  "d": 60 * 60 * 24  # days
}

total = 0  # 0 seconds by default

for arg in args:
  for pattern in re.findall(r"(?:(-?\d+(?:\.\d+)?)([smhd])?)", arg):
    (dur, measure) = pattern
    total += float(dur) * multipliers[measure]

if (total == 0):
  print "Specify duration in format 3.1d 1h5m 2s"
else:
  print "Not sleeping for %d seconds" % total

  execvp("/usr/bin/caffeinate", ["caffeinate", "-%s" % mode, "-t", str(int(total))])