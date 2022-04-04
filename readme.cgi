#!/bin/sh
/bin/echo "Content-type: text/html"
/bin/echo ""

cat header.html

cat << EOF
<b>ReadMe</b><br />
<br />
It must be first noted that was and is still a bit of an experimental website.  It is currently
under development and is being moved to fully supported IS project. This project originally 
started as a simple call generator that took a single file of DIDs as an argument.  It is only 
when our Porting Group staff needed an efficient way to test ports and provisioning to ensure a
superior and "Awesome Sauce" service to our customers that we realized we had a solution or at 
least the building blocks of a web front end for that original call generator.<br /> 
<br />
The first system was very close to what we have today: a main web page (standard iframe html via
cgi bash script) and about a dozen and a half or so other bash (GNU Bourne Again SHell) scripts,
one Apple script and up to four X-Lite soft phones that ran on a Mac desktop.<br />
<br />
Over the course of the years the X-Lite soft phones were replaced with a command line soft phone
written one Sunday AM based on PJSip libraries and much of the website moved to AJAX data pulls 
by the web browser, but the site continued to be ran from a Mac Mini sitting in the Toronto IT 
room.<br />
<br />
<b><i>New!</i></b> As of the April 1 2022 the system is ran on a Linux Docker container 
environment. The code was fairly easy to port from Mac OSX to Linux as they are very close cousins.  
Really the only differences were in the arguments and output of a few command line utilities, 
notably ps and date and how carriage returns are treated when using the IFS variable to separate
input data.<br />
<br />
Switching to Docker is huge!  This provides for extremely fast build of a new instance to run the
system.  A developer could checkout the code for the Docker container and build a fully operating 
DID Testing Dialler in 3 minutes in his own Docker host.<br />
<br />
If you don't know what Docker is, I suggest spending a few minutes reading about it, but the highly
abbreviated description is it is a virtual container to run primarily web applications.  It is 
different from a virtual machine in that all containers on the Docker host are running the same 
kernel, using the same memory and disks, but the container is essentially chrooted in its own small
part of the filing system and limited on what resources it may use, and is also provided with its own
network layer.  Way less overhead than a true VM and also a fraction of the time to spin up a fresh
instance. Hugely advantageous when needing a separate enviroment with different libraries and dev
tools for different applications.  If you do web application development, then Docker can be your 
best friend.<br />
<br />
The main files and operations of the site are:
<ul>
<li>did.dialler.cgi --The main web page, provides for the collection of user ticket data and 
manages the posting of that data to the ticketprocessor.cgi.  This page also serves to display 
readme and diagnostic pages.<br /><br /></li>

<li>systemstatus.cgi --cgi shell script that creates the page portion that will accept the updates
from the Ajax routines. This is the background process info for the Dialling Server, soft phones, 
and record logger(s).<br /><br /></li>

<li>systemstatus.xml.cgi --cgi shell script that creates the Ajax XML encoded system status data. 
When Auto refresh is enabled, this page is called every few seconds.
<br /><br /></li>

<li>processcontrol.cgi --cgi shell script that will fullfill the {Restart} of process requests 
from the systemstatus page or from the Dialling Server when it is processing tickets. Starts and 
Stops Dialling Server, softphones (runVSSP.sh), and record logger connections to MtlXfB01 (xrecords
repository).
<br /><br /></li>

<li>ticketprocessor.cgi --cgi shell script that creates the work ticket of DIDs, waits on the 
Dialling Server, and searches through local call record logs that are created by some local bash 
scripts (described below) for call results as specified by your selections in your ticket.<br />
<br /></li>

<li>DiallingServer.sh and xfileread.bash --Shell scripts that wait until a work file of DIDs is 
created, then DiallingServer spawns instances of soft phones and record logger(s) required to process
the ticket, and spawns an instance of xfileread.bash to process the ticket, distributing the calls 
across the soft phones.  Once all DIDs have been dialled and the results acquired, the soft phones
and record logger(s) are destroyed.
<br /><br /></li></ul>

Additionally, there are many files in /var/www/DiallingSite (main website), /var/www/.ssh &amp; 
.sip (credentials), /opt/VSSP-Softphone (softphone source and binary), /opt/DiallingServer (ticket
dial processing) that support these operations.<br />
<br />
Daniel

EOF

cat footer.html
