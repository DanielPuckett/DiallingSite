#!/bin/sh
cd /var/www/DiallingSite
chown www-data *
chmod u+r *
chmod u+rx *.cgi
ln -s /tmp ./tmp
cp ApacheDiallerSite.conf /etc/apache2/sites-available/
rm /etc/apache2/sites-enabled/000-default.conf
ln -s /etc/apache2/sites-available/ApacheDiallerSite.conf /etc/apache2/sites-enabled/ApacheDiallerSite.conf
cd /var/www
mkdir .ssh
chown www-data .ssh
a2enmod cgid
# reload apache2
