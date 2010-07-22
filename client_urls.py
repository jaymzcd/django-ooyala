from django.conf.urls.defaults import *

urlpatterns = patterns('',
    (r'^$', 'ooyala.views.home', {}, 'home'),
)
