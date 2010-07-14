from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'ooyala.admin_views.backlot_query', {}, 'home'),
)
