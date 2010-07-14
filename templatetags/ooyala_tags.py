from django import template
from ooyala.models import UrlVideoLink

register = template.Library()

@register.simple_tag
def ooyala_video(for_url):
    try:
        video = UrlVideoLink.objects.get(url=for_url)
    except UrlVideoLink.DoesNotExist:
        return ''
    return """<script src="http://www.ooyala.com/player.js?width=335&height=243&embedCode=%s"></script>""" % video.item.embed_code

