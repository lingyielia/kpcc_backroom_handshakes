from __future__ import division
from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.db.models import Sum, F
from kpcc_backroom_handshakes.custom_fields import ListField
from ballot_box.utils_data import Framer, Checker
from election_registrar import models as registrar
from ballot_box import models as ballot_box
import logging

logger = logging.getLogger("kpcc_backroom_handshakes")

framer = Framer()
checker = Checker()

# Create your models here.
class Topic(models.Model):
    election = models.ForeignKey(registrar.Election)
    contest = models.ManyToManyField(ballot_box.Contest)
    topicname = models.CharField("Topic Name", db_index=True, unique=True, max_length=255, null=True, blank=True)
    topicslug = models.SlugField("Topic Slug", db_index=True, unique=True, max_length=255, null=True, blank=True)
    description = models.TextField("About This Topic", null=True, blank=True)
    created = models.DateTimeField("Date Created", auto_now_add=True)
    modified = models.DateTimeField("Date Modified", auto_now=True)

    def __unicode__(self):
        return self.topicname

    def save(self, *args, **kwargs):
        super(Topic, self).save(*args, **kwargs)