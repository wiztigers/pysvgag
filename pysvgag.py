from xml.dom.minidom import parse;
from svg.path import parse_path;

def f(svg, create, duration):
	animate(svg.getElementsByTagName('path'), create, duration);

def animate(shapes, create, duration):
	unit_time = float(duration) / shapes.length;
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
	print("Unsupported shape \"%s\"."%shape.tagName); #TODO

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



if __name__ == '__main__':
	source = open('sample.svg');
	dom = parse(source);
	svg = dom.getElementsByTagName('svg');
	if svg.length < 1:
		print("Not an SVG file.");
		exit(1);
	for image in svg:
		f(image, dom.createElement, 12)
	with open('sample_animated.svg', 'wb') as f:
		dom.writexml(f);

