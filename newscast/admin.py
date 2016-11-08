from __future__ import division
from django.conf import settings
from django.contrib import admin
from django import forms
from ballot_box.models import *
from newscast.models import *
import logging

logger = logging.getLogger("kpcc_backroom_handshakes")

class ContestForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ContestForm, self).__init__(*args, **kwargs)
        contests = Contest.objects.filter(election__electionid="general-2016-11-08")
        w = self.fields['contest'].widget
        choices = []
        for item in contests:
            if item.is_ballot_measure == False:
                choices.append((item.id, item.contestname))
            else:
                for measure in item.ballotmeasure_set.all():
                    measure.fullname = "%s (%s)" % (measure.fullname, item.contestname)
                    choices.append((item.id, measure.fullname))
        w.choices = choices


class TopicAdmin(admin.ModelAdmin):

    list_display = (
        "topicname",
        "election",
        "created",
    )

    list_per_page = 15

    list_filter = ("topicname",)

    ordering = ("topicname",)

    save_on_top = True

    save_as = True

    filter_horizontal = ("contest",)

    form = ContestForm

    prepopulated_fields = {
        "topicslug": ("topicname",)
    }

    fields = (
        "election",
        "contest",
        "topicname",
        "topicslug",
        "description",
    )


class ContextAdmin(admin.ModelAdmin):

    list_display = (
        "contestid",
        "election",
    )

    list_per_page = 15

    list_filter = ("election",)

    search_fields = ("contestid",)

    ordering = ("contestid",)

    save_on_top = True

    save_as = True

    fields = (
        "election",
        "contestid",
        "cities_counties_list",
        "description",
    )

admin.site.register(Topic, TopicAdmin)
admin.site.register(ContestContext, ContextAdmin)
