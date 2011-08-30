from django.contrib import admin
from ooyala.models import OoyalaItem, UrlVideoLink, VideoPage, OoyalaChannelList, SiteChannels
from ooyala.library import OoyalaQuery
from django.conf import settings



class OoyalaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'content_type', 'nice_length', 'updated_at',)
    list_filter = ('content_type', 'status')
    search_fields = ('title', 'description')
    if not settings.DEBUG:
        exclude = ['site']

class LinkAdmin(admin.ModelAdmin):
    search_fields = ('item__title', 'url')
    list_display = ('url', 'item')
    raw_id_fields = ('item',)
    if not settings.DEBUG:
        exclude = ['sites']

class PageAdmin(admin.ModelAdmin):
    search_fields = ('url',)
    list_display = ('url',)

    filter_horizontal = ('items',)

class ChannelAdmin(admin.ModelAdmin):
    if not settings.DEBUG:
        exclude = ['sites']
    search_fields = ('channel__title',)
    list_display = ('channel', 'total_items')
    filter_horizontal = ('videos',)

admin.site.register(OoyalaChannelList, ChannelAdmin)
admin.site.register(OoyalaItem, OoyalaItemAdmin)
admin.site.register(UrlVideoLink, LinkAdmin)
admin.site.register(VideoPage, PageAdmin)
admin.site.register(SiteChannels)

