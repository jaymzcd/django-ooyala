# -*- coding: utf-8 -*-
from django.core.management.base import BaseCommand
import sys

from ooyala.models import OoyalaItem
from ooyala.library import OoyalaQuery

class Command(BaseCommand):
    help = 'Imports all channel and video content from Ooyala to the admin'

    def handle(self, *args, **kwargs):
        count = 0
        total = 0
        i = 1
        retries_left = 5
        while True:
            req = OoyalaQuery(page_id=i)
            ooyala_response = req.process()

            if type(ooyala_response) != str:
                items = ooyala_response.getElementsByTagName('item')
                if not items:
                    print 'No more items after %d' % i
                    break
                else:
                    print '%d items from offset %s' % (len(items), i)
                total += len(items)
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
                retries_left -= 1
                if retries_left <= 0:
                    print 'TOO MANY RETRIES GIVING UP!'
                    break
                continue

            i += 500

        sys.stdout.write('\nCOMPLETE: All items imported - %d imported out of %s in total\n\n' % (count, total))

