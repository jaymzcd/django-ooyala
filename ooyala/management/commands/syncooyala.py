from django.core.management.base import BaseCommand
from django.utils.encoding import smart_str
import sys

from ooyala.models import OoyalaItem
from ooyala.library import OoyalaQuery

class Command(BaseCommand):
    help = 'Imports all channel and video content from Ooyala to the admin'

    def handle(self, *args, **kwargs):
        req = OoyalaQuery()
        ooyala_response = req.process()
        count = 0

        if type(ooyala_response)!=str:
            items = ooyala_response.getElementsByTagName('item')
            for item in items:
                [ooyala_item, created] = OoyalaItem.from_xml(item)
                if created:
                    count += 1
                    s = """Added %s (%s)\n""" % (smart_str(ooyala_item.title, errors='replace'), ooyala_item.content_type)
                    sys.stdout.write(s)
        else:
            sys.stdout.write('Problem getting the data from ooyala, retrying...\n')
            self.handle(self, *args, **kwargs)

        sys.stdout.write('\nCOMPLETE: All items imported - %d in total\n\n' % count)
