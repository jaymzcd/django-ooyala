# -*- coding: utf-8 -*-
from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import list_detail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from ooyala.models import OoyalaItem, VideoPage
from ooyala.conf import BASE_TEMPLATE

try:
    video_homepage = VideoPage.objects.get(url='/')
except VideoPage.DoesNotExist:
    video_homepage = None

def home(request):
    """ Simple landing page for the most recent video """
    page = get_object_or_404(VideoPage, url='/')
    latest_videos = OoyalaItem.live.all().order_by('-updated_at')
    context = {
        'video_page': page,
        'BASE_TEMPLATE': BASE_TEMPLATE,
    }
    return list_detail.object_list(request, latest_videos, paginate_by=8,
        template_name='ooyala/video_index.html', extra_context=context)

def channel(request, object_id):
    """ Returns a specific OoyalaItem (not necassarily a channel). We *could*
    just return the channel which has a valid embed code, however, it's (client)
    preferred to return the very latest video only, hence the additional request. """

    video = OoyalaItem.objects.get(pk=object_id)
    
    context = {
        'video_page': video_homepage,
        'video': video,
        'BASE_TEMPLATE': BASE_TEMPLATE,
    }
    return render_to_response('ooyala/video_item.html', context, \
        context_instance=RequestContext(request))

def search(request):
    """ Searches the existing OoyalaItem's rather than making a query to Ooyala """
    if 'search_query' in request.POST and request.POST['search_query'] != '':
        search_query = request.POST['search_query']
        items = OoyalaItem.live.all().filter(title__icontains=search_query)
        context = {
            'items': items,
            'BASE_TEMPLATE': BASE_TEMPLATE,            
        }
        return list_detail.object_list(request, items, \
            template_name='ooyala/search_results.html', \
            extra_context={
                'search_query': search_query,
                'video_page': video_homepage,
            })
    else:
        return HttpResponseRedirect(reverse('video:home'))

