function submitticketform() {
   var txt = "<h3>Ticket created, waiting on results to load.</h3>";
   var frame = document.getElementById('ticketprocessor');
   var frame = (frame.contentWindow || frame.contentDocument);
   if (frame.document) frame = frame.document;
   frame.open();
   frame.write(txt);
   frame.close();
  document.ticketform.submit();
}
