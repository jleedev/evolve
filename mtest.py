#!/usr/bin/python -i
import random
from tree import *

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
		return mutate(child)

def _swap(t):
	"Swap a random subtree for something else."
	# This isn't ideal. It should pick one node at random from the set
	# of nodes, instead of picking randomly at each stop, but it's at
	# least passable.
	c = random.choice(t)
	if isinstance(c, Node):
		# Recurse on c
		return swap(c)
	else:
		# Swap out a child
		i = random.randrange(1,len(t))
		return lambda value: _replace(t, i, value)
