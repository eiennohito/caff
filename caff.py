#!/usr/bin/env python

from optparse import OptionParser, Option, OptionValueError
import re
from os import execvp
from datetime import datetime, timedelta
from copy import copy

def check_int(s):
    try:
        return int(s)
    except TypeError:
        return 0

def check_time(option, opt, value):
    m = re.match(r"(\d\d):(\d\d)(?::(\d\d))?", value)
    if m is None:
        raise OptionValueError("")
    else:
        return map(check_int, m.groups())

class TimeOption(Option):
    TYPES = Option.TYPES + ("time",)
    TYPE_CHECKER = copy(Option.TYPE_CHECKER)
    TYPE_CHECKER["time"] = check_time

parser = OptionParser(option_class=TimeOption)
parser.add_option('-i', action="store_const", dest='mode', const='i')
parser.add_option('-m', action="store_const", dest='mode', const='m')
parser.add_option('-s', action="store_const", dest='mode', const='s')
parser.add_option('-u', action="store_const", dest='mode', const='u')
parser.add_option('-t', type="time", dest="till")

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
d = datetime.now()
if opts.till is None:
    for arg in args:
      for pattern in re.findall(r"(?:(-?\d+(?:\.\d+)?)([smhd])?)", arg):
        (dur, measure) = pattern
        total += float(dur) * multipliers[measure]
else:
   time = opts.till
   d2 = d.replace(hour=time[0], minute=time[1], second=time[2])
   if d2 < d:
       d2 = d2 + timedelta(days=1)
   total = (d2 - d).total_seconds()


if (total == 0):
    print "Specify duration in format 3.1d 1h5m 2s.\nOtherwise you can use -t 12:30[:15] format to sleep until 12:30.\nUtil will use 24h format and nearest time in the future."
else:
  end = datetime.now() + timedelta(seconds = total)
  print "Not sleeping for %d seconds, until %s" % (total, end.strftime("%c"))

  execvp("/usr/bin/caffeinate", ["caffeinate", "-%s" % mode, "-t", str(int(total))])
