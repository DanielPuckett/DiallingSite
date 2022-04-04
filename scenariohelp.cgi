#!/bin/bash
/bin/echo "Content-type: text/html"
/bin/echo ""

cat header.html
source "logger.src"

cat << EOF
<b>Scenario Help</b><br />
<br />
The mission of this system is to test ported numbers. In order to do so we need to get the calls
off of the DCL network and then test that they route back in from the PSTN.  Essentially, if you
love the DID, set it free, if it comes back, it's yours, it it doesn't, it never was :)<br />
<br >
To get the calls off the network, we dial out each DID prefixed with a special routing code, 77766.
The code results in the Meta Switch stripping off the code and route the call out a Telus LD DAL
that is connected to the Primus Western CFS.<br />
<br />
<code>
DclEasternCFS:6473170010 776614162209911 04/03/22.14:28:00 - 14:28:09 - - 3012 0 N   0 - ORG OT A F 2345<br />
DclWesternCFS:6473170010 776614162209911 04/03/22.14:28:01 - 14:28:09 3012 0 7028 0 N   0 - TRN NA A F 2345<br />
PrimusWesternCFS:6473170010 4162209911 04/03/22.14:28:01 - 14:28:10 9122 0 7890 0 N   0 - TRN IL A F 9998<br />
</code>
<br />
We suppress the reporting of the first two legs of the DialOut as we route the call to the west and 
report only the call as it exits our network.<br />
<br />
If the call fails to be reported as reentering our network it may be due to a few reasons.<br />
<ul>
<li>The DID may not be ported to DCL.</li>
</i>The DID may be ported to DCL but one or more LECs may incorrectely have the DID in their system
as a local customer of theirs.</li>
<li>The DID did reeenter our network, but this tool failed to see the call record data.  It is good
practice to repeat a test on failure.</li>
</ul>
We report all call legs of the call as the call reenters our network.  In order to assist the user,
we catagorize the records as <b>DialOut</b> (the last leg as the call leaves on the Telus LD DAL, 
<b>Routing</b> as the call is switched through our DCL and Primus CFSs, and finally as <b>Termination
</b> as we attempt to terminate the call on a customer facility.<br />
<br />
<code>
1 :: 2022-04-03 09:43:25 4163242803<br />
&nbsp;&nbsp;DialOut PrimusEasternCFS:6473170010 4163242803 04/03/22.14:43:26 - 14:43:35 9122 0 7890 0 N 0 - TRN IL A F 9998<br />
&nbsp;&nbsp;Routing PrimusEasternCFS:6473170010 4163242803 04/03/22.14:43:28 - 14:43:36 9900 0 9122 0 N 0 - TRN IL A F -<br />
&nbsp;&nbsp;Termination DclWesternCFS:6473170010 4163242803 04/03/22.14:43:28 - 14:43:36 7025 0 - - N 0 - TER LO A F -<br />
&nbsp;&nbsp;MRR2, 4163242803, 1, 1, 1,<br />
</code>
<br />

Sometimes there will not be any Routing records, only the DialOut and Termination records, This is the 
case when the DID is served from the same Meta CFS that received the call from PSTN.  Sometimes there will
be multiple Routing records.  This is the case when the call needs to be routed through multiple Meta CFS.
Note that the order these records are printed are simply the order we found them, it does not indicate
the true path of the call.<br />
<br />
Mutiple Termination records are usually an indication of an error in our provisioning. These will
typically be accommpanied with error codes at the end of each record.  To assist the user, this tool
looks up the errors and attached plain text descriptions of the error.<br />
<br />
Regardless of the inclusion of Termination records without error, or even Termination records with an 
error that suggests an error on the customer's side like an error 027 (Destination out of order), this
is just a tool, and the users need to apply their skills, their experience and understanding to problems
recported by customers.<br />
<br />
An error 027 could very well be that a customer has not provisioned a DID on their equipment, but it also
could be that we are sending the call on the wrong customer facing facility, or perhaps they have a SIP
trunk down becasue we have a problem with a proxy or SBC.<br />
<br />
Use this tool to augment your skills, not replace them.<br />
<br />
Daniel 

EOF

cat footer.html
