from django.core.management.base import BaseCommand
from django.utils.encoding import smart_str
import sys

from ooyala.models import OoyalaItem, OoyalaChannelList
from ooyala.managers import OChanManager
from ooyala.library import OoyalaChannel

class Command(BaseCommand):
    help = 'Loops over all OoyalaItems which are channels and creates ' + \
        'channel lists for them. You must have already imported items.'

    def handle(self, *args, **kwargs):

        channels = OoyalaItem.ochan.all().filter(content_type='channel')\
            .values_list('embed_code', flat=True)

        count = 0
        for channel in channels:

            try:
                channel_obj = OoyalaItem.ochan.get(embed_code=channel)
                [channel_list, created] = OoyalaChannelList.objects.get_or_create(channel=channel_obj)
                req = OoyalaChannel(embed_code=channel)
                ooyala_response = req.process()

                if type(ooyala_response)!=str:
                    items = ooyala_response.getElementsByTagName('item')
                    sys.stdout.write('Pairing up OoyalaItems for channel: %s\n' % channel)
                    for item in items:
                        try:
                            e_code = item.getElementsByTagName('embedCode')[0].firstChild.nodeValue
                            channel_item = OoyalaItem.ochan.get(embed_code=e_code)
                            channel_list.videos.add(channel_item)
                            s = '\tAdding "%s" to channel items\n' % channel_item.title
                            sys.stdout.write(smart_str(s))                         
                        except OoyalaItem.DoesNotExist:
                            sys.stdout.write('\tCould not find OoyalaItem with embed_code %s for channel %s\n' \
                                % (e_code, channel))
                    channel_list.save()
                    count += 1
                else:
                    sys.stdout.write('Problem getting the data from ooyala for channel %s, retrying...\n' % channel)
                    self.handle(self, *args, **kwargs)

            except OoyalaItem.DoesNotExist:
                sys.stdout.write('Could not find channel item in OoyalaItems: %s' % channel)

        sys.stdout.write('\nCOMPLETE: All channel lists created- %d in total\n\n' % count)

