#!/usr/bin/python

from math import hypot;
from xml.dom.minidom import parse;
from svg.path import parse_path;

def f(svg, create, duration):
	elements = []
	for node in svg.childNodes:
		try:
			node.tagName; #only on Elements
			elements.append(node);
		except AttributeError:
			pass #Text or Comment
	if len(elements) > 0:
		animate(elements, create, duration);

def animate(shapes, create, duration):
	unit_time = float(duration) / len(shapes);
	previous = None
	for node in shapes:
		current = _getId(node);
		length = computeLength(node);
		updateStyle(node, {'stroke-dasharray': str(length)});
		child = create('animate');
		previous = initializeAnimationNode(child, length, unit_time, current, previous);
		node.appendChild(child);
		node.setAttribute('visibility', 'hidden');
		child = create('set');
		initializeSetNode(child, previous);
		node.appendChild(child);

def computeLength(shape):
	if shape.tagName == 'path':
		path = parse_path(shape.getAttribute('d'));
		return path.length(); # this is by far is the program most costly instruction
	if shape.tagName == 'line':
		return hypot(float(shape.getAttribute('x2')) - float(shape.getAttribute('x1')),
		             float(shape.getAttribute('y2')) - float(shape.getAttribute('y1')));
	if shape.tagName == 'polyline':
		points = shape.getAttribute('points');
		pass #TODO
	if shape.tagName == 'polygon':
		points = shape.getAttribute('points');
		pass #TODO
	print("Unsupported shape \"%s\" will not be animated."%shape.tagName);

def updateStyle(node, style):
	attrs = {};
	result = node.getAttribute('style');
	attrs = {}
	if len(result) > 0:
		attrs = dict(item.split(':') for item in result.split(';'));
	attrs.update(style);
	result = ';'.join(['%s:%s'%(k,v) for k,v in attrs.items()])
	node.setAttribute('style', result);

_counter = 0;
def _getId(node):
	identifier = node.getAttribute('id');
	if len(identifier) is 0:
		global _counter;
		_counter += 1;
		identifier = 'shape%d'%_counter;
		node.setAttribute('id', identifier);
	return identifier;

def initializeAnimationNode(animation, length, duration, pathId, previousAnimation):
	identifier = '%s_animation'%pathId;
	animation.setAttribute('id', identifier);
	animation.setAttribute('attributeName', 'stroke-dashoffset');
	animation.setAttribute('attributeType', 'XML');
	animation.setAttribute('from', str(length));
	animation.setAttribute('to', '0.0');
	begin = '0s';
	if (previousAnimation is not None):
		begin = '%s.end'%previousAnimation;
	animation.setAttribute('begin', begin); #TODO previous.end
	animation.setAttribute('dur', '%ss'%duration);
	return identifier;

def initializeSetNode(node, correspondingAnimation):
	node.setAttribute('attributeName', 'visibility');
	node.setAttribute('from', 'hidden');
	node.setAttribute('to', 'visible');
	node.setAttribute('begin', '%s.begin'%correspondingAnimation);



from argparse import ArgumentParser

if __name__ == '__main__':
	parser = ArgumentParser(description="SVG Animator");
	parser.add_argument('svg_file', help="SVG image input file");
	parser.add_argument('-o', '--output', help="SVG image output file", default='pysvgag_output.svg');
	parser.add_argument('-t', '--total-time', help="Animation total duration in seconds", default=3.0);
	args = parser.parse_args();
	svg = [];
	try:
		with open(args.svg_file) as source:
			dom = parse(source);
			svg = dom.getElementsByTagName('svg');
	except:
		exit("Error: %s seems not to be a valid SVG file."%args.svg_file);
	if svg.length < 1:
		exit("Error: %s seems not to be a valid SVG file."%args.svg_file);
	for image in svg:
		f(image, dom.createElement, args.total_time)
	with open(args.output, 'wb') as f:
		dom.writexml(f);

