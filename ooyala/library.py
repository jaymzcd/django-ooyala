# -*- coding: utf-8 -*-
import hashlib
import urllib
import base64
import time
import datetime
from xml.dom.minidom import parseString
from xml.parsers.expat import ExpatError

from ooyala.exceptions import OoyalaParameterException
from ooyala.constants import OoyalaConstants as O
from ooyala.constants import OoyalaAPI
from ooyala.conf import *

class OoyalaRequest(object):
    """
        Represents a request to Ooyala for various data. You can pass through
        an expiry time for the request or include it in the params passed. If
        you include it in your params it needs to be (epoch + offset)
    """
    created = None
    action = None
    expires = O.DEFAULT_EXPIRE_TIME
    processed = False
    response = None
    api_url = None

    def __init__(self, action, api_url, expires=None):
        self.created = time.mktime(time.gmtime()) # time.time is giving me the wrong time!?
        self.action = action # set to the particular backlot api you want to use
        self.api_url = api_url # different "top level" API's have different URI's
        if expires:
            self.expires = expires

    def __str__(self):
        return self.__class__.__name__ + ' ' + self.params().__str__()

    def params(self):
        params = dict()
        attrs = self.__dict__.items()
        for key, value in attrs:
            if key in OOYALA_PARAMS[self.action]['PARAMS'] and value is not None:
                params.update({key : getattr(self, key)})
                if type(value) == bool:
                    value = repr(value).lower() # convert True to "true"
                    params.update({key : value })
                if type(value) == list:
                    value = ','.join(value) # comma-sep. lists
                    params.update({key : value })
        params.update(dict(expires=self.expiry()))
        return self.clean_params(params)

    def clean_params(self, params):
        """ Changes some parameters from the usual python style of foo_bar to
            Ooyala prefered camelCase. Weirdly the Ooyala XML has a mix itself!
            List the names you want convereted below
        """
        ooyala_mapping = OOYALA_PARAMS[self.action]['REMAPS']
        return dict(map(lambda (k, v): (ooyala_mapping.get(k, k), v), params.items()))

    def expiry(self):
        return int(self.created + self.expires)

    @property
    def url(self):
        """ Returns the URL used to issue a request for data """
        signature = self.signature()
        uri = OoyalaAPI.BASE_URL + self.api_url + self.action + '?pcode=' + \
            API_KEYS['PARTNER_CODE'] + '&' + urllib.urlencode(self.params()) + \
            '&signature=' + signature
        return uri

    def process(self):
        """ Makes the request to Ooyala and flags the query as processed. """
        if not self.processed:
            backlot = urllib.urlopen(self.url)
            self.response = backlot.read()
            self.processed = True
            backlot.close()
        try:
            return parseString(self.response)
        except ExpatError:
            # we seem to have had an issue decoding that XML, send back response
            return self.response

    def signature(self):
        """ Create a signature for signing Backlot API requests
            This is based on the method outlined here:

            http://www.ooyala.com/support/docs/backlot_api#signing
        """
        keys = sorted(self.params().keys())
        param_str = ''.join([key + '=' + self.params()[key].__str__() for key in keys])
        signature = hashlib.sha256(''.join([API_KEYS['SECRET_CODE'], param_str]))
        digest64 = base64.b64encode(signature.digest())
        signature = digest64[0:43].rstrip('=')
        return signature

class OoyalaQuery(OoyalaRequest):
    """ An Ooyala query
        API Definition: http://www.ooyala.com/support/docs/backlot_api#query
    """

    def __init__(self, **kwargs):
        super(OoyalaQuery, self).__init__(OoyalaAPI.BACKLOT.QUERY, OoyalaAPI.BACKLOT.URL)

        self.content_type = kwargs.get('content_type', None)
        self.description = kwargs.get('description', None)
        self.embed_code = kwargs.get('embed_code', None)
        self.fields = kwargs.get('fields', None)
        self.include_deleted = kwargs.get('include_deleted', None)
        self.label = kwargs.get('label', None)
        self.page_id = kwargs.get('page_id', None)
        self.query_mode = kwargs.get('query_mode', None)
        self.statistics = kwargs.get('statistics', None)
        self.status = kwargs.get('status', None)
        self.title = kwargs.get('title', None)
        self.updated_after = kwargs.get('updated_after', None)
        self.order_by = kwargs.get('order_by', None)
        self.limit = O.OOYALA_QUERY_LIMIT


