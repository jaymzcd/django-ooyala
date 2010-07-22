from datetime import datetime, timedelta
from django.utils.safestring import mark_safe
from django.db import models

class OoyalaItem(models.Model):
    """ Holds an ooyala item from a Backlot Query request - essentially
    a cached version to save making requests for every client """

    embed_code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, default="live")
    content_type = models.CharField(max_length=20)
    length = models.IntegerField(blank=True, null=True)
    size = models.IntegerField(default=0)
    updated_at = models.DateTimeField()
    flight_start_time = models.DateTimeField()
    width = models.IntegerField()
    height = models.IntegerField()
    thumbnail = models.URLField(blank=True, null=True)
    stat = models.CharField(max_length=255)

    def __unicode__(self):
        return '%s (%s [%s])' % (self.title, self.content_type, self.status)

    @property
    def nice_length(self):
        length = timedelta(milliseconds=self.length)
        return str(length)

    @staticmethod
    def from_xml(xml):
        """ Creates a new item from an input XML definition """

        def get_data(tagname):
            try:
                return xml.getElementsByTagName(tagname)[0].firstChild.nodeValue
            except IndexError:
                if tagname in ['length']:
                    return 0
                else:
                    return None

        item_data = {
            'embed_code': get_data('embedCode'),
            'title': get_data('title'),
            'status': get_data('status'),
            'content_type': get_data('content_type'),
            'length': int(get_data('length')),
            'size': int(get_data('size')),
            'updated_at': datetime.fromtimestamp(float(get_data('updatedAt'))),
            'flight_start_time': datetime.fromtimestamp(float(get_data('flightStartTime'))),
            'width': int(get_data('width')),
            'height': int(get_data('height')),
            'thumbnail': get_data('thumbnail'),
            'stat': get_data('stat'),
        }

        [ooyala_item, created] = OoyalaItem.objects.get_or_create(**item_data)
        if created:
            print "Created new item %s " % ooyala_item.embed_code

        return [ooyala_item, created]

    class Meta:
        ordering = ('-updated_at',)

class UrlVideoLink(models.Model):
    url = models.CharField(unique=True, max_length=255) # unique for now, a path like /news/item/10
    url.help_text = mark_safe("""The url that this video should be connected to '(assuming template supports video). Eg <em>/news/item/</em>, use <strong>/</strong> for home.""")
    url.allow_tags = True
    item = models.ForeignKey(OoyalaItem)
    item.help_text = 'The ooyala content that will be loaded on this page\'s video section'

    def __unicode__(self):
        return self.url

