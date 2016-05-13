from __future__ import unicode_literals
from django.db import models
from kpcc_backroom_handshakes.custom_fields import ListField
import logging

logger = logging.getLogger("kpcc_backroom_handshakes")

class Election(models.Model):
    """
    describes an election that will have results we want to capture
    """
    PRIMARY = "Primary"
    GENERAL = "General"
    SPECIAL = "Special"

    ELECTION_TYPE_CHOICES = (
        (PRIMARY, "Primary"),
        (GENERAL, "General"),
        (SPECIAL, "Special"),
    )

    type = models.CharField(
        "Type of Election",
        max_length=255,
        choices=ELECTION_TYPE_CHOICES,
        default=PRIMARY,
    )

    electionid = models.CharField(
        "Election ID", max_length=255, null=True, blank=True)
    test_results = models.BooleanField("Are These Test Results", default=False)
    live_results = models.BooleanField("Are These Live Results", default=False)
    election_date = models.DateField(
        "Date of the Election", null=True, blank=True)
    poll_close_at = models.DateTimeField(
        "Time the Polls Close", null=True, blank=True)
    national = models.BooleanField(
        "Is this a National Election?", default=False)
    # parsed_json
    # next_request
    # datafile
    # results_level
    created = models.DateTimeField("Date Created", auto_now_add=True)
    modified = models.DateTimeField("Date Modified", auto_now=True)

    def __unicode__(self):
        return self.electionid

    def save(self, *args, **kwargs):
        # if not self.electionid:
        #     self.election_date_str = self.election_date.strftime("%Y-%m-%d")
        #     self.electionid = "%s-%s" % (self.type.lower(), self.election_date_str)
        super(Election, self).save(*args, **kwargs)


class ResultSource(models.Model):
    """
    describes a source of data for election results
    """
    election = models.ForeignKey(Election)
    source_name = models.CharField(
        "Name Of Data Source", db_index=True, unique=True, max_length=255)
    source_short = models.CharField("Shortname Of Data Source", max_length=5)
    source_slug = models.SlugField(
        "Slugged Data Soure", db_index=True, unique=True, max_length=255, null=True, blank=True)
    source_url = models.URLField(
        "Url To Data Source", max_length=1024, null=True, blank=True)
    source_active = models.BooleanField("Active Data Source?", default=False)
    source_type = models.CharField(
        "Ext Of File Or Type Of Source", max_length=255, null=False, blank=False)
    source_files = ListField("Results Files We Want", null=True, blank=True)
    source_created = models.DateTimeField("Date Created", auto_now_add=True)
    source_modified = models.DateTimeField("Date Modified", auto_now=True)

    def __unicode__(self):
        return self.source_name

    def save(self, *args, **kwargs):
        super(ResultSource, self).save(*args, **kwargs)


class Office(models.Model):
    """
    describes the thing that a candidate is campaigning for
    """
    name = models.CharField("Name Of The Office",
                            max_length=255, null=False, blank=False)
    slug = models.SlugField("Slug Of The Office",
                            unique=True, max_length=255, null=True, blank=True)
    active = models.BooleanField("Is This Office Active?", default=False)
    created = models.DateTimeField("Date Created", auto_now_add=True)
    modified = models.DateTimeField("Date Modified", auto_now=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Office, self).save(*args, **kwargs)


