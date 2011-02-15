# -*- coding: utf-8 -*-
from ooyala.constants import OoyalaAPI
from django.conf import settings

if hasattr(settings, 'OOYALA'):
    API_KEYS = settings.OOYALA['API_KEYS']
    try:
        BASE_TEMPLATE = settings.OOYALA['BASE_TEMPLATE']
    except KeyError:
        BASE_TEMPLATE = 'ooyala/ooyala_base.html'
else:
    raise Exception('Cannot import your Ooyala API keys from settings.py')

# Parameters, remappings and default values for each API type. The base class
# will use the data here to make sure only valid params are passed and it will
# also rename parameters from python style to the required schema defintion

# TODO: the label param should be able to take a list and then transformed into
# label[0..X] etc, for now we allow just 1 label search
OOYALA_PARAMS = {
    OoyalaAPI.BACKLOT.QUERY: {
        'PARAMS': ['content_type', 'statistics', 'description', 'embed_code', 'fields', 'include_deleted', 'label', 'limit', 'page_id' , 'title'],
        'REMAPS': {'embed_code': 'embedCode', 'label': 'label[0]', 'content_type': 'contentType', 'page_id': 'pageID' },
        'DEFAULTS': {},
    },
    OoyalaAPI.BACKLOT.THUMB: {
        'PARAMS': ['indicies', 'resolution', 'embed_code'],
        'REMAPS': {'embed_code': 'embedCode', 'indicies': 'range' },
        'DEFAULTS': {'resolution': '320x240', 'indicies': '1,2,3' },
    },
    OoyalaAPI.BACKLOT.ATTR: {
        'PARAMS': ['title', 'description', 'flight_end', 'flight_start', 'status', 'hosted_at', 'embed_code'],
        'REMAPS': {'embed_code': 'embedCode', 'flight_end': 'flightEnd' , 'flight_start': 'flightStart', 'hosted_at': 'hostedAt'},
        'DEFAULTS': {},
    },
    OoyalaAPI.BACKLOT.LABEL:  {
        'PARAMS': ['mode',],
        'REMAPS': {},
        'DEFAULTS': {},
    },
    OoyalaAPI.BACKLOT.CHANNEL: {
        'PARAMS': ['mode', 'embed_code'],
        'REMAPS': {'embed_code': 'channelEmbedCode'},
        'DEFAULTS': {},
    },
    OoyalaAPI.ANALYTICS.ANALYTICS: {
        'PARAMS': ['date', 'granularity', 'method', 'video'],
        'REMAPS': {},
        'DEFAULTS': {},
    },
}

RENDER_SIZES = {
    'regular': (325, 185),
    'large': (630, 354),
}
