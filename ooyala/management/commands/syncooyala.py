from django.core.management.base import BaseCommand
import sys
import warnings

from ooyala.models import OoyalaItem
from ooyala.library import OoyalaQuery

class Command(BaseCommand):
    help = 'Imports all channel and video content from Ooyala to the admin'

    def handle(self, *args, **kwargs):
        warnings.warn("This command is now deprecated, use syncooyalaitems (and then syncooyalachannels)", DeprecationWarning)