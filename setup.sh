#!/bin/sh
chown www-data *
chmod u+r *
chmod u+rx *.cgi
ln -s /tmp ./tmp
