from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^query/$', 'ooyala.admin_views.backlot_query', {}, 'query'),
)
