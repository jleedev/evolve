from django.conf.urls.defaults import *

urlpatterns = patterns("evolve.art.views",
	(r"^$", "index"),
	(r"^old_vote/$", "vote"),
	(r"^vote/$", "vote2"),

	(r"^view/$", "browse"),
	(r"^view/(?P<generation_num>\d+)/$", "generation"),
	(r"^view/(?P<generation_num>\d+)/(?P<organism_id>\d+)/$", "view"),
)

urlpatterns += patterns("django.views.generic.simple",
	(r"^about/$", "direct_to_template", {"template": "art/about"}),
)
