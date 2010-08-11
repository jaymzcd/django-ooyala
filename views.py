from django.shortcuts import render_to_response
from django.template import RequestContext
from ooyala.models import OoyalaItem

def home(request):
    video = OoyalaItem.objects.all()[0]
    context = {
        'video': video,
    }
    return render_to_response('landing-pages/video.html', context, context_instance=RequestContext(request))

def channel(request, object_id):
    video = OoyalaItem.objects.get(pk=object_id)
    context = {
        'video': video,
    }
    return render_to_response('landing-pages/video.html', context, context_instance=RequestContext(request))
