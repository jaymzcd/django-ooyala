from django.contrib import admin
from ooyala.models import OoyalaItem, UrlVideoLink, VideoPage, OoyalaChannelList
from ooyala.library import OoyalaQuery

class OoyalaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'content_type', 'nice_length', 'tags')
    list_filter = ('content_type', 'status')
    search_fields = ('title', 'description')

class LinkAdmin(admin.ModelAdmin):
    search_fields = ('item__title', 'url')
    list_display = ('url', 'item')

class PageAdmin(admin.ModelAdmin):
    search_fields = ('url',)
    list_display = ('url',)

    filter_horizontal = ('items',)

class ChannelAdmin(admin.ModelAdmin):
    pass

admin.site.register(OoyalaChannelList, ChannelAdmin)
admin.site.register(OoyalaItem, OoyalaItemAdmin)
admin.site.register(UrlVideoLink, LinkAdmin)
admin.site.register(VideoPage, PageAdmin)
