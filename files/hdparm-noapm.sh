#!/bin/bash
#
# Disable automatic head-parking on "green" hard drives (mainly Western 
# Digital).  This helps to avoid exceeding the design LOAD_CYCLE_COUNT with
# frequently-written filesystems like /var/log.
#
# This script effectively disables power saving on *all* hard drives.

set -e


handle_disk() {
	local DEV="$1"
	if [ "$(cat "/sys/class/block/$DEV/queue/rotational")" = "0" ]; then
		echo "$DEV: skipping non-rotating drive"
		return
	fi
	if ! hdparm -B 254 "/dev/$DEV"; then
		echo "$DEV: hdparm failed with exit status $?"
	fi
}

# Iterate SCSI / SAT / IDE drives
cd /dev/
for i in sd[a-z]* hd[a-z]*; do
	case "$i" in
	*[0-9])
		# ignore partitions
	;;
	[sh]d[a-z]*)
		handle_disk "$i"
	;;
	esac
done
