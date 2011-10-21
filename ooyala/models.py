# -*- coding: utf-8 -*-
import sys
from datetime import datetime, timedelta
from django.utils.safestring import mark_safe
from django.db import models
from ooyala.managers import OItemManager, OChanManager, OSiteManager, VideoManager, UrlVideoLinkManager
from django.contrib.sites.models import Site
from django.conf import settings

#from xml.dom import minidom

class OoyalaItem(models.Model):
    """ Holds an ooyala item from a Backlot Query request - essentially
    a cached version to save making requests for every client """

    STATUS_CHOICES = (
        (0, 'Offline'),
        (1, 'Paused'),
        (5, 'Live'),
        (-1, 'File Missing'),
        (-2, 'Uploading'),
        (-3, 'Processing'),
    )
    # Ugh!
    STATUS_LOOKUP = {
        'offline': 0,
        'uploading': 3,
        'paused': 1,
        'live': 5,
    }

    embed_code = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    status = models.IntegerField(max_length=10, default=5, choices=STATUS_CHOICES)
    content_type = models.CharField(max_length=20)
    length = models.IntegerField(blank=True, null=True)
    size = models.BigIntegerField(default=0)
    updated_at = models.DateTimeField()
    flight_start_time = models.DateTimeField()
    width = models.IntegerField()
    height = models.IntegerField()
    thumbnail = models.URLField(blank=True, null=True)
    stat = models.CharField(max_length=255, blank=True, null=True)

    site = models.ForeignKey(Site, null=True, blank=True)
    tags = models.CharField(max_length=255, blank=True, null=True)
    tags.help_text = 'Simple tag field, seperate with commas'

    def __unicode__(self):
        return '%s (%s [%s])' % (self.title, self.content_type, self.get_status_display())

    objects = OItemManager()
    all_objects = models.Manager()
    live = OItemManager()
    ochan = OChanManager()

    @models.permalink
    def get_absolute_url(self):
        return ('video:channel', [self.pk,])

    @property
    def tag_list(self):
        if self.tags:
            return self.tags.split(',')
        else:
            return None

    @property
    def nice_length(self):
        length = timedelta(milliseconds=self.length)
        return str(length)

    @staticmethod
    def from_xml(xml):
        """ Creates a new item from an input XML definition """

        def get_data(tagname):
            if tagname == 'metadata':
                metadata = xml.getElementsByTagName('metadata')
                for meta in metadata:
                    for i in meta.getElementsByTagName('metadataItem'):
                        if i.getAttribute('name') == 'site':
                            site_id = settings.SITE_ID
                            try:
                                site = Site.objects.get(domain=i.getAttribute('value'))
                            except Site.DoesNotExist:
                                site = Site.objects.get(pk=site_id)
                            return site

            try:
                if tagname != 'metadata':
                    tag_field = xml.getElementsByTagName(tagname)[0].firstChild.nodeValue
                    return tag_field
            except IndexError:
                if tagname in ['length']:
                    return 0
                else:
                    return None

        created = False

        # we are getting a couple items with status_key "filemissing", so should skip rather than fail
        status_key = get_data('status')
        if status_key not in OoyalaItem.STATUS_LOOKUP:
            sys.stdout.write("Unknown OoyalaItem.STATUS_LOOKUP: %s" % status_key)
            return [None, False]
        status = OoyalaItem.STATUS_LOOKUP[status_key]

        item_data = {

            'embed_code': get_data('embedCode'),
            'title': get_data('title'),
            'status': status,
            'content_type': get_data('content_type'),
            'length': int(get_data('length')),
            'size': int(get_data('size')),
            'updated_at': datetime.fromtimestamp(float(get_data('updatedAt'))),
            'flight_start_time': datetime.fromtimestamp(float(get_data('flightStartTime'))),
            'width': int(get_data('width')),
            'height': int(get_data('height')),
            'thumbnail': get_data('thumbnail'),
            'stat': get_data('stat'),
            'description': '',
            'site': get_data('metadata'), # actually will be a attribute
        }

        try:
            item_data.update(dict(description=get_data('description'))) # not everything has
        except:
            pass

        try:
            ooyala_item = OoyalaItem.all_objects.get(embed_code=get_data('embedCode'))
            ooyala_item.description = item_data['description']
            #TODO: here attributes should update for that item
        except OoyalaItem.DoesNotExist:
            created = True
            ooyala_item = OoyalaItem(**item_data)
        ooyala_item.save()

        if created:
            print "Created new item %s " % ooyala_item.embed_code

        return [ooyala_item, created]

    class Meta:
        ordering = ('title',)

class OoyalaChannelList(models.Model):
    """ Holds a collection of OoyalaItems which match a channel to it's associated
    video items. You can treat channels just like regular video's in Ooyala so
    these can be used to output other videos from a channel """

    channel = models.ForeignKey(OoyalaItem, related_name='channel', unique=True)
    videos = models.ManyToManyField(OoyalaItem, related_name='videos')

    @property
    def latest_video(self):
        try:
            return videos.all()[0].filter(site_id__in=settings.SITEPOST["SITES_DISPLAY"])
        except IndexError:
            return None

    def __unicode__(self):
        try:
            return self.channel.title
        except:
            return 'Missing data'

    @property
    def total_items(self):
        return self.videos.count()


class UrlVideoLink(models.Model):
    sites = models.ManyToManyField(Site, blank=True, null=True)
    url = models.CharField(max_length=255)
    url.help_text = mark_safe("""The url that this video should be connected to '(assuming template supports video). Eg <em>/news/item/</em>, use <strong>/</strong> for home.""")
    url.allow_tags = True
    item = models.ForeignKey(OoyalaItem)
    item.help_text = 'The ooyala content that will be loaded on this page\'s video section'

    def __unicode__(self):
        return self.url

    objects = UrlVideoLinkManager()
    all_objects = models.Manager()

class VideoPage(models.Model):
    site = models.ForeignKey(Site, blank=True, null=True)
    url = models.CharField(max_length=255)
    url.help_text = 'The url for this page to load (relative to /video/). Use / for just top level page.'
    items = models.ManyToManyField(OoyalaItem)
    featured_item = models.ForeignKey(OoyalaItem, related_name='featured_item')
    updated_at = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return self.url

    class Meta:
        unique_together = ('site', 'url')

    objects = VideoManager()
    all_objects = models.Manager()

class SiteChannels(models.Model):
    site = models.ForeignKey(Site, blank=True, null=True)
    channel = models.ManyToManyField(OoyalaChannelList)

    class Meta():
        verbose_name_plural = 'Site Channels'

    def __unicode__(self):
        return self.site.name
