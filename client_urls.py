from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^channel/(?P<object_id>\d+)/$', 'ooyala.views.channel', {}, 'channel'),
    (r'^$', 'ooyala.views.home', {}, 'home'),
)
