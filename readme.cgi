#!/bin/sh
/bin/echo "Content-type: text/html"
/bin/echo ""

cat header.html

cat << EOF
<b>ReadMe</b><br />
<br />
It must be first noted that this is an experimental website.  It is currently under development but it is a low priority project.  This project originally started as a simple call generator that took a single file of DIDs as an argument.  It is only when certain Toronto ThinkTel staff needed to test dial many DIDs manually on a MBS phone and the accompanying beep beep beep of the touch tones started eating away at my brain even through a closed door, that I realized we had a solution or at least the building blocks of a web front end for that original call generator.<br /> 
<br />
The main web page (standard iframe html via cgi bash script) and about a dozen and a half or so other bash (GNU Bourne Again SHell) scripts, <s>one Apple script and up to four X-Lite SoftPhones</s> <b>and now Ajax methodology in the system status section</b> reside on a MAC Mini in an unused cubicle in the Toronto office as well as a scaterring of machines around the country.<br />
<br />
<b><i>New!</i></b> The System Status section was a reloadable iFrame section, that would refresh every 60 seconds.  This resulted in the typical screen re-render issues of reloading a page.  I had been vaguely aware of how Ajax worked, which is not a product but rather a design and coding methodolgy.  Ajax is simply using some Javascript to pull (any stories about pushed data are misunderstandings) XML encoded data from a web server And Asynchronously update just the relevent parts of the web page.  Means loading the page once, any after that, just the changes.  Take the capital letters from the Javascript, Async.., XML, and And, rearrange to make AJAX.  Quite often a website will use libraries of Ajax routines that run on PHP or Perl on the server and Javascript on the client, instead I wrote the server side in bash scripting and similarly, some home grown Javascript to handle the client side.<br />
<br />
<b><i>New!</i></b> The X-Lite SoftPhones really bugged me.  Because they had no scripting interface and they are a graphical application, they were hanging out on the desktop of that MAC Mini, and rendered it quite unusable.  So...  I wrote a console application SIP softphone.  On Sunday moring I downloaded the PJ SIP opensource project, great set of libraries.  And then I wrote and tested and wrote and tested, and Eureka! we now have a in-house developed softphone very suitable for our needs.  Written in C language and compiled using GCC 4.0.1, the softphone would actually fit on a floppy.  If we had one :)<br />
<br />
The SoftPhones are configured with one of <s>two</s> <b>three</b> SIP accounts on the Ottawa GenBand switch, that are specially provisioned in the Ottawa SCP #2 to always force their calls out a Bell LD DAL.  This ensures that all calls are handled by another LEC that will DIP the LNP (Local Number Portability) database.  If the dialled DID is a native Distributel number or has been ported to Distributel the call will re-enter our network either through a Distributel Genband in Ontario or Quebec; and through the ThinkTel MetaSwitch in Alberta or B.C. 

<ul>
<li>did.dialler.cgi --The main web page, provides for the collection of user ticket data and manages the posting of that data to the ticketprocessor.cgi.  This page also serves to display readme and diagnostic pages.<br /><br /></li>

<li>systemstatus.cgi --cgi shell script that creates the page portion that will accept the updates from the Ajax routines.  Previously this script also provided the system status data, now just the framework. Presents certain statuses and conditions that may be helpful in determining readiness of system to deliver dialling results.<br /><br /></li>

<li>systemstatus.xml.cgi --cgi shell script that creates the Ajax XML encoded system status data.<br /><br /></li>

<li>processcontrol.cgi --cgi shell script that will fullfill the {Restart} of process requests from the systemstatus page.  Currently under development.<br /><br /></li>

<li>ticketprocessor.cgi --cgi shell script that creates the work ticket of DIDs, waits on the DiallingServer, and searches through local call record logs that are created by some local bash scripts (described below) for call results as specified by your selections in your ticket.<br /><br /></li>

<li>DiallingServer.sh --Shell script that waits until a work file of DIDs is created, then spawns an instance of the AppleScript (xfileread.scpt) to process the file, distributing the calls across the SoftPhones.  Since the X-Lite SoftPhones don't have a scripting API (well, they do, but it only has one instruction), this script manipulates the mouse and literally 'clicks' and 'types' instructions to the SoftPhones. <b>ya ya ya, scratch all of that</b>, The new VerySmallSipPhones are controlled by a wrapping bash script that redirects the phone's stdin and stdout to the filing system and then watches for desired instructions on a third file.  The DiallingServer script now calls a xfileread.bash script that distributes the instructions by appending them to an input file for each softphone.  Too easy with a good design!<br /><br /></li>

<li><s>remote.readFromMetaSwitch.sh</s> <b>Functionality has been moved to processcontrol.cgi</b> --Shell script that maintains an ssh connection to the a DevBox in Edmonton that is connected to the Craft menu of the MetaSwitch and is gathering craft call records. The records are sent back to this MAC Mini for local logging.<br /><br /></li>

<li><s>remote.readFromXrecords.sh</s> <b>Functionality has been moved to processcontrol.cgi</b>  --Shell script that maintains an ssh connection to the Montreal xrecords server that receives all CSDR records from Distributel's 6 productions SCPs.  A Script runs on the remote side that sends calls placed by our four SoftPhones back to this Mac Mini for local logging.<br /><br /></li>

<li><s>remote.readFromAsteriskMontreal.sh</s> <b>Functionality has been moved to processcontrol.cgi</b>  --Shell script that maintains an ssh connection to a NOC netlog server and then spawns a connection to the Montreal Asterisk server and runs a remote script that sends all calls received from our four SoftPhones back to this MAC Mini for local logging.</li>

<li><s>remote.readFromAsteriskToronto.sh</s> <b>Functionality has been moved to processcontrol.cgi</b> --Shell script that maintains an ssh connection to a NOC netlog server and then spawns a connection to the Toronto Asterisk server and runs a remote script that sends all calls received from our four SoftPhones back to this MAC Mini for local logging.</li>

<li><s>remote.readFromAsteriskThunderBay.sh</s> <b>Functionality has been moved to processcontrol.cgi</b> --Shell script that maintains an ssh connection to a NOC netlog server and then spawns a connection to the Thunder Bay Asterisk server and runs a remote script that sends all calls received from our four SoftPhones back to this MAC Mini for local logging.</li>

<li><s>remote.readFromAsteriskCalgary.sh</s> <b>Functionality has been moved to processcontrol.cgi</b> --Shell script that maintains an ssh connection to a NOC netlog server and then spawns a connection to the Calgary Asterisk server and runs a remote script that sends all calls received from our four SoftPhones back to this MAC Mini for local logging.</li>
</ul>

Additionally, on the MAC Mini are several bash scripts that keep a close eye on all of the above processes to ensure that they keep running properly.  These are all in various development stages and some much more successful than others.  There are other scripts on the Edmonton dev box, the NOC netlog server, the Montreal xrecords server, and the individual Asterisk servers to keep this whole thing chugging along.  None of which would be possible without keeping a clear design that incorporates high cohesion and low coupling :)

EOF

cat footer.html

