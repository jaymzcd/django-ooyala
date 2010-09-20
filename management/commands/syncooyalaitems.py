# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import sys

from ooyala.models import OoyalaItem
from ooyala.library import OoyalaQuery

class Command(BaseCommand):
    help = 'Imports all channel and video content from Ooyala to the admin'

    def handle(self, *args, **kwargs):
        req = OoyalaQuery(page_id=730)
        ooyala_response = req.process()
        count = 0

        if type(ooyala_response)!=str:
            items = ooyala_response.getElementsByTagName('item')
            for item in items:
                [ooyala_item, created] = OoyalaItem.from_xml(item)
                try:
                    if created:
                        count += 1
                        sys.stdout.write('Added %s (%s)\n' % (str(ooyala_item.title), ooyala_item.content_type))
                    else:
                        print "Skipping %s" % str(ooyala_item.title)
                except UnicodeEncodeError:
                    print 'decode error for title'
        else:
            sys.stdout.write('Problem getting the data from ooyala, retrying...\n')
            self.handle(self, *args, **kwargs)

        sys.stdout.write('\nCOMPLETE: All items imported - %d in total\n\n' % count)

