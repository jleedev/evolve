#!/usr/bin/python

from django.models.art import organisms
from django.models.formkeys import formkeys
from django.core.db import db

import sys, time
import datetime

# Fifteen minutes
DELAY = 60 * 15

def clean_formkeys():
	cursor = db.cursor()
	ret = cursor.execute("DELETE FROM formkeys_formkeys WHERE timestamp + %s < now()", [DELAY])
	cursor.close()
	return ret

def main(argv):
	while True:
		count = clean_formkeys()
		if count:
			print "%s: cleaned up %i formkey%s" % \
				(datetime.datetime.now().strftime("%F %T"), count, ('s','')[not (count-1)])
		time.sleep(DELAY)
	pass

if __name__== '__main__':
	try:
		sys.exit(main(sys.argv))
	except KeyboardInterrupt:
		print
		raise
