#!/usr/bin/python

from django.models.art import organisms
from django.conf import settings
from django.core.db import db

import tree, render
import sys, os, time
import random

# Probabilities for mutation, reproduction, crossover and spontaneous
# generation.
P_M = 0.05
P_R = P_M + 0.05
P_X = P_R + 0.75
P_G = P_X + 0.15

# Quick update: 3 seconds
# This is so the status message gets updated often and breeder will
# spring into action as soon as the voting is done.
DELAY = 3

def set_status(text, old_text = [""]):
	if text != old_text[0]:
		old_text[0] = text
		print time.strftime("[%F %T]"), text
		f = file("/home/josh/code/evolve/STATUS",'w')
		print >> f, text
		f.close()

def selection():
	"Continuously yield organisms that have a good rating"
	gen = organisms.get_current_generation()
	orgs = organisms.get_list(generation__exact=gen, order_by='?')
	max_rating = float(sum([org.rating for org in orgs]))
	while True:
		choice = random.random() * max_rating
		current = 0.0
		for org in orgs:
			current += float(org.rating)
			if current >= choice:
				yield org
				break

def breed():
	s = selection()
	new = []
	count = settings.GENERATION_SIZE
	gen = organisms.get_current_generation() + 1
	count -= organisms.get_count(generation__exact=gen)
	while count > 0:
		set_status("Generation %s is breeding: %s left" % (gen, count))
		old = s.next()
		try:
			genes = old.eval_genes()
		except MemoryError:
			continue
		other = None
		genes2 = None
		orphan = False

		p = random.random() * P_G
		print "p is", p
		if p < P_M:
			# Mutate
			print "mutating"
			tree.mutate(genes)
		elif P_M < p < P_R:
			# Reproduce (do nothing)
			print "nothing"
			pass
		elif P_R < p < P_X:
			# Cross over
			print "crossing"
			other = s.next()
			try:
				genes2 = other.eval_genes()
			except MemoryError:
				continue
			tree.cross(genes, genes2)
		elif P_X < p < P_G:
			# New organism
			orphan = True
			print "brand new one"
			genes = tree.random_tree()

		# i.e. 'For genes, and optionally for genes2:'
		for g in filter(bool, (genes, genes2)):
			# Save and render it!
			org = organisms.Organism(genes=repr(g), generation=gen)
			if not orphan: org.parent1_id = old.id
			if other: org.parent2_id = other.id
			# Save the organism so it will have an id and hence a place to
			# store the images.
			org.save()
			try:
				for path in (org.get_image_path(), org.get_thumbnail_path()): 
					dir = os.path.dirname(path)
					if not os.path.isdir(dir):
						os.mkdir(dir)
				render.do_render(g, org.get_image_path(), org.get_thumbnail_path())
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
	# Done
	f = file("/home/josh/code/evolve/CURRENT",'w')
	print >> f, gen
	f.close()

def main(argv):
	print time.strftime("[%F %T]"), "breeder.py started"
	try:
		cursor = db.cursor()
		while True:
			gen = organisms.get_current_generation()
			cursor.execute("""
				SELECT sum(upvotes+downvotes) FROM art_organisms
					WHERE generation=%s
			""", [gen])
			votes = cursor.fetchone()[0]
			if votes is None: raise ValueError("No current generation?")
			else: votes = int(votes)
			needed = settings.GENERATION_SIZE * settings.VOTES_NEEDED
			if votes >= needed:
				set_status("Breeding generation %s, please wait!" % (gen+1))
				breed()
			else:
				set_status("Generation %(gen)s is in voting: %(votes)s votes out of %(needed)s needed" % locals())
			time.sleep(DELAY)
	finally:
		cursor.close()

if __name__=='__main__':
	sys.exit(main(sys.argv))
