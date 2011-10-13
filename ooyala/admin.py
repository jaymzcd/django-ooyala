from django.contrib import admin
from ooyala.models import OoyalaItem, UrlVideoLink, VideoPage, OoyalaChannelList, SiteChannels
from ooyala.library import OoyalaQuery
from django.conf import settings



class SiteSaveAdmin(admin.ModelAdmin):
    """ This is the default m2m save for the sites framework for various apps
    This ensures that each admin save adds the correct site_id to the appropriate
    model save """
    def has_fk(self, called='site'):
        "TODO use something f.rel.to==Site"
        return any(f for f in self.model._meta.fields if f.name==called)

    def has_m2m(self, called='sites'):
        "TODO use something f.rel.to==Site"
        return any(f for f in self.model._meta.many_to_many if f.name==called)

    def save_form(self, request, form, change):
        # no point overriding a M2M that is also in the form, as
        # the admin will call form.save_m2m() which will use cleaned_data
        # to overwrite our change later
        if 'sites' in form.fields or 'site' in form.fields:
            return super(SiteSaveAdmin, self).save_form(request, form, change)

        user_site = request.user.get_profile().primary_site
        obj = form.save(commit=False)
        if self.has_fk():
            obj.site = user_site
        if self.has_m2m():
            obj.sites = (user_site,)
        return obj

    # This would be needed if we had inlines
    """
    def save_formset(self, request, form, formset, change):
        super(SiteSaveAdmin, self).save_formset(request, form, formset, change)
        site = request.user.get_profile().primary_site
        try:
            instances = formset.save(commit=False)
            for instance in instances:
                if self.has_fk():
                    instance.site = site
                if self.has_m2m():
                    instance.sites = (site,)
        except ValidationError:
            # It's likely we're not actually dealing with something that should
            # be using this admin class. likely a bug on the admin of the model
            raise
    """

    def base_queryset(self, request):
        """
        edited version from django source
        https://code.djangoproject.com/browser/django/tags/releases/1.3/django/contrib/admin/options.py#L195
        """
        if hasattr(self.model, 'all_objects'):
            qs = self.model.all_objects.get_query_set()
        else:
            qs = self.model._default_manager.get_query_set()
        ordering = self.ordering or () # otherwise we might try to *None, which is bad ;)
        if ordering:
            qs = qs.order_by(*ordering)
        return qs

    def queryset(self, request):
        """ Filter the admin changelist views to return only items that apply
        to the logged in users primary site (so a user that has a profile with
        Vans UK should only see UK content regardless of which URL they
        use to login """
        qs = self.base_queryset(request)
        try:
            user_site = request.user.get_profile().primary_site
        except UserProfile.DoesNotExist:
            # If our logged in user isn't a superuser then we should
            # probably not show them any content to edit just yet
            # whilst someone creates them a valid profile
            user_site = None

        # if we've got a superuser then return it all
        if request.user.is_superuser:
            return qs
        else:
            if self.has_fk():
                return qs.filter(sites__in=(user_site,))
            if self.has_m2m():
                return qs.filter(site=user_site)
        return None



class OoyalaItemAdmin(SiteSaveAdmin):
    queryset = lambda self, req: OoyalaItem.all_objects.all()
    list_display = ('title', 'status', 'content_type', 'nice_length', 'updated_at',)
    list_filter = ('content_type', 'status')
    search_fields = ('title', 'description')

    if not settings.DEBUG:
        exclude = ('site',)

class UrlVideoLinkAdmin(SiteSaveAdmin):
    queryset = lambda self, req: UrlVideoLink.all_objects.all()
    search_fields = ('item__title', 'url')
    list_display = ('url', 'item')
    raw_id_fields = ('item',)
    if not settings.DEBUG:
        exclude = ('sites',)

class VideoPageAdmin(SiteSaveAdmin):
    queryset = lambda self, req: VideoPage.all_objects.all()
    search_fields = ('url',)
    list_display = ('url',)

    filter_horizontal = ('items',)
    if not settings.DEBUG:
        exclude = ('site',)

class ChannelAdmin(admin.ModelAdmin):
    if not settings.DEBUG:
        exclude = ('sites',)
    search_fields = ('channel__title',)
    list_display = ('channel', 'total_items')
    filter_horizontal = ('videos',)

class SiteChannelsAdmin(SiteSaveAdmin):
    if not settings.DEBUG:
        exclude = ('site',)

admin.site.register(OoyalaChannelList, ChannelAdmin)
admin.site.register(OoyalaItem, OoyalaItemAdmin)
admin.site.register(UrlVideoLink, UrlVideoLinkAdmin)
admin.site.register(VideoPage, VideoPageAdmin)
admin.site.register(SiteChannels, SiteChannelsAdmin)
