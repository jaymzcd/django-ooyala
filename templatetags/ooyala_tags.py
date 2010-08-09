from django import template
from ooyala.models import UrlVideoLink, OoyalaItem
from ooyala.conf import RENDER_SIZES

register = template.Library()

@register.simple_tag
def ooyala_video(for_url, width=RENDER_SIZES['regular'][0], height=RENDER_SIZES['regular'][1]):
    try:
        video = UrlVideoLink.objects.get(url=for_url)
    except UrlVideoLink.DoesNotExist:
        return ''
    return """
        <div class="ooyala-video">
            <script src="http://www.ooyala.com/player.js?width=%d&height=%d&embedCode=%s"></script>
        </div>
    """ % (width, height, video.item.embed_code)

@register.simple_tag
def ooyala_for_object(video_object, width=RENDER_SIZES['large'][0], height=RENDER_SIZES['large'][1]):
    try:
        return """
            <script src="http://www.ooyala.com/player.js?width=%d&height=%d&embedCode=%s"></script>
        """ % (width, height, video_object.embed_code)
    except AttributeError:
        return ""

@register.inclusion_tag('ooyala/tags/channel_list.html')
def ooyala_channel_list(limit=None):
    channels = OoyalaItem.objects.all().filter(content_type='channel')
    if limit:
        channels = channels[:limit]
    return {
        'channels': channels,
    }

@register.inclusion_tag('ooyala/tags/facebook_headers.html')
def ooyala_facebook_headers(video_object):
    return {
        'video': video_object,
    }
