#!/bin/bash

source cgiparser.src
cgi_getvars BOTH ALL

www=www-data

source logger.src

USER=`ls -l ./|grep tmp\ -|awk '{print $3}'`

# First process any control arguments
# -----------------------------------
processcontrolresult="";
if [ "x$A" != "x" ]||[ "x$P" != "x" ]; then
  source "processcontrol.src"
  processcontrolresult=`processcontrol`;
fi

function makeButton() {
  # ---------------------------------
  # Arg 1 Button Caption
  # Arg 2 START or STOP
  # Arg 3 PROCESSNAME
  # button html and script
  # ---------------------------------
cat << EOF
<input type="button" value="$1" onclick="javascript:autoTimer(0,'now',0,'./systemstatus.xml.cgi', 'ajaxstatus', 'A=${2}&P=${3}');" /> 
EOF
}

function printRunningTime_www() {
  # ---------------------------------
  # Arg 1 PID
  # Exit Code 0 and "Day MMM DD 24:MM:SS"
  # Exit Code 1 and "Not Running"
  # If multiple match, first returned
  # ---------------------------------
  [ "x$1" == "x" ] && echo "Not Running" && return 1
  local starttime=`ps -p $1 -o lstart|grep -v STARTED|colrm 20|colrm 1 4|tail -n 1`
  [ "x$starttime" == "x" ] && echo "Not Running" && return 1
  echo "$starttime" && return 0
}

function getPID() {
  # ---------------------------------
  # Arg 1 Grep -E string to Find PID
  # Exit Code 0 and echo PID
  # Exit Code 1 and no echo
  # If multiple match, first returned
  # ---------------------------------
  local pid=`ps -U $www -o pid,command|grep -E "$1"|grep echo\ $USER|awk '{print $1}'|head -n 1`
  [ "x$pid" != "x" ] && echo $pid && return 0
  return 1
}

function makeSectionDetail() {
  # ---------------------------------
  # Arg 1 is DIV id tag
  # Arg 2 is Measure Type
  #       0=Count of Calls in Log
  #       1=Date of Log
  #       2=Ticket Status
  # Arg 3 Section Label
  # Arg 4 Grep -E String to Find PID
  # Arg 5 Log File
  # Arg 6 ProcessControl ID
  # Four <td> html sections
  # ---------------------------------
  local zz=""
  local yy=""
  #local xx="`makeButton Start START $6`"
  local xx=""
  local pid=`getPID "$4"`

if [ "x$1" == "x1" ]; then
  xx="`makeButton Start START $6`"
else
  xx="Auto-Starts"
fi

count=$(cat $5|wc -l)
count=$(( $count - 1 ))

  if [ "x$pid" != "x" ]; then
    case $2 in
      0) zz="`grep -E "state=CALLING" $5|wc -l` test calls";;
      1) zz="`ls -ltr $5|awk '{print $6" "$7" "$8}'`";;
      2) zz="`[ ! -s $5.working ] && /bin/echo "Idle"``[ -s $5.working ] && /bin/echo "Processing $count DIDs"`";;
      *) zz="unknown method";;
    esac

if [ "x$1" == "x1" ]; then
    xx="`makeButton Restart START $6`"
    yy="`makeButton Stop STOP $6`"
else
    xx="Auto-Starts"
    yy=""
fi

  fi
  [ "x$zz" == "x" ] && zz="&nbsp;";
  [ "x$yy" == "x" ] && yy="&nbsp;";
  [ "x$xx" == "x" ] && xx="&nbsp;";
cat << EOF
  <statusrow>
    <processname div="s${1}p"  enc="html"><![CDATA[$3]]></processname>
    <starttime   div="s${1}s"  enc="html"><![CDATA[`printRunningTime_www $pid`]]></starttime>
    <results     div="s${1}r"  enc="html"><![CDATA[$zz]]></results>
    <button      div="s${1}b1" enc="html"><![CDATA[$xx]]></button>
    <button      div="s${1}b2" enc="html"><![CDATA[$yy]]></button>
  </statusrow>
EOF
}

cat << EOF
Content-type: text/xml

<?xml version="1.0" encoding="ISO-8859-1"?>
<statusrows>
<processcontrol div="ctrl" enc="html"><![CDATA[$processcontrolresult]]></processcontrol>
<hostinfo       div="host" enc="html"><![CDATA[Current time `uptime`]]></hostinfo>
`makeSectionDetail  1 2 "Dialling Server" "DiallingServer.sh" ./tmp/did.ticket DIALLINGSERVER`
`makeSectionDetail  8 1 "MetaSwitches" idrsa ./tmp/did.CRAFTS CRAFTRECORDS`
`makeSectionDetail  2 0 "SIP Phone 1" "runVSSP.sh\ [1]" ./tmp/sip.out.1 PHONE1`
`makeSectionDetail  3 0 "SIP Phone 2" "runVSSP.sh\ [2]" ./tmp/sip.out.2 PHONE2`
`makeSectionDetail  4 0 "SIP Phone 3" "runVSSP.sh\ [3]" ./tmp/sip.out.3 PHONE3`
`makeSectionDetail  5 0 "SIP Phone 4" "runVSSP.sh\ [4]" ./tmp/sip.out.4 PHONE4`
`makeSectionDetail  6 0 "SIP Phone 5" "runVSSP.sh\ [5]" ./tmp/sip.out.5 PHONE5`
`makeSectionDetail  7 0 "SIP Phone 6" "runVSSP.sh\ [6]" ./tmp/sip.out.6 PHONE6`
</statusrows>
EOF

#`makeSectionDetail 10 1 "Genband" Get_csdr.inbound ./tmp/did.INCSDR CSDRRECORDSIN`
#`makeSectionDetail  9 1 "MetaSwitches" Get_craft.inbound ./tmp/did.INCRAFT CRAFTRECORDSIN`
# `makeSectionDetail 10 1 "Montreal Astx" GetAsteriskMontreal ./tmp/did.ASM ASX_MONTREAL`
# `makeSectionDetail 11 1 "Toronto Astx" GetAsteriskToronto ./tmp/did.AST ASX_TORONTO`
# `makeSectionDetail 12 1 "ThunderBay Astx" GetAsteriskThunderBay ./tmp/did.ASB ASX_THUNDERBAY`
# `makeSectionDetail 13 1 "Vancouver Astx" GetAsteriskVancouver ./tmp/did.ASV ASX_VANCOUVER`

