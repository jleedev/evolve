from django.core import meta

class Organism(meta.Model):
	genes = meta.TextField()
	generation = meta.PositiveIntegerField()
	rendered = meta.BooleanField()

	upvotes = meta.PositiveIntegerField(default=0)
	downvotes = meta.PositiveIntegerField(default=0)
	rating = meta.FloatField(max_digits=11, decimal_places=10, default=0.5)

	parent1 = meta.ForeignKey("self", null=True)
	parent2 = meta.ForeignKey("self", null=True)

	def __repr__(self):
		return "Organism (id:%s, generation:%s, genes:'%s')" % \
			(self.id, self.generation, self.genes)
	
	def __str__(self):
		return "Organism (id:%s, generation:%s, genes:'%s')" % \
			(self.id, self.generation, self.genes_ellipsize())
	
	def eval_genes(self):
		from tree import Node
		try:
			return eval(self.genes)
		except MemoryError:
			# dang python parser
			return "[MemoryError] %s" % self.genes
	
	def pretty_genes(self):
		try:
			return self.eval_genes().expr()
		except AttributeError:
			# eval_genes gave up because python couldn't handle the
			# deeply nested expression
			return self.eval_genes()
	pretty_genes.short_description = "Genes"

	def genes_ellipsize(self):
		from tree import ellipsize
		return ellipsize(self.pretty_genes())
	genes_ellipsize.short_description = "Genes..."

	def get_absolute_url(self):
		return "/evolve/view/%s/%s/" % (self.generation, self.id)
	
	def _image_part(self):
		return "renders/%s/%s.png" % (self.generation, self.id)
	def _thumbnail_part(self):
		return "renders/thumbs/%s/%s.png" % (self.generation, self.id)

	def get_image_path(self):
		from django.conf.settings import MEDIA_ROOT
		return os.path.join(MEDIA_ROOT, self._image_part())
	def get_thumbnail_path(self):
		from django.conf.settings import MEDIA_ROOT
		return os.path.join(MEDIA_ROOT, self._thumbnail_part())

	def get_image_url(self):
		from django.conf.settings import MEDIA_URL
		return os.path.join(MEDIA_URL, self._image_part())
	def get_thumbnail_url(self):
		from django.conf.settings import MEDIA_URL
		return os.path.join(MEDIA_URL, self._thumbnail_part())

	def _module_get_generation_list():
		"Returns a sorted list of all generations."
		return [d.values()[0] for d in get_values(fields=["generation"],
		distinct=True, order_by = ["generation"])]
	
	def _module_get_current_generation():
		"Returns the generation in voting now."
		return int(file("/home/josh/code/evolve/CURRENT").read())
	
	def _module_get_votable_organism(count=1):
		"""Returns one or more organisms that have the fewest votes and
		are in the current generation."""
		if count < 1: raise ValueError
		return (get_list, get_object)[count == 1](
			select = {"totalvotes": "upvotes + downvotes"},
			generation__exact = get_current_generation(),
			order_by = ["totalvotes", '?'],
			limit=count,
		)

	def _pre_save(self):
		up = self.upvotes
		down = self.downvotes
		if up and down:
			self.rating = float(up) / (up + down)
		elif up:
			self.rating = 1
		elif down:
			self.rating = 0
		else:
			self.rating = 0.5
	
	class META:
		admin = meta.Admin(
			list_display = (
				"genes_ellipsize", "generation", "rating", "rendered"
			),
			list_filter = ("rendered",),
			fields = (
				(None, {
					"fields": ("genes", "generation"),
				}),
				("Statistics", {
					"fields":
						("rendered", "upvotes", "downvotes", "rating"),
					"classes":"collapse",
				}),
			)
		)

		# This is a load of crap. I want magic-removal.
		module_constants = {
			"os":__import__("os"),
		}
