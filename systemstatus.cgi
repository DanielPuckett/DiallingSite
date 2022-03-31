#!/bin/bash

source logger.src

makeSectionDetail() {
  # ---------------------------------
  # Arg 1 is DIV id tag
  # Five <td> html sections
  # ---------------------------------
  echo "    <td><div id=\"s${1}p\" ></div></td>"
  echo "    <td><div id=\"s${1}s\" ></div></td>"
  echo "    <td><div id=\"s${1}r\" ></div></td>"
  echo "    <td><div id=\"s${1}b1\"></div></td>"
  echo "    <td><div id=\"s${1}b2\"></div></td>"
}

cat << EOF
<form name="statusform">
<table border="0" width="100%">
<tr>
  <td></td>
  <td>Host Machine</td>
  <td colspan="7"><div id="host">
    <a onclick="javascript:popup('popUpDiv'); parent.document.getElementById('popUpDiv').innerHTML = '<iframe name=\'test\' frameborder=\'0\' class=\'if_popup\' height=\'100%\' marginheight=\'0\' scrolling=\'no\' width=\'100%\' src=\'./sessioncontrol.cgi\'></iframe>';">
    <b><u><i>@<i></u><b></a>
  </div></td>
  <td colspan="3" align="right">
    <INPUT name="autobutton" type="BUTTON" value="Auto-Refresh"
     onClick="javascript: if(document.statusform.autobutton.value=='Auto-Refresh') {autoTimer(0,'set',5,'./systemstatus.xml.cgi', 'ajaxstatus',''); document.statusform.autobutton.value='Stop-Refresh';}else{autoTimer(0,'stop',0,'./systemstatus.xml.cgi', 'ajaxstatus',''); document.statusform.autobutton.value='Auto-Refresh';};">
  </td>
</tr>
<tr>
    <td rowspan="9"><div style="border: solid 0 #3366CC; border-left-width:2px; padding-left:0.5ex">&nbsp;<br />
      &nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />
    </div></td>
    <td><b>Process</b></td>
    <td><b>Running Since</b></td>
    <td><b>Last Results</b></td>
    <td colspan="2"><b>Controls</b></td>
    <td rowspan="9"><div style="border: solid 0 #3366CC; border-left-width:2px; padding-left:0.5ex">&nbsp;<br />
      &nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />
    </div></td>
    <td><b>Record Loggers</b></td>
    <td><b>Running Since</b></td>
    <td><b>Last Results</b></td>
    <td colspan="2"><b>Controls</b></td>
    <td rowspan="9"><div style="border: solid 0 #3366CC; border-left-width:2px; padding-left:0.5ex">&nbsp;<br />
      &nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />&nbsp;<br />
    </div></td>
</tr>
<tr>
`makeSectionDetail  1`
`makeSectionDetail  8`
</tr>
<tr>
`makeSectionDetail  2`
`makeSectionDetail  9`
</tr>
<tr>
`makeSectionDetail  3`
`makeSectionDetail 10`
</tr>
<tr>
`makeSectionDetail  4`
`makeSectionDetail 11`
</tr>
<tr>
`makeSectionDetail  5`
`makeSectionDetail 12`
</tr>
<tr>
`makeSectionDetail  6`
`makeSectionDetail 13`
</tr>
<tr>
`makeSectionDetail  7`
`makeSectionDetail 14`
</tr>
<tr class="ajaxstatus"><td colspan="5" align="right"><div id="debug">autorefresh is off&nbsp;&nbsp;&nbsp;&nbsp;</div></td>
                       <td colspan="2" align="left"><div id="ajaxstatus">ajax: unitialized</div></td>
                       <td colspan="3" align="right"><div id="ctrl">ctrl: idle</div></td>
</tr>
</table>
</form>
EOF

