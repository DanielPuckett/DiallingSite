#!/bin/bash
/bin/echo "Content-type: text/html"
/bin/echo ""

cat header.html
source "logger.src"

cat << EOF
<b>Scenario Help</b><br />
<br />
This section is still pretty much the same text from the first week of this project.  I promise that this will get better.<br />
<br />
<b>If DID is in Ontario or Quebec</b><br />
<u>Served by Distributel Montreal, Ottawa or Toronto Genband Switch</u><br />
Should have a VoIP dial out record and a Distributel Genband record<br />
<u>Served by ThinkTel Edmonton Switch</u><br />
Should have a VoIP dial out record, Distributel Genband record and a ThinkTel Metaswitch record<br />
<br />
<b>If DID is in Alberta or BC</b><br />
<u>Served by Distributel Montreal, Ottawa or Toronto Genband Switch</u><br />
Should have a VoIP dial out record and a ThinkTel Metaswitch record and a Distributel Genband record<br />
<u>Served by ThinkTel Edmonton Switch</u><br />
Should have a VoIP dial out record and a ThinkTel Metaswitch record<br />
<br />
<b>If the DID is served from an Asterisk Server</b><br />
Should have a VoIP dial out record<br />
May have a Distributel Genband record if ported to Distributel and in Ontario or Quebec<br />
May have a ThinkTel MetaSwitch record if ported to Distributel and in Alberta or British Columbia<br />
Select 3Web Montreal Asterisk server to show inbound Asterisk records<br />
Select 3Web Toronto Asterisk server to show inbound Asterisk records<br />
Select 3Web Thunder Bay Asterisk server to show inbound Asterisk records<br />
Select 3Web Calgary Asterisk server to show inbound Asterisk records<br />

EOF

cat footer.html

