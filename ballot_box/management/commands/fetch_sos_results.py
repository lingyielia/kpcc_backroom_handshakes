from django.conf import settings
from django.core.management.base import BaseCommand
import time
import datetime
import logging
from ballot_box.manager_sos_results import BuildSosResults

logger = logging.getLogger("kpcc_backroom_handshakes")

class Command(BaseCommand):
    help = "Begin request to secretary of state for latest election results"
    def handle(self, *args, **options):
        task_run = BuildSosResults()
        task_run._init()
        self.stdout.write("\nTask finished at %s\n" % str(datetime.datetime.now()))
