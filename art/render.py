#!/usr/bin/python
from django.models.art import organisms
import numarray
import Image, ImageDraw

def render(id):
	"""1. Load the specified organism
	2. Render it to a matrix
	3. Normalize each channel to [0,255]
	4. Save it to renders/$id.png"""
	org = organisms.get(pk=id)
	print "Trying to render " + org