class OoyalaThumbnail(OoyalaRequest):
    """ An Ooyala thumbnail lookup. The embed code must be provided
        API Definition: http://www.ooyala.com/support/docs/backlot_api#thumbnail
    """

    def __init__(self, **kwargs):
        """ All params for this API call must be defined """
        super(OoyalaThumbnail, self).__init__(OoyalaAPI.BACKLOT.THUMB, OoyalaAPI.BACKLOT.URL)

        defaults = OOYALA_PARAMS[OOYALA_ACTION_THUMB]['DEFAULTS']

        self.embed_code = kwargs.get('embed_code', None)
        self.indicies = kwargs.get('indicies', defaults['indicies'])
        self.resolution = kwargs.get('resolution', defaults['resolution'])

        if self.embed_code is None:
            raise OoyalaParameterException('embed_code')


class OoyalaAttributeEdit(OoyalaRequest):
    """ An Ooyala attribute api class. The embed code must be provided
        API Definition: http://www.ooyala.com/support/docs/backlot_api#attribute

        This API is used to update the attributes of videos already uploaded
        onto backlot. Use flight_end/start to enable/disable a video for a date
        range. Set status to "paused" to have it taken offline.
    """

    def __init__(self, **kwargs):
        """ All params for this API call must be defined """
        super(OoyalaAttributeEdit, self).__init__(OoyalaAPI.BACKLOT.ATTR, OoyalaAPI.BACKLOT.URL)

        self.embed_code = kwargs.get('embed_code', None)
        self.title = kwargs.get('title', None)
        self.description = kwargs.get('description', None)
        self.flight_end = kwargs.get('flight_end', None)
        self.flight_start = kwargs.get('flight_start', None)
        self.status = kwargs.get('status', None)
        self.hosted_at = kwargs.get('hosted_at', None)

        if self.embed_code is None:
            raise OoyalaParameterException('embed_code')


class OoyalaLabelManage(OoyalaRequest):
    """ Allows full management of labels for backlot. Create/delete/rename and assign
        API Definition: http://www.ooyala.com/support/docs/backlot_api#label
    """

    def __init__(self, **kwargs):
        super(OoyalaLabelManage, self).__init__(OoyalaAPI.BACKLOT.LABEL, OoyalaAPI.BACKLOT.URL)

        self.mode = kwargs.get('mode', None)


class OoyalaChannel(OoyalaRequest):
    """ Allows listing of channels & getting embedcodes - best used for
        getting the content for certain pages and sections. mode and the
        channelEmbedCode are required.
        API Definition: http://www.ooyala.com/support/docs/backlot_api#channel
    """

    def __init__(self, embed_code, **kwargs):
        super(OoyalaChannel, self).__init__(OoyalaAPI.BACKLOT.CHANNEL, OoyalaAPI.BACKLOT.URL)

        self.mode = kwargs.get('mode', O.CHANNEL_MODE.LIST)
        self.embed_code = embed_code

class OoyalaAnalytics(OoyalaRequest):
    """ Performs an analytic request for data either on the whole account or
        specific sets of embed_codes.
        API Definition: http://www.ooyala.com/support/docs/backlot_api#channel
    """

    def __init__(self, **kwargs):
        super(OoyalaAnalytics, self).__init__(OoyalaAPI.ANALYTICS.ANALYTICS, OoyalaAPI.ANALYTICS.URL)

        self.date = kwargs.get('date', str(datetime.date.today()))
        self.granularity = kwargs.get('granularity', O.GRANULATIRY.TOTAL)
        self.method = kwargs.get('method', O.ANALYTIC_METHODS.TOTALS)
        self.video = kwargs.get('video', None)