class Contest(models.Model):
    """
    describes the thing that the electorate is casting votes for
    """
    election = models.ForeignKey(Election)
    resultsource = models.ForeignKey(ResultSource)
    office = models.ForeignKey(Office)
    contestid = models.CharField(
        "Contest ID", max_length=255, null=True, blank=True)
    contestname = models.CharField(
        "Display Reference To This Contest", max_length=255, null=False, blank=False)
    seatnum = models.IntegerField(
        "Number of district or seat up for grabs", null=True, blank=True)
    contestdescription = models.TextField(
        "Description Of This Contest", null=True, blank=True)
    is_uncontested = models.BooleanField("Uncontested Contest?", default=False)
    is_national = models.BooleanField("National Contest?", default=False)
    is_statewide = models.BooleanField("Statewide Contest?", default=False)
    is_ballot_measure = models.BooleanField("Is A Measure?", default=False)
    is_judicial = models.BooleanField("Is Judicial Contest?", default=False)
    is_runoff = models.BooleanField("Is A Runoff Contest?", default=False)
    precinctstotal = models.IntegerField(
        "Total Number Of Precincts", null=True, blank=True)
    precinctsreporting = models.IntegerField(
        "Number Of Precincts Reporting Votes", null=True, blank=True)
    precinctsreportingpct = models.FloatField(
        "Percent Of Precincts Reporting", null=True, blank=True)
    votersregistered = models.FloatField(
        "Number of Registered Voters", null=True, blank=True)
    votersturnout = models.FloatField(
        "Percent Voters Who Cast Ballots", null=True, blank=True)
    created = models.DateTimeField("Date Created", auto_now_add=True)
    modified = models.DateTimeField("Date Modified", auto_now=True)

    def __unicode__(self):
        return self.contestname

    def save(self, *args, **kwargs):
        # if self.pk is None and not self.contestid:
        #     self.contestid = "%s-%s" % (self.election.electionid, self.office.slug)
        # elif not self.contestid:
        #     self.contestid = "%s-%s" % (self.election.electionid, self.office.slug)
        super(Contest, self).save(*args, **kwargs)


class Candidate(models.Model):
    """
    describes a person running for office
    """
    contest = models.ForeignKey(Contest)
    candidateid = models.CharField(
        "Candidate ID", max_length=255, null=True, blank=True)
    ballotorder = models.IntegerField(
        "Numerical Position On The Ballot", null=True, blank=True)
    firstname = models.CharField(
        "Candidate's First Name", max_length=255, null=True, blank=True)
    lastname = models.CharField(
        "Candidate's Last Name", max_length=255, null=True, blank=True)
    fullname = models.CharField(
        "Candidate's Full Name", max_length=255, null=True, blank=True)
    party = models.CharField(
        "Political Party", max_length=255, null=True, blank=True)
    incumbent = models.BooleanField(
        "Is Candidate An Incumbent?", default=False)
    votecount = models.IntegerField(
        "Votes Received", null=True, blank=True)
    votepct = models.FloatField(
        "Percent Of Total Votes", null=True, blank=True)
    created = models.DateTimeField("Date Created", auto_now_add=True)
    modified = models.DateTimeField("Date Modified", auto_now=True)

    def __unicode__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        # if self.pk is None and not self.fullname:
        #     self.fullname = "%s %s" % (self.firstname, self.lastname)
        #     self.slugname = "%s-%s" % (self.firstname.lower(), self.lastname.lower())
        #     self.candidateid = "%s-%s" % (self.contest.contestid, self.slugname)
        # elif not self.fullname:
        #     self.fullname = "%s %s" % (self.firstname, self.lastname)
        #     self.slugname = "%s-%s" % (self.firstname.lower(), self.lastname.lower())
        #     self.candidateid = "%s-%s" % (self.contest.contestid, self.slugname)
        super(Candidate, self).save(*args, **kwargs)


class BallotMeasure(models.Model):
    """
    describes a measure that can be voted on
    """
    contest = models.ForeignKey(Contest)
    measureid = models.CharField(
        "Measure ID", max_length=255, null=False, blank=False)
    ballotorder = models.IntegerField(
        "Numerical Position On The Ballot", null=True, blank=True)
    fullname = models.CharField(
        "Name of Ballot Measure", max_length=255, null=False, blank=False)
    description = models.TextField(
        "Description Of Ballot Measure", null=True, blank=True)
    yescount = models.IntegerField(
        "Number Of Yes Votes Received", null=True, blank=True)
    yespct = models.FloatField(
        "Percent Of Yes Votes Received", null=True, blank=True)
    nocount = models.IntegerField(
        "Number Of Yes Votes Received", null=True, blank=True)
    nopct = models.FloatField(
        "Percent Of Yes Votes Received", null=True, blank=True)
    created = models.DateTimeField("Date Created", auto_now_add=True)
    modified = models.DateTimeField("Date Modified", auto_now=True)

    def __unicode__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        super(BallotMeasure, self).save(*args, **kwargs)


