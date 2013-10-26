pyCrontab_Editor
================

A simple pygtk GUI to add script in crontab under Linux

This GUI helps you to add script under crontab in Linux.

<b>Usage</b><br />
Just run the script with root account and follow the GUI ;-)

<b>/etc/crontab example</b><br />
A basic crontab file look like this:
<pre>
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#
</pre>

After modified with Crontab Editor, it will look like the following

<pre>
SHELL=/bin/sh
PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin

# m h dom mon dow user	command
17 *	* * *	root    cd / && run-parts --report /etc/cron.hourly
25 6	* * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.daily )
47 6	* * 7	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.weekly )
52 6	1 * *	root	test -x /usr/sbin/anacron || ( cd / && run-parts --report /etc/cron.monthly )
#

# Inserted with Crontab Editor
50  14  *  *  *    root    /usr/local/bin/checkbin.sh
</pre>

Don't worry about original /etc/crontab it will backupped in /etc/crontab.bak

Enjoy!
