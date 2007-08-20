from django.core.extensions import *
from django.utils.httpwrappers import *
from django.models.art import organisms
from django.models.formkeys import formkeys

def index(request):
	"Home page"
	status = file("/home/josh/code/evolve/STATUS").read().strip()
	return render_to_response("art/index", locals())

def vote(request):
	"Vote a single organism up or down"
	if request.POST:
		#formkey = request.POST["formkey"]
		vote = request.POST["vote"]
		id = int(request.POST["id"])
		#try:
		#	key = formkeys.get_object(hash__exact=formkey)
		#	assert key.check(id)
		#except (formkeys.FormkeyDoesNotExist, AssertionError):
		#	return render_to_response("art/bad_formkey")
		
		# Okey-dokey
		org = organisms.get_object(pk=id)
		if vote == "good":
			org.upvotes += 1
		elif vote == "bad":
			org.downvotes += 1
		else:
			response = render_to_response("art/bad_vote", {"vote":request.POST.getlist("vote")})
			response.status_code = 400
			return response
		
		org.save()
		#key.delete()
		return HttpResponseRedirect("/evolve/vote/")
		
	org = organisms.get_votable_organism()
	#key = formkeys.Formkey(data=org.id)
	#key.save()
	#formkey = key.hash
	response = render_to_response("art/vote", locals())
	response["Cache-Control"] = "private"
	response["Expires"] = "-1"
	return response

def vote2(request):
	"Vote between two organisms"
	if request.POST:
		vote = request.POST["vote"]
		id1 = int(request.POST["id1"])
		id2 = int(request.POST["id2"])

		org1 = organisms.get_object(pk=id1)
		org2 = organisms.get_object(pk=id2)

		if vote == "first":
			org1.upvotes += 1
			org2.downvotes += 1
		elif vote == "second":
			org1.downvotes += 1
			org2.downvotes += 1
		else:
			response = render_to_response("art/bad_vote", {"vote":request.POST.getlist("vote")})
			response.status_code = 400
			return response

		org1.save()
		org2.save()

		return HttpResponseRedirect("/evolve/vote/")
	
	org1, org2 = organisms.get_votable_organism(2)
	response = render_to_response("art/vote2", locals())
	response["Cache-Control"] = "private"
	response["Expires"] = "-1"
	return response

def browse(request):
	"Main browsing page, list of generations"
	gens = organisms.get_generation_list()
	top_list = organisms.get_list(
		order_by = ["-rating", "?"],
		where = ["upvotes+downvotes <= 21"],
		limit = 5,
	)
	random_list = organisms.get_list(
		order_by = ["?"],
		limit = 5,
	)
	return render_to_response("art/browse", locals())

PAGE_SIZE = 10
def generation(request, generation_num):
	"Browse through a generation"

	gen = generation_num

	total = organisms.get_count(generation__exact=gen, rendered__exact=True)
	if total == 0: raise Http404("No such generation")

	start = int(request.GET.get("start", 0))
	if start < 0: start += total
	stop = start + PAGE_SIZE
	prev = start - PAGE_SIZE
	next = start + PAGE_SIZE
	last = total - PAGE_SIZE

	if prev < 0: prev = "None"
	if next >= total: next = "None"

	orgs = organisms.get_list(
		generation__exact=gen,
		rendered__exact=True,
		limit = 10,
		offset = start,
		order_by = ["-rating"],
	)
	
	return render_to_response("art/generation", locals())

def perfection(request):
	"Browse all perfect organisms."
	total = organism.get_count(rating__exact=1.0, rendered__exact=True)
	start = int(request.GET.get("start", 0))
	if start < 0: start += total
	stop = start + PAGE_SIZE
	prev = start - PAGE_SIZE
	next = start + PAGE_SIZE
	last = total - PAGE_SIZE

	if prev < 0: prev = "None"
	if next >= total: next = "None"

	orgs = organisms.get_list(
		rating__exact=1.0
		rendered__exact=True,
		limit = 10,
		offset = start,
		order_by = ["-upvotes"],
	)

	return render_to_response("art/perfection", locals())

def view(request, generation_num, organism_id):
	"Organism detail page"
	organism = get_object_or_404(organisms,
		generation__exact = generation_num,
		id__exact = organism_id,
	)
	parents = []
	try: parents.append(organism.get_parent1())
	except: pass
	try: parents.append(organism.get_parent2())
	except: pass
	children = organism.get_organism_list()
	return render_to_response("art/view_organism", locals())

__all__ = "index vote vote2 browse generation perfection view".split()
