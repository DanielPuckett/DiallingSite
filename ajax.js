autotimer_running=0;
autotimer_last_ran=0;
autotimer_interval=0;
autotimer_lock=0;
autotimer_thread=0;

function autoTimer(thread,cmd,interval,url,label,nowarg) {
  /* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *
   * cmd is 'set' requires interval, url and label.                                        *
   *     sets the inteval in seconds and starts 1 second interval checking routine         *
   *     replaces any previous interval set                                                *
   * cmd is 'auto' requires thread, url and label.                                         *
   *     is an internally generated call, do not use yourself.                             *
   *     is thread does not equal global thread value, exits.                              *
   *     if the tie since the last running of submitForm exceeds interval and              *
   *     submitForm is not currently running, the set timeout to run it in 1 second.       *
   * cmd is 'now' requires url and label                                                   *
   *     if submitForm is not currently running, the set timeout to run it in 1 second.    *
   *     if interval was set, this run counts as an early run of the next scheduled run.   *
   * cmd is 'stop' requires none.                                                          *
   *     stops any scheduled interval.                                                     *
   * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * */
  function roundNumber(num, dec) {
    var result = Math.round(num*Math.pow(10,dec))/Math.pow(10,dec);
    return result;
  };
  if((cmd=='auto')&&(thread!=autotimer_thread)) return;
  if (autotimer_lock) {
    setTimeout("autoTimer('"+cmd+"',"+refreshms+",'"+url+"','"+label+'","'+nowarg+"')",1000); return;}
  autotimer_lock=1;
  var myDate = new Date;
  var rightnow = myDate.getTime()/1000.0;
  autotimer_thread=rightnow;
  document.getElementById('debug').innerHTML=autotimer_running+" "+roundNumber((autotimer_interval-(autotimer_thread-autotimer_last_ran)),0)+" "+autotimer_interval+" "+roundNumber(autotimer_thread,0)+" "+cmd+" "+nowarg+" "+roundNumber(thread,0)+"&nbsp;&nbsp;&nbsp;";
  
  switch (cmd) {
    case 'stop': autotimer_interval=0;
                 break;
    case 'set' : autotimer_interval=interval;
                 setTimeout("autoTimer("+autotimer_thread+",'auto',0,'"+url+"','"+label+"');",1000);
                 break;
    case 'auto': if (!autotimer_interval) break;
                 setTimeout("autoTimer("+autotimer_thread+",'auto',0,'"+url+"','"+label+"');",1000);
                 if((autotimer_last_ran+autotimer_interval) < rightnow)
                   if(!autotimer_running) {
                     setTimeout("submitForm('"+url+"','"+label+"');",1050);
                     autotimer_running=1;
                   }
                 break;
    case 'now':  if(!autotimer_running) {
                   setTimeout("submitForm('"+url+"','"+label+"','"+nowarg+"');",1);
                   autotimer_running=1;
                 }
                 if (!autotimer_interval) break;
                 setTimeout("autoTimer("+autotimer_thread+",'auto',0,'"+url+"','"+label+"');",1000);
  }
  autotimer_lock=0;
};

function submitForm(url,n,args) { 
  var req = null;

  var myDate = new Date;
  autotimer_last_ran=myDate.getTime()/1000.0;
  autotimer_running=2;

  document.getElementById(n).innerHTML="Ajxax: Starting";
  if (window.XMLHttpRequest) {
    req = new XMLHttpRequest();
    if (req.overrideMimeType) {
      req.overrideMimeType('text/xml');
    }
  } else if (window.ActiveXObject) {
    try {
      req = new ActiveXObject("Msxml2.XMLHTTP");
    } catch (e)	{
      try {
        req = new ActiveXObject("Microsoft.XMLHTTP");
      } catch (e) {}
    }
  }
  req.onreadystatechange = function() { 
    document.getElementById(n).innerHTML="Ajax: Waiting on server ";
    if(req.readyState == 4) {
      document.getElementById(n).innerHTML="Ajax: Completed Request";
      if(req.status == 200) {
        document.getElementById(n).innerHTML="Ajax: Status 200 (OK) ";
        var doc = req.responseXML;
        c=0
        function processStatus(s) {
          c++;
          //document.write("Enter "+c+"<br />");
          function processElement(e) {
            if(e.nodeType!=1) return;
            var div="";
            var enc="";
            var data=""
            try {
              div=e.attributes.getNamedItem("div").value;
            } catch (err) {}
            try {
              enc=e.attributes.getNamedItem("enc").value;
            } catch (err) {}
            var key=e.nodeName;
            try {
              data=e.childNodes[0].nodeValue;
            } catch (err) {}
            switch(enc) {
              case "html": data=data.replace(/^\s+|\s+$/g, '');
                           try {
                             if ((div!="")&&(document.getElementById(div).innerHTML!=data)) document.getElementById(div).innerHTML=data;
                           } catch (err) {}
                           break;
              case "test": data=data.replace(/^\s+|\s+$/g, '');
                           document.write("key='"+key+"' div='"+div+"' enc='"+enc+"' data='"+data+"'<br />");
                           document.write("nodeName='"+e.nodeName+"' tagName='"+e.tagName+"' nodType='"+e.nodeType+"' length='"+e.childNodes.length+"'<br />");
                           break;
            }
          };
          processElement(s);
          for (var i=0;i<s.childNodes.length;i++) {
            processElement(s.childNodes[i]);
            if(s.childNodes[i].childNodes.length>1)
              processStatus(s.childNodes[i]);
          }
          //document.write("Exit "+c+"<br />");
          c--;
        };
        x=doc.getElementsByTagName('statusrows').item(0);
        while (x!=null) {
          processStatus(x);
          x=x.nextSibling;
        }
      }	else {
        document.getElementById(n).innerHTML="Ajax: Error occured, status code " + req.status + " " + req.statusText;
      }
      autotimer_running=0;
    }
  }; 
  req.open("POST", url, true); 
  req.send(args);
}