class JudicialCandidate(models.Model):
    """
    describes a measure that can be voted on
    """
    contest = models.ForeignKey(Contest)
    judgeid = models.CharField(
        "Judicial Candidate ID", max_length=255, null=False, blank=False)
    ballotorder = models.IntegerField(
        "Numerical Position On The Ballot", null=True, blank=True)
    firstname = models.CharField(
        "Candidate's First Name", max_length=255, null=True, blank=True)
    lastname = models.CharField(
        "Candidate's Last Name", max_length=255, null=True, blank=True)
    fullname = models.CharField(
        "Candidate's Last Name", max_length=255, null=False, blank=False)
    yescount = models.IntegerField(
        "Number Of Yes Votes Received", null=True, blank=True)
    yespct = models.FloatField(
        "Percent Of Yes Votes Received", null=True, blank=True)
    nocount = models.IntegerField(
        "Number Of Yes Votes Received", null=True, blank=True)
    nopct = models.FloatField(
        "Percent Of Yes Votes Received", null=True, blank=True)
    created = models.DateTimeField("Date Created", auto_now_add=True)
    modified = models.DateTimeField("Date Modified", auto_now=True)

    def __unicode__(self):
        return self.fullname

    def save(self, *args, **kwargs):
        if self.pk is None and not self.judgeid:
            self.fullname = "%s %s" % (self.firstname, self.lastname)
            self.slugname = "%s-%s" % (self.firstname.lower(), self.lastname.lower())
            self.judgeid = "%s-%s" % (self.contest.contestid, self.slugname)
        elif not self.judgeid:
            self.fullname = "%s %s" % (self.firstname, self.lastname)
            self.slugname = "%s-%s" % (self.firstname.lower(), self.lastname.lower())
            self.judgeid = "%s-%s" % (self.contest.contestid, self.slugname)
        super(JudicialCandidate, self).save(*args, **kwargs)


# class ReportingUnit(models.Model):
#     """
#     describes an entity that contains precincts and reports voting results
#     """
#     election = models.ForeignKey(Election)
#     contest = models.ForeignKey(Contest)
#     reportingunitname = models.CharField(
#         "Name Of The Reporing Entity", max_length=255, null=False, blank=False)
#     reportingunitslug = models.SlugField(
#         "Slug Of The Reporing Entity", db_index=True, unique=True, max_length=255, null=True, blank=True)
#     # delegatecount
#     # winner
#     # fipscode
#     precinctstotal = models.IntegerField(
#         "Total Number Of Precincts", null=True, blank=True)
#     precinctsreporting = models.IntegerField(
#         "Number Of Precincts That Have Reported Votes", null=True, blank=True)
#     precinctsreportingpct = models.FloatField(
#         "Percent Of Precincts Reporting", null=True, blank=True)
#     votersregistered = models.FloatField(
#         "Number of Registered Voters", null=True, blank=True)
#     votersturnout = models.FloatField(
#         "Percent Of Registered Voters Who Cast Ballots", null=True, blank=True)
#     statename = models.CharField(
#         "Name Of The Reporing Entity's State", max_length=255, null=False, blank=False)
#     statepostal = models.CharField(
#         "Postal Code Of The Reporing Entity's State", max_length=2, null=False, blank=False)
#     description = models.TextField(
#         "Description Of Ballot Measure", null=True, blank=True)
#     created = models.DateTimeField("Date Created", auto_now_add=True)
#     modified = models.DateTimeField("Date Modified", auto_now=True)

#     def __unicode__(self):
#         return self.reportingunitname

#     def save(self, *args, **kwargs):
#         super(ReportingUnit, self).save(*args, **kwargs)
