#!/usr/bin/env python3
#
# test/time_manager.py
# Authors:
#   Samuel Vargas
#

from dateutil.parser import *
from datetime import timezone
import datetime


class TimeManager:
    @staticmethod
    def get_current_time_as_iso_format_string():
        return datetime.datetime.now(timezone.utc).astimezone().isoformat()

    @staticmethod
    def get_current_time_plus_time_delta_in_days_as_iso_8601_str(days=None):
        assert days is not None
        return (datetime.datetime.now(timezone.utc).astimezone() + datetime.timedelta(days=1))\
            .isoformat()

    @staticmethod
    def election_in_progress(end_date_iso8601_str: str):
        now = datetime.datetime.now(timezone.utc).astimezone()
        end = parse(end_date_iso8601_str)
        return now < end
