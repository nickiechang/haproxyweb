#
# Regular cron jobs for the haproxyweb package
#
0 4	* * *	root	[ -x /usr/bin/haproxyweb_maintenance ] && /usr/bin/haproxyweb_maintenance
