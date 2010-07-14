from django import template
register = template.Library()

@register.simple_tag
def ooyala_latest_video():
    return """<script src="http://www.ooyala.com/player.js?width=335&height=243&embedCode=U0a2R5Op9wcpdGIDleeT5DanDHROx94Q"></script>"""

