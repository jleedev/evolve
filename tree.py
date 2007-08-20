#!/usr/bin/python

import sys

import random
from numarray.ufunc import _UFuncs as ufuncs, _UnaryUFunc as unary, _BinaryUFunc as binary

def _expr(tree):
	"Turn a tree into a python expression"
	if not isinstance(tree, (tuple, list)):
		# Base case: it's a variable name or a constant
		return str(tree)
	op = tree[0]
	args = tree[1:]
	return "%s(%s)" % (op, ', '.join(map(_expr, args)))

class Node(list, object):
	# How many nodes are drawn on the page for this tree.
	size = property(fget=lambda self:
		sum([getattr(c, "size", 1) for c in self])
	)

	# How many edges are drawn on the page for this tree.
	len = property(fget=lambda self:
		sum([getattr(c, "len", 0) for c in self[1:]]) + len(self[1:])
	)

	expr = _expr

	def compile(self):
		return compile(self.expr(), "tree.py", "eval")

	def __repr__(self):
		return "Node(%s)" % repr(list(self))

def ellipsize(s, max_length=80):
	if len(s) > max_length:
		return s[:max_length-3] + "..."
	else:
		return s

ops = {}
# Yay backwards incompatibilities
#ops = dict([(op, ufuncs[op].arity) for op in "abs add arcsinh arctan2 ceil cos cosh divide exp floor floor_divide hypot maximum minimum multiply power remainder sin sinh subtract tan tanh true_divide".split()])
for op in "abs add arcsinh arctan2 ceil cos cosh divide exp floor floor_divide hypot maximum minimum multiply power remainder sin sinh subtract tan tanh true_divide".split():
	func = ufuncs[op]
	if type(func) == unary:
		ops[func] = 1
	elif type(func) == binary:
		ops[func] = 2
	else:
		raise ValueError("Unknown arity %s for %s" % (type(func), func))

def random_tree(height=5, root=True, constants=True):
	if height==1:
		# Leaf node: a constant or a variable
		if random.randrange(2) or not constants:
			return random.choice(("x","y"))
		else:
			return random_number()
	elif root:
		# Color node
		op, arity = "rgb", 3
	else:
		# Regular node
		op, arity = random.choice(ops.items())
	return Node([op] + [
		random_tree(height-1, root=False, constants=(arity!=1))
	for i in range(arity)])

def random_number():
	return random.choice(range(-10,0) + range(1,11))

### Breeding stuff

def _replace(lst, index, value):
	old = lst[index]
	lst[index] = value
	return old

def _mutate(t):
	"Change a random node's value."
	e = enumerate(t)
	if t[0] == "rgb":
		e.next()

	# We're picking a random index of t, weighted by size
	stuff = []

	for index, child in e:
		size = getattr(child, "size", 1)
		stuff.extend([index] * size)

	i = random.choice(stuff)
	child = t[i]

	if i == 0 or not isinstance(child, Node):
		# We're changing an item of t
		return lambda value: _replace(t, i, value)
		pass
	elif isinstance(child, Node):
		# We're mutating one of tree's children
		return _mutate(child)

def _swap(t):
	"Swap a random subtree for something else."
	# This isn't ideal. It should pick one node at random from the set
	# of nodes, instead of picking randomly at each stop, but it's at
	# least passable.
	# Idea: make an iterator that yields a node and its parent for every
	# node in the tree
	c = random.choice(t)
	if isinstance(c, Node):
		# Recurse on c
		return _swap(c)
	else:
		# Swap out a child
		i = random.randrange(1,len(t))
		return lambda value: _replace(t, i, value)

def mutate_value(old):
	if old in ops:
		arity = ops[old]
		return random.choice([
			k for k in ops if ops[k] == arity and k != old
		])
	elif old in ['x','y']:
		return "xy"[old == "x"]
	elif isinstance(old, int):
		return random_number()

def mutate(a):
	"Mutates a node in the tree."
	f = _mutate(a)
	old = f(None)
	new = mutate_value(old)
	f(new)

def cross(a,b):
	"Crossover two trees. Returns two new trees."
	fa = _swap(a)
	fb = _swap(b)
	olda = fa(None)
	oldb = fb(olda)
	fa(oldb)

__all__ = "Node ellipsize random_tree mutate cross".split()
