#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.utils.timezone import localtime
from ballot_box.models import *
from election_registrar.models import *
from ballot_box.utils_data import Framer, Checker
import logging
import time
import datetime
import os.path
import shutil
import pytz

logger = logging.getLogger("kpcc_backroom_handshakes")

checker = Checker()


class Saver(object):
    """
    """

    log_message = "\n*** My Import Messages ***\n"

    def make_office(self, office):
        """
        """
        log_message = ""
        try:
            obj, created = Office.objects.get_or_create(
                officeid=office["officeid"],
                defaults={
                    # "name": office["officename"],
                    "slug": office["officeslug"],
                    "active": office["active"],
                    "poss_error": False,
                }
            )
            if created:
                log_message += "* CREATED OFFICE: %s \n" % (office["officeslug"])
            else:
                log_message += "* %s exists\n" % (office["officeslug"])
        except Exception, exception:
            error_output = "%s %s" % (exception, office["officeslug"])
            logger.debug(error_output)
            raise
        return log_message

    def make_contest(self, office, contest):
        """
        """
        log_message = ""
        try:
            this_office = Office.objects.get(officeid=office["officeid"])
        except Exception, exception:
            error_output = "%s %s" % (exception, office["officeid"])
            logger.debug(error_output)
            raise
        try:
            obj, created = this_office.contest_set.update_or_create(
                election_id=contest["election_id"],
                resultsource_id=contest["resultsource_id"],
                contestid=contest["contestid"],
                defaults={
                    # don't overwrite admin edits
                    # "contestname": contest["contestname"],
                    # "contestdescription": contest["contestdescription"],
                    "seatnum": contest["seatnum"],
                    "is_uncontested": contest["is_uncontested"],
                    "is_national": contest["is_national"],
                    "is_statewide": contest["is_statewide"],
                    "is_ballot_measure": contest["is_ballot_measure"],
                    "is_judicial": contest["is_judicial"],
                    "reporttype": contest["reporttype"],
                    "precinctstotal": contest["precinctstotal"],
                    "precinctsreporting": contest["precinctsreporting"],
                    "precinctsreportingpct": contest["precinctsreportingpct"],
                    "votersregistered": contest["votersregistered"],
                    "votersturnout": contest["votersturnout"],
                    "poss_error": contest["poss_error"],
                }
            )
            if created:
                log_message += "\t* CREATED CONTEST: %s\n" % (contest["contestid"])
            else:
                log_message += "\t* %s exists but we updated figures\n" % (contest["contestid"])
        except Exception, exception:
            error_output = "%s %s" % (exception, contest["contestid"])
            logger.debug(error_output)
            raise
        return log_message

    def make_judicial(self, contest, judicial):
        """
        """
        log_message = ""
        try:
            this_contest = Contest.objects.get(contestid=contest["contestid"])
        except Exception, exception:
            error_output = "%s %s" % (exception, contest["contestid"])
            logger.debug(error_output)
            raise
        try:
            presave = this_contest.judicialcandidate_set.get(judgeid=judicial["judgeid"])
            if presave.yespct:
                preyespct = "%0.1f" % (presave.yespct * 100)
            else:
                preyespct = None
            if presave.nopct:
                prenopct = "%0.1f" % (presave.nopct * 100)
            else:
                prenopct = None
        except Exception, exception:
            error_output = "ALERT: %s" % (exception)
            logger.debug(error_output)
        try:
            obj, created = this_contest.judicialcandidate_set.update_or_create(
                judgeid=judicial["judgeid"],
                defaults={
                    "ballotorder": judicial["ballotorder"],
                    # don't overwrite admin edits
                    # "firstname": judicial["firstname"],
                    # "lastname": judicial["lastname"],
                    # "fullname": judicial["fullname"],
                    "yescount": judicial["yescount"],
                    "yespct": judicial["yespct"] / 100,
                    "nocount": judicial["nocount"],
                    "nopct": judicial["nopct"] / 100,
                    "poss_error": judicial["poss_error"],
                }
            )
            if created:
                log_message += "\t\t* CREATED JUDGE: %s\n" % (judicial["judgeid"])
            else:
                log_message += "\t\t* UPDATED %s: %s from %s%% to %s%%\n" % (this_contest.contestname, judicial["fullname"], prevotepct, judicial["votepct"])
        except Exception, exception:
            error_output = "%s %s" % (exception, judicial["judgeid"])
            logger.debug(error_output)
            raise
        return log_message

    def make_measure(self, contest, measure):
        """
        """
        log_message = ""
        try:
            this_contest = Contest.objects.get(contestid=contest["contestid"], election_id=contest["election_id"])
        except Exception, exception:
            error_output = "%s %s" % (exception, contest["contestid"])
            logger.debug(error_output)
            raise
        try:
            presave = this_contest.ballotmeasure_set.get(measureid=measure["measureid"])
            if presave.yespct:
                preyespct = "%0.1f" % (presave.yespct * 100)
            else:
                preyespct = None
            if presave.nopct:
                prenopct = "%0.1f" % (presave.nopct * 100)
            else:
                prenopct = None
        except Exception, exception:
            error_output = "ALERT: %s" % (exception)
            logger.debug(error_output)
        try:
            obj, created = this_contest.ballotmeasure_set.update_or_create(
                measureid=measure["measureid"],
                defaults={
                    "ballotorder": measure["ballotorder"],
                    # don't overwrite admin edits
                    # "fullname": measure["fullname"],
                    # "description": measure["description"],
                    "yescount": measure["yescount"],
                    "yespct": measure["yespct"] / 100,
                    "nocount": measure["nocount"],
                    "nopct": measure["nopct"] / 100,
                    "poss_error": measure["poss_error"],
                }
            )
            if created:
                log_message += "\t\t* CREATED MEASURE: %s\n" % (measure["measureid"])
            else:
                log_message += "\t\t* UPDATED %s:\n\t\t\t* Yes from %s%% to %s%%.\n\t\t\t* No from %s%% to %s%%.\n" % (this_contest.contestname, preyespct, measure["yespct"], prenopct, measure["nopct"])
        except Exception, exception:
            error_output = "%s %s" % (exception, measure["measureid"])
            logger.debug(error_output)
            raise
        return log_message

    def make_candidate(self, contest, candidate):
        """
        """
        log_message = ""
        try:
            this_contest = Contest.objects.get(contestid=contest["contestid"])
        except Exception, exception:
            error_output = "%s %s" % (exception, contest["contestid"])
            logger.debug(error_output)
            raise
        try:
            presave = this_contest.candidate_set.get(candidateid=candidate["candidateid"])
            if presave.votepct:
                prevotepct = "%0.1f" % (presave.votepct * 100)
            else:
                prevotepct = None
            if presave.party:
                candidate["party"] = presave.party
            else:
                pass
            if presave.incumbent:
                candidate["incumbent"] = presave.incumbent
            else:
                pass
        except Exception, exception:
            error_output = "ALERT: %s" % (exception)
            logger.debug(error_output)
        try:
            obj, created = this_contest.candidate_set.update_or_create(
                candidateid=candidate["candidateid"],
                defaults={
                    "ballotorder": candidate["ballotorder"],
                    # don't overwrite admin edits
                    # "firstname": candidate["firstname"],
                    # "lastname": candidate["lastname"],
                    # "fullname": candidate["fullname"],
                    "party": candidate["party"],
                    "incumbent": candidate["incumbent"],
                    "votecount": candidate["votecount"],
                    "votepct": candidate["votepct"] / 100,
                    "poss_error": candidate["poss_error"],
                }
            )
            if created:
                log_message += "\t\t* CREATED CANDIDATE: %s\n" % (candidate["candidateid"])
            else:
                outputname = candidate["fullname"].decode("utf8")
                log_message += "\t\t* UPDATED %s: %s from %s%% to %s%%\n" % (this_contest.contestname, outputname, prevotepct, candidate["votepct"])
        except Exception, exception:
            error_output = "%s %s" % (exception, candidate["candidateid"])
            logger.debug(error_output)
            raise
        return log_message

    def _eval_timestamps(self, file_time, database_time):
        """
        """
        fttz = localtime(file_time).tzinfo
        dbtz = localtime(database_time).tzinfo
        if fttz == None and dbtz == None:
            raise Exception
        elif fttz == None:
            raise Exception
        elif dbtz == None:
            raise Exception
        else:
            if fttz._tzname == "PDT" or fttz._tzname == "PST":
                if file_time > database_time:
                    return True
                else:
                    return False
            else:
                raise Exception

    def _update_result_timestamps(self, src, file_timestamp):
        """
        """
        obj = ResultSource.objects.get(source_slug=src.source_slug)
        obj.source_latest = file_timestamp
        obj.save(update_fields=["source_latest"])

    def _make_office_id(self, *args, **kwargs):
        """
        """
        framer = Framer()
        required_keys = [
            "source_short",
            "officeslug",
        ]
        if len(args) != len(required_keys):
            raise Exception
        else:
            pass
        if kwargs:
            args = list(args)
            # this needs work but it's a start
            args.append(kwargs.values()[0].lower())
            output = framer._concat(*args, delimiter="-")
        else:
            output = framer._concat(*args, delimiter="-")
        return output

    def _make_contest_id(self, *args, **kwargs):
        """
        """
        framer = Framer()
        required_keys = [
            # "electionid",
            "source_short",
            "level",
            "officeslug",
        ]
        if len(args) != len(required_keys):
            raise Exception
        else:
            pass
        if kwargs:
            args = list(args)
            # this needs work but it's a start
            args.append(str(kwargs.values()[0]).lower())
            output = framer._concat(*args, delimiter="-")
        else:
            output = framer._concat(*args, delimiter="-")
        return output

    def _make_this_id(self, contest_type, *args, **kwargs):
        """
        """
        framer = Framer()
        if contest_type == "measure":
            required_keys = [
                "contestid",
                "measure_id",
            ]
        elif contest_type == "judicial":
            required_keys = [
                "contestid",
                "judicialslug",
            ]
        elif contest_type == "candidate":
            required_keys = [
                "contestid",
                "candidateslug",
            ]
        if len(args) != len(required_keys):
            raise Exception
        else:
            pass
        if kwargs:
            args = list(args)
            # this needs work but it's a start
            args.append(str(kwargs.values()[0]).lower())
            output = framer._concat(*args, delimiter="-")
        else:
            output = framer._concat(*args, delimiter="-")
        return output
