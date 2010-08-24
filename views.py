from django.shortcuts import render_to_response, get_object_or_404
from django.views.generic import list_detail
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.template import RequestContext
from ooyala.models import OoyalaItem, VideoPage

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
    }
    return list_detail.object_list(request, latest_videos, paginate_by=8,
        template_name='landing-pages/video.html', extra_context=context)

def channel(request, object_id):
    """ Returns a specific OoyalaItem (not necassarily a channel) """
    video = OoyalaItem.objects.get(pk=object_id)
    context = {
        'video_homepage': video_homepage,
        'video': video,
    }
    return render_to_response('video/video_item.html', context, \
        context_instance=RequestContext(request))

def search(request):
    """ Searches the existing OoyalaItem's rather than making a query to Ooyala """
    if 'search_query' in request.POST and request.POST['search_query'] != '':
        search_query = request.POST['search_query']
        items = OoyalaItem.live.all().filter(title__icontains=search_query)
        context = {
            'items': items,
        }
        return list_detail.object_list(request, items, \
            template_name='video/search_results.html', \
            extra_context={
                'search_query': search_query,
                'video_homepage': video_homepage,
            })
    else:
        return HttpResponseRedirect(reverse('video:home'))

