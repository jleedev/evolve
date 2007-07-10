#!/usr/bin/python2.3

from django.models.art import organisms
from django.conf.settings import *
import sys, os
import tree, render

def main(argv):
	try:
		count = int(argv[1])
	except:
		count = GENERATION_SIZE
	
	while count:
		print count, "left to go"
		t = tree.random_tree()
		org = organisms.Organism(genes=repr(t), generation=0)
		# Save the organism so it will have an id and hence a place to
		# store the images.
		org.save()
		try:
			for path in (org.get_image_path(), org.get_thumbnail_path()): 
				dir = os.path.dirname(path)
				if not os.path.isdir(dir):
					os.mkdir(dir)
			render.do_render(t, org.get_image_path(), org.get_thumbnail_path())
		except KeyboardInterrupt:
			print "Discarding", org.id
			org.delete()
			raise
		except render.NotRenderable:
			print "Discarding", org.id
			org.delete()
		else:
			print "Saving", org.id
			org.rendered = True
			org.save()
			count -= 1

if __name__=='__main__':
	sys.exit(main(sys.argv))
