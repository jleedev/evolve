from django.conf.urls.defaults import *
from django.conf.settings import DEBUG

urlpatterns = patterns('',
	(r'^evolve/', include('evolve.art.urls')),
	(r'^admin/', include('django.contrib.admin.urls.admin')),
	(r'^r/', include('django.conf.urls.shortcut')),
)

if DEBUG:
	# Not for development! Django is not a web server!
	urlpatterns += patterns('',
		(r'^evolve_media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': '/home/josh/code/evolve/media'}),
	)
