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

def handle_disk(name, fd):
	fn = '/sys/class/block/{0}/queue/rotational'.format(name)
	try:
		f = open(fn, 'r')
	except OSError as e:
		if e.errno != errno.ENOENT:
			raise
		print('Error, maybe disk was immediately removed.')
		print(e)
		return
	with f:
		try:
			data = f.read()
		except OSError as e:
			# Haven't tested what errno's to expect.
			print('Error, maybe disk was immediately removed.')
			print(e)
			return

	rotational = int(data)
	if rotational == 0:
		print('Skipping non-rotational drive {0}'.format(disk))

	print('{0}: set APM to max performance'.format(disk))
	rc = subprocess.call(('hdparm', '-q', '-B', '254', '/dev/fd/0'),
	                     stdin=fd)
	if rc != 0:
		print('Failed with exit status {0}'.format(rc))

# Iterate SCSI / SAT / IDE drives (but not partitions thereof)
disk_iter = (p.name for p in Path('/dev/').iterdir()
	     if (p.match('sd[a-z]*') or p.match('hd[a-z]*')) and
	        not p.match('*[0-9]'))

for disk in disk_iter:
	# If we work on an open fd, it can't be replaced half-way through.
	# (it can just be closed by something like sys_revoke()).
	disk_path = '/dev/' + disk

	try:
		# This matches hdparm.  O_RDONLY works, and avoids triggering
		# rescan by udev (inotify).  O_NONBLOCK seems to be used to
		# avoid requesting the equivalent of closing a CD tray.
		disk_fd = os.open(disk_path, os.O_RDONLY | os.O_NONBLOCK)
	except OSError as e:
		if e.errno == errno.ENOENT:
			# hot-unplug
			continue
		raise

	try:
		handle_disk(disk, disk_fd)
	finally:
		os.close(disk_fd)

