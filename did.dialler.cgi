#!/bin/bash

tmpdir=`ls -l ./tmp|awk -F\> '{print $2}'`
[ ! -d $tmpdir ] && mkdir $tmpdir && chmod ugo+rwx $tmpdir


/bin/echo "Content-type: text/html"
x=$(pwd)
/bin/echo ""

cat header.html
source logger.src

cat << EOF
<script language=javascript>mainpage=1;</script>

<!-- readme section $x -->
<table width="100%">
<tr>
  <td align="center">
  <form>
  <input type="button" value="Read Me Stuff, You really should read this at least once" onclick="window.open('./readme.cgi','_blank')" />
  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
  <input type="button" value="Some scenario examples and what to look for" onclick="window.open('./scenariohelp.cgi','_blank')" />
  </form>
  </td>
</tr>
</table>

<!-- system status frame -->
<div style="text-align:center;">
EOF
bash systemstatus.cgi imbed

cat << EOF
</div><hr />

<!-- did ticket section -->
<b>Your Ticket</b>
<br /><br />
<form action="./ticketprocessor.cgi" method="post" target="ticketprocessor" id="ticketform" name="ticketform">
<input type="checkbox" name="optionVD"  value="VD"  checked  /> Show DialOut records <br />
<input type="checkbox" name="optionTT"  value="TT"  checked  /> Show Routing &amp; Termination records <br />
<input type="checkbox" name="optionMR2" value="true" checked /> Show Version 2 machine readable summary records<br />
<input type="checkbox" name="optionTCP" value="true"         /> Force SIP INVITES through TCP<br />
<br />
Enter your list of 100 or less DIDs<br />
Enter as NPANXXXXXX each on its own line or space separated, you may add additional trace DIDs separate by a T, but no spaces. Eg. 4168011462<b>T</b>4162209911<br />
<textarea rows="10" name="DIDLIST"></textarea><br />
<br />
<input type="button" name="sub2" value="Submit, results will be loaded below" onclick="javascript: submitticketform();"></input>
</form>

<hr />

<!-- did ticket results frame -->
<b>Ticket Processor Results</b>
<iframe id='ticketprocessor' name="ticketprocessor" frameborder='0' class="if_inline" src="./ticketprocessor.cgi" width="100%" height="600">
  <p>Your browser does not support iframes.</p>
  <p>This site cannot function without them.</p>
</iframe>
<br />

<!-- very cool dark, translucent canvas div, see canvas.js  -->
<div id="blanket" style="display:none;"></div>

<!-- very cool popup div, see canvas.js -->
<div id="popUpDiv" style="display:none;">
<a href="#" onclick="popup('popUpDiv')">Click Me To Close</a>
</div>

EOF

cat footer.html

