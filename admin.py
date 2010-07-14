from django.contrib import admin
from ooyala.models import OoyalaItem, UrlVideoLink
from ooyala.library import OoyalaQuery

class OoyalaItemAdmin(admin.ModelAdmin):
    list_display = ('title', 'status', 'content_type', 'nice_length')
    list_filter = ('content_type', 'status')
    search_fields = ('title', 'description')

class LinkAdmin(admin.ModelAdmin):
    search_fields = ('item__title', 'url')
    list_display = ('url', 'item')

admin.site.register(OoyalaItem, OoyalaItemAdmin)
admin.site.register(UrlVideoLink, LinkAdmin)
