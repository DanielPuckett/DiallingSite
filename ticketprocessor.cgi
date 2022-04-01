#!/bin/bash
echo "Content-type: text/html"
echo ""

source cgiparser.src
cgi_getvars BOTH ALL

#configfile=../DiallingServer/configuration

#function cfg() {
#   # Arg 1 is the Config Keyword
#   # Returns either blank string or key value
#   grep -E "^$1=" $configfile|sed s/[^=]*=//
#}


# ---------------------------------
# Build a DID string from POST vars
# ---------------------------------
DEFAULTDIDS=""
LF="
"
DIDEXPORTLIST=""

# Bug..  cr is not being treated as white space
DIDLISTO=$DIDLIST
DIDLIST=$(echo "$DIDLISTO"|tr '\r' ' ')

for i in $DIDLIST; do
  # clean out anything not number or T then change T to PIPE
  CLEANDID=`/bin/echo $i | /usr/bin/tr -cd "T0123456789" | /usr/bin/tr 'T' '|'`
  if [ "x$CLEANDID" != "x" ]; then
    match=`/bin/echo $DIDEXPORTLIST|/usr/bin/grep -c $CLEANDID`
# match=0
    [ $match -eq 0 ] && DIDEXPORTLIST="${DIDEXPORTLIST}${CLEANDID}${LF}"
    [ $match -eq 0 ] && /bin/echo "Added $CLEANDID to DID Export List<br />"
    [ $match -ne 0 ] && /bin/echo "Did not add duplicate DID $CLEANDID<br />"
  fi
done

source "logger.src"

# ------------------------------------------------------------
# If we have a list, then put to ticket and let server do work
# ------------------------------------------------------------
if [ "x$DIDEXPORTLIST" == "x" ]; then
  /bin/echo "Nothing to do, idle."
fi

if [ "x$DIDEXPORTLIST" != "x" ]; then

  # ------------------------------------------------
  # Check if Dialling Server is Busy for someone else
  # ------------------------------------------------
  if [ -s ./tmp/did.ticket.working ]; then
    /bin/echo "<b>Cannot use Dialling Server -it is currently busy dialling for someone else.</b><br />"

  # -----------------------
  # Else, do work for us :)
  # -----------------------
  else

    # Give last running process time to read all of its call results.
    # Yep, it's a bug.  If this cgi starts too fast and the previous
    # Dialler instance just finished a large run of DIDs, the last
    # instance of the cgi might still be reading the call results.
    # I can fix it by using two process flags instead of one, or just
    # wait two seconds.  Hmmm.. to fix now or not..
    sleep 2

    # Create ticket settings
    /bin/echo "TCP=$optionTCP" > ./tmp/did.ticket.settings

    # Create ticket
    # And clear the call record file(s) of all previous ticket results
    /bin/echo "$DIDEXPORTLIST"  > ./tmp/did.ticket
    /bin/echo "reset by ticketprocessor.cgi" > ./tmp/did.CRAFTS

    # Wait for the Dialling server (running from ../DiallingServer directory) to pick up the ticket
    /bin/echo "Waiting for Dialling Server to Pickup Ticket<br /><br />"
    while [ ! -s ./tmp/did.ticket.working ]; do
      sleep 1
    done
    /bin/echo "Dialling Server picked up Ticket<br />"

    # Control vars
    current=1
    line=""
    lastline=""

    # Process some options from the web form
    if [ "x$optionMR2" == "xtrue" ];then
      /bin/echo "<br />Machine Readable records requested, building template...<br />"
      MRrecord2="MRR2, Telephone Number"
      [ "x$optionVD" == "xVD" ]   && MRrecord2="$MRrecord2, Dialout Record Count"
      [ "x$optionTT" == "xTT" ]   && MRrecord2="$MRrecord2, Routing Record Count, Termination Record Count, Record Errcode"
      /bin/echo "<br /><b>MR2 record=</b> $MRrecord2<br /><br />"
    fi

    # For each DID dialed by the DiallingServer.. (from its logs)
    while [ "x$line" != "xCLOSED" ]; do
      line=`head -n $current ./tmp/did.events.log|tail -n 1`
      if [ "$lastline" != "$line" ] && [ "x$line" != "xCLOSED" ]; then
        
        /bin/echo "$current :: $line <br />"

        # DiallingServer & xfileread writes the call start time and the DID in the log file
        # HangupTime = Call starttime from log + 11 seconds call duration (set in xfileread.bash)
        hanguptime=`echo "$line"|colrm 20`
        hanguptime=`date -d "$hanguptime" +%s`
        let hanguptime=( $hanguptime + 11  )
        # ExpectedRecordDelay=Some calibrated time value
        expectedRecordDelay=5
        # ElapsedTime = difference between hangup and now(secno)
        let elapsedtime=( `date +%s` - $hanguptime )        
        # RequiredTime = ExpectedTimeDelay - ElaspdedTime
        let requiredtime=( $expectedRecordDelay - $elapsedtime )
        # Use Required Time to build a WaitString.        
        [ $requiredtime -le 0 ] && requiredtime=0 && WaitString="1 99" && SleepInteger=0
        #[ $requiredtime -gt 0 ] && let requiredtimeStringPosition=( $requiredtime * 2 ) && SleepInteger=1 && WaitString="`/bin/echo "1 2 3 4 5 6 7 8 9 0 1 2 3"|colrm $requiredtimeStringPosition` 99"
        sleep $requiredtime


        thisDID=`/bin/echo $line|/usr/bin/awk '{print $3}'|/usr/bin/tr -cd "|0123456789"`
        let current=($current + 1)
        lastline=$line

        VD=0; [ "x$optionVD" == "xVD" ] && VD=1
        TT=0; [ "x$optionTT" == "xTT" ] && TT=1
        MR2=0; [ "x$optionMR2" == "xtrue" ] && MR2=1 && MRrecord2=$thisDID

        vd_count=0
        tt_count=0
        tm_count=0

        tt_err="---"
        error=""

