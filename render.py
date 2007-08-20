#!/usr/bin/python

import sys, os
from numarray import *
from numarray import ieeespecial as ieee
import Image, ImageDraw
import tree
from tree import *
import re

"""1. Render to a matrix
2. Normalize each channel to [0,255]
3. Save it to renders/$id.png
4. Save a thumbnail to renders/$id.thumb.png"""

""" (0,0) YMAX
    +------+------+
    |      |      |
    |      |      |
XMIN+------+------+XMAX
    |      |      |
    |      |      |
    +------+------+(IMAGE_WIDTH, IMAGE_HEIGHT)
          YMIN"""

ZOOM = 10.001
SIZE = 400
HALF_SIZE = SIZE / 2.

RATIO = ZOOM / HALF_SIZE

Error.setMode(all="raise")

class NotRenderable(ValueError): pass

def is_special(v):
	v = repr(v)
	return v=="nan" or v=="inf" or v=="-inf"

def evaluate(c, y, x):
	"Evaluates c in the context of _UFuncs, x, and y."
	x,y = (x - SIZE/2) * RATIO, (SIZE/2 - y) * RATIO
	# Misalign some math errors
	x += 1e-10
	y += 1e-10
	result = eval(c, ufunc._UFuncs, dict(x=x,y=y))
	try:
		len(result)
	except TypeError:
		# Idiot c evaluated to a float. This is because the random tree
		# generator picked all constants, without any x or y. Let's be
		# nice and turn it into a bunch of that result.
		result *= ones(type=Float64, shape=(SIZE, SIZE))

	# Normalize the data to interval[0,255]. Do this by finding the
	# minimum and maximum values.
	copy = ravel(result.copy())
	copy.sort()

	for minv in copy:
		if not is_special(minv): break
	else: raise ValueError("Ack! No numbers!")

	for maxv in copy[::-1]:
		if not is_special(maxv): break
		else: break
	else: raise ValueError("Ack! No numbers!")

	print "Min, max:", (minv,maxv)
	diff = maxv-minv+1

	result[ieee.getnan(result)] = minv
	result[ieee.getneginf(result)] = minv
	result[ieee.getposinf(result)] = maxv

	result -= minv
	result /= diff
	result *= 255

	result[ieee.getnan(result)] = 0
	result[ieee.getinf(result)] = 0
	return result.astype(UInt32)

def _render(t):
	"Renders the tree and returns the image data."
	print "Rendering", t

	if t[0] != "rgb": raise ValueError("t must be an rgb() node")

	nodes = []
	for n in t[1:]:
		# We may end up with a string instead of a ufunc as a top-level
		# item, as a result of the crossing-over process. Let's give it
		# something that it can call
		if not isinstance(n, tree.Node):
			n = tree.Node(["add",n,0])
		nodes.append(n)

	red, green, blue = [fromfunction(lambda x,y: evaluate(node.compile(),x,y), (SIZE, SIZE)) for node in nodes]
	data = array(shape=(SIZE, SIZE*3), type=UInt8)
	# This slice is kinda confusing
	data[:,::3] = red
	data[:,1::3] = green
	data[:,2::3] = blue
	return data

def do_render(t, filename, thumbname=None):
	try:
		# Make sure we can recreate this organism later!
		eval(repr(t))
		a = _render(t)
	#except (ZeroDivisionError, OverflowError, UnderflowError, ufunc.MathDomainError, MemoryError, ValueError):
	except:
		raise NotRenderable
	image = Image.fromstring("RGB", (SIZE, SIZE), a.tostring())
	image.save(filename)
	if thumbname is not None:
		image = image.resize((100,100), Image.ANTIALIAS)
		image.save(thumbname)
