# hdparm-noapm #

Disable power saving on all hard drives.
Solid-state drives are excluded.

This should disable automatic head-parking on hard drives like
WD Green.  It helps to avoid exceeding the design LOAD_CYCLE_COUNT,
when filesystems are frequently written to like /var/log.

I made sure the setting is applied after resume from suspend, as well
as at boot time and when the role is first run.


## Status

Hotplugged drives are not supported.

I would be interested to see code which can be configured with a list of
drives to include (or exclude?).  However I haven't needed it yet, and
ideally it would be based on filesystems and support mdraid (sysfs), btrfs
(detect same UUID)...


## Requirements

This role should work on any machine with systemd.


## License

This role is licensed GPLv3, please open an issue if this creates any problem.
