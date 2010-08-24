from django.core.management.base import BaseCommand
import sys

from ooyala.models import OoyalaItem, OoyalaChannelList
from ooyala.library import OoyalaChannel

class Command(BaseCommand):
    help = 'Loops over all OoyalaItems which are channels and creates ' + \
        'channel lists for them. You must have already imported items.'

    def handle(self, *args, **kwargs):
        req = OoyalaChannel()