linefeed="
"

        # Dial Out
        if [ $VD -eq 1 ]; then
          vd_count=0
          ALLLINES=`/usr/bin/grep -a -E "${thisDID}" ./tmp/did.CRAFTS|grep -E "\ 9998"`
          oIFS=$IFS
          IFS=$linefeed
          for line in $ALLLINES; do
            let vd_count=( $vd_count + 1 )  
            /bin/echo "&nbsp;&nbsp;&nbsp;<b>DialOut</b> $line<br />"
          done
          IFS=$oIFS
        fi

        #Routing
        if [ $TT -eq 1 ]; then
          tt_count=0
          ALLLINES=`/usr/bin/grep -a -E "${thisDID}" ./tmp/did.CRAFTS|grep -vE "7766|\ 9998|TER|INT"`
          oIFS=$IFS
          IFS=$linefeed
          for line in $ALLLINES; do
            let tt_count=( $tt_count + 1 )  
            error=`/bin/echo "$line"|/usr/bin/awk '{print $10}'|/usr/bin/grep -c -E "N|B"`
            if [ "x$error" == "x0" ]; then
              tt_err=`/bin/echo "$line"|/usr/bin/awk '{print $10}'|head -n 1`
              #error=" <b>Error in MetaSwitch Provisioning</b>"
              error="<b>Error: $tt_err `grep -E "^$tt_err\ " MetaSwitchErrorCodes.txt|colrm 1 4`</b>"
              /bin/echo "&nbsp;&nbsp;&nbsp;<b>Routing</b> $line ${error}<br />"
            else
              error=""
              /bin/echo "&nbsp;&nbsp;&nbsp;<b>Routing</b> $line<br />"
            fi
          done
          IFS=$oIFS
        fi

        #TERM
        if [ $TT -eq 1 ]; then
          tm_count=0
          ALLLINES=`/usr/bin/grep -a -E "${thisDID}" ./tmp/did.CRAFTS| grep -E "\ TER|\ INT" | grep -vE "7766|\ 9998"`
          oIFS=$IFS
          IFS=$linefeed
          for line in $ALLLINES; do
            let tm_count=( $tm_count + 1 )
            error=`/bin/echo "$line"|/usr/bin/awk '{print $10}'|/usr/bin/grep -c -E "N|B"`
            if [ "x$error" == "x0" ]; then
              #error=" <b>Error in MetaSwitch Provisioning</b>"
              tt_err=`/bin/echo "$line"|/usr/bin/awk '{print $10}'|head -n 1`
              error="<b>Error: $tt_err `grep -E "^$tt_err\ " MetaSwitchErrorCodes.txt|colrm 1 4`</b>"
              [ "$tt_err" == "027" ] && error="<b>PBXError: $tt_err `grep -E "^$tt_err\ " MetaSwitchErrorCodes.txt|colrm 1 4`</b>"
              [ "$tt_err" != "027" ] && error="<b>Error: $tt_err `grep -E "^$tt_err\ " MetaSwitchErrorCodes.txt|colrm 1 4`</b>"
              /bin/echo "&nbsp;&nbsp;&nbsp;<b>Termination</b> $line ${error}<br />"
            else
              error=""
              /bin/echo "&nbsp;&nbsp;&nbsp;<b>Termination</b> $line<br />"
            fi
          done
          IFS=$oIFS
        fi

        # MRR
        if [ $MR2 -eq 1 ]; then
          [ "x$optionVD" == "xVD" ] && [ $VD -eq 0 ] && MRrecord2="$MRrecord2, $vd_count"
          [ "x$optionVD" == "xVD" ] && [ $VD -eq 1 ] && MRrecord2="$MRrecord2, $vd_count"
          [ "x$optionTT" == "xTT" ] && [ $TT -eq 0 ] && MRrecord2="$MRrecord2, $tt_count, $tm_count, $error"
          [ "x$optionTT" == "xTT" ] && [ $TT -eq 1 ] && MRrecord2="$MRrecord2, $tt_count, $tm_count, $error"
        fi

        [ $MR2 -eq 1 ] && /bin/echo "&nbsp;&nbsp;&nbsp;<b>MRR2</b>, $MRrecord2<br />"

      fi

    done

    /bin/echo "<br>"
    /bin/echo "Dialling Server has completed Ticket<br /><br />"
  fi
fi

