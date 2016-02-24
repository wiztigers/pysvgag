
var images = []; // put image ids here
var groups = {};
var durationms = 2500;
var start = null;
var frameId;

function getLength(path) {
	//TODO sometimes all length is not drawn
	return path.getTotalLength();
}

function initialize() {
	for(var i=0; i<images.length; i++) {
		var svg = document.getElementById(images[i]);
		if (svg != null)
			 groups[images[i]] = initializeSVG(svg);
		else console.log("images["+i+"] \""+images[i]+"\": not found.");
	}
}
function initializeSVG(svg) {
	var lengths = {};
	var groups = svg.getElementsByTagName('g');
	for(var g=0; g<groups.length; g++) {
		var gid = groups[g].id;
		lengths[gid] = 0;
		var paths = groups[g].getElementsByTagName('path');
		for(var p=0; p<paths.length; p++) {
			var len = getLength(paths[p]);
			// we must do it all by hand, so no need to set properties like
			// animation-duration, animation-timing-function and so on
			paths[p].setAttribute('stroke-dasharray',  len);
			paths[p].setAttribute('stroke-dashoffset', len);
			paths[p].setAttribute('svgag-ingroupoffset', lengths[gid]);
			lengths[gid] += len;
		}
		groups[g].setAttribute('svgag-length', lengths[gid]);
	}
	return lengths;
}
function step(timestamp) {
	if (start == null) start = timestamp;
	var progress = timestamp - start;
	if (progress >= durationms) {
		cancelAnimationFrame(frameId);
		return;
	}
	progress = progress/durationms;
	for(var i=0; i<images.length;i++) {
		stepSVG(images[i], progress);
	}
	frameId = requestAnimationFrame(step);
}
function stepSVG(iname, progress) {
	var svg = document.getElementById(iname);
	if (svg == null) return;
	var groups = svg.getElementsByTagName('g');
	for(var g=0; g<groups.length; g++) {
		var grouplen = groups[g].getAttribute('svgag-length');
		var current = progress*grouplen;
		var paths = groups[g].getElementsByTagName('path');
		for(var p=0; p<paths.length; p++) {
			var offset = paths[p].getAttribute('svgag-ingroupoffset');
			var os = current-offset;
			if (os < 0) break;//we have already drawn a previous path
			var len = paths[p].getAttribute('stroke-dasharray');
			if (os > len) continue; // we have already drawn this path
			paths[p].setAttribute('stroke-dashoffset', len-os);
		}
	}
}

window.onload = function f() {
	//add an load event listener to the object, to load the svg doc asynchronously
	//svg.addEventListener('load',function(){
//	svg.onload = function() {
//		var doc = svg.contentDocument; // get the inner DOM of the .svg file
//		var paths = doc.getElementsByTagName('path');
		initialize();
//		for(var path in paths) initialize(path);
		frameId = requestAnimationFrame(step);
	//}, false);
//	};
}

