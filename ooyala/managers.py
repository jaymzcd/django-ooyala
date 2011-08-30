from django.db.models import Manager
from django.conf import settings
from django.core.exceptions import FieldError

class OItemManager(Manager):
    def get_query_set(self):
        return super(OItemManager, self).get_query_set().filter(status=5, site=settings.SITE_ID).order_by('-updated_at')

class OChanManager(Manager):
    def get_query_set(self):
        return super(OChanManager, self).get_query_set()

class OSiteManager(Manager):
    def get_query_set(self):
        return super(OSiteManager, self).get_query_set().filter(channel__site=settings.SITE_ID).order_by('-updated_at')

class VideoManager(Manager):
    def get_query_set(self):
        try:
            return super(VideoManager, self).get_query_set().filter(site=settings.SITE_ID).order_by('-updated_at')
        except FieldError:
            return super(VideoManager, self).get_query_set().filter(sites=settings.SITE_ID).order_by('-updated_at')

