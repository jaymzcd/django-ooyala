from django.db.models import Manager

class OItemManager(Manager):
    def get_query_set(self):
        return super(OItemManager, self).get_query_set().filter(status=5).order_by('-updated_at')
