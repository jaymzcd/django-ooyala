# -*- coding: utf-8 -*-
from django.template import RequestContext
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.http import HttpResponse
from datetime import datetime, date, timedelta

from ooyala.conf import *
from ooyala.library import OoyalaQuery, OoyalaLabelManage, OoyalaChannel, OoyalaAnalytics
from ooyala.constants import OoyalaConstants as O
from ooyala.models import OoyalaItem

@staff_member_required
def backlot_query(request):

    req = OoyalaQuery(page_id=500)

    ooyala_response = req.process()
    print ooyala_response

    print req.url
    if type(ooyala_response)!=str:
        items = ooyala_response.getElementsByTagName('item')
        return HttpResponse(ooyala_response.toprettyxml(), mimetype="text/xml")
    else:
        print "got an error back"

    return HttpResponse("tada")
