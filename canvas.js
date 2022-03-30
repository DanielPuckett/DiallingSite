function toggle(div_id) {
	var el = parent.document.getElementById(div_id);
	if ( el.style.display == 'none' ) {	el.style.display = 'block';}
	else {el.style.display = 'none';}
}
function blanket_size(popUpDivVar) {
	if (typeof parent.window.innerWidth != 'undefined') {
		viewportheight = parent.window.innerHeight;
	} else {
		viewportheight = parent.document.documentElement.clientHeight;
	}
	if ((viewportheight > parent.document.body.parentNode.scrollHeight) && (viewportheight > parent.document.body.parentNode.clientHeight)) {
		blanket_height = viewportheight;
	} else {
		if (parent.document.body.parentNode.clientHeight > parent.document.body.parentNode.scrollHeight) {
			blanket_height = parent.document.body.parentNode.clientHeight;
		} else {
			blanket_height = parent.document.body.parentNode.scrollHeight;
		}
	}
	var blanket = parent.document.getElementById('blanket');
	blanket.style.height = blanket_height + 'px';
	var popUpDiv = parent.document.getElementById(popUpDivVar);
	popUpDiv_height=blanket_height/2-150; //150 is half popup's height
popUpDiv_height=viewportheight/2-150; //150 is half popup's height
if (navigator.appVersion.indexOf("MSIE") != -1)
  popUpDiv_height+=200;
	popUpDiv.style.top = popUpDiv_height + 'px';
}
function window_pos(popUpDivVar) {
	if (typeof parent.window.innerWidth != 'undefined') {
		viewportwidth = parent.window.innerHeight;
	} else {
		viewportwidth = parent.document.documentElement.clientHeight;
	}
	if ((viewportwidth > parent.document.body.parentNode.scrollWidth) && (viewportwidth > parent.document.body.parentNode.clientWidth)) {
		window_width = viewportwidth;
	} else {
		if (parent.document.body.parentNode.clientWidth > parent.document.body.parentNode.scrollWidth) {
			window_width = parent.document.body.parentNode.clientWidth;
		} else {
			window_width = parent.document.body.parentNode.scrollWidth;
		}
	}
	var popUpDiv = parent.document.getElementById(popUpDivVar);
	window_width=window_width/2-150;//150 is half popup's width
	popUpDiv.style.left = window_width + 'px';
}
function popup(windowname) {
	blanket_size(windowname);
	window_pos(windowname);
	toggle('blanket');
	toggle(windowname);		
}
