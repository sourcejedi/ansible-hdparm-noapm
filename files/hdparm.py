#!/bin/python3
#
# Disable automatic head-parking on "green" hard drives (mainly Western 
# Digital).  This helps to avoid exceeding the design LOAD_CYCLE_COUNT with
# frequently-written filesystems like /var/log.
#
# This script effectively disables power management on all hard drives.

from pathlib import Path
import os
import errno
import subprocess

def handle_disk(name):
	fn = '/sys/class/block/{0}/queue/rotational'.format(name)
	f = open(fn, 'r')
	with f:
			data = f.read()

	rotational = int(data)
	if rotational == 0:
		print('Skipping non-rotational drive {0}'.format(disk))

	print('{0}: set APM to max performance'.format(disk))

	rc = subprocess.call(('hdparm', '-q', '-B', '254', '/dev/'+name))

	if rc != 0:
		print('Failed with exit status {0}'.format(rc))

# FIXME: os.listdir()

# Iterate SCSI / SAT / IDE drives (but not partitions thereof)
disk_iter = (p.name for p in Path('/dev/').iterdir()
	     if (p.match('sd[a-z]*') or p.match('hd[a-z]*')) and
	        not p.match('*[0-9]'))

for disk in disk_iter:
	handle_disk(disk)
