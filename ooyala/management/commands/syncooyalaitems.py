# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import sys

from ooyala.models import OoyalaItem
from ooyala.library import OoyalaQuery

class Command(BaseCommand):
    help = 'Imports all channel and video content from Ooyala to the admin'

    def handle(self, *args, **kwargs):
        count = 0
        offset = 1
        retries_left = 5
        while True:
            req = OoyalaQuery(page_id=offset)
            ooyala_response = req.process()

            if not isinstance(ooyala_response, basestring):
                items = ooyala_response.getElementsByTagName('item')
                if not items:
                    sys.stdout.write('\nNo more items after offset %d\n' % offset)
                    break
                else:
                    sys.stdout.write('\nFound %d items from offset %s\n' % (len(items), offset))
                for item in items[:2]:
                    [ooyala_item, created] = OoyalaItem.from_xml(item)
                    try:
                        if created:
                            count += 1
                            sys.stdout.write('Added %s (%s)\n' % (str(ooyala_item.title), ooyala_item.content_type))
                        else:
                            sys.stdout.write("Skipping %s" % str(ooyala_item.title))
                    except UnicodeEncodeError:
                        sys.stdout.write('decode error for title')
            else:
                sys.stdout.write('Problem getting the data from ooyala, retrying...\n')
                retries_left -= 1
                if retries_left <= 0:
                    sys.stdout.write('TOO MANY RETRIES GIVING UP!')
                    break
                continue # keep same offset

            offset += 500

        sys.stdout.write('\nCOMPLETE: All items imported - %s in total\n\n' % count)

