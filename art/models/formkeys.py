from django.core import meta

class Formkey(meta.Model):
	"""To use a formkey, just create it, give it data, and save it.
	Then you can call its check_hash function and stuff."""
	hash = meta.CharField(maxlength=40)
	data = meta.IntegerField()
	# http://code.djangoproject.com/ticket/555
	timestamp = meta.DateTimeField(auto_now_add=False)

	def _pre_save(self):
		if not self.timestamp: self.timestamp = datetime.datetime.now()
		# Tricky tricky. Microseconds vanish when saving to mysql, so
		# we zero it now to make the hash not change.
		self.timestamp = self.timestamp.replace(microsecond = 0)
		self.hash = self.calc_hash(self.data)

	def calc_hash(self, data):
		"Cats data+timestamp+secretkey, and returns their hash."
		import sha
		from django.conf.settings import SECRET_KEY
		if not self.timestamp:
			raise ValueError, "No timestamp?"
		return sha.sha(
			str(data)+str(self.timestamp)+SECRET_KEY
		).hexdigest()

	def check(self, data):
		return self.hash == self.calc_hash(data)

	def __repr__(self):
		return "Formkey, data=(%s)" % self.data
