# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import sys

from ooyala.models import OoyalaItem
from ooyala.library import OoyalaQuery

class Command(BaseCommand):
    help = 'Imports all channel and video content from Ooyala to the admin'

    def handle(self, *args, **kwargs):
        VIDEOS_PER_PAGE = 500
        count = 0
        offset = 1
        retries_left = 5
        while True:
            req = OoyalaQuery(page_id=offset, fields=O.OOYALA_FIELDS_METADATA)
            ooyala_response = req.process()

            if not isinstance(ooyala_response, basestring):
                items = ooyala_response.getElementsByTagName('item')
                if items:
                    sys.stdout.write('Found items %d - %d\n' % (offset, offset+len(items)-1))
                else:
                    #No more items
                    break
                for item in items:
                    [ooyala_item, created] = OoyalaItem.from_xml(item)
                    try:
                        if created:
                            count += 1
                            sys.stdout.write('Added %s (%s)\n' % (str(ooyala_item.title), ooyala_item.content_type))
                        else:
                            sys.stdout.write("Skipping %s\n" % str(ooyala_item.title))
                            pass
                    except UnicodeEncodeError:
                        sys.stdout.write('Decode error for title\n')
                if len(items) < VIDEOS_PER_PAGE:
                    #This was the last page of items
                    break
            else:
                sys.stdout.write('Problem getting the data from ooyala, retrying...\n')
                retries_left -= 1
                if retries_left <= 0:
                    sys.stdout.write('TOO MANY RETRIES GIVING UP!\n')
                    break
                continue # keep same offset

            offset += VIDEOS_PER_PAGE


        sys.stdout.write('\nCOMPLETE: All items imported - %s in total\n\n' % count)

