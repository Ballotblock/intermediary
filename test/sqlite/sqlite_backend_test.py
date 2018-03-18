#!/usr/bin/env python3
#
# test/sqlite3/test_sqlite3_backend
# Authors:
#     Samuel Vargas

from src.sqlite.sqlite_backend_io import SQLiteBackendIO
import datetime
import time
import unittest
import uuid
import json


class SQLite3BackendTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.backend_io = SQLiteBackendIO(":memory:")

        now = int(time.time())
        ten_days_later = int((datetime.datetime.fromtimestamp(now) + datetime.timedelta(days=10)).timestamp())

        self.questions = [
            ["Do you like Fishsticks?", ["Yes", "No"]],
            ["Red or Blue Pill?:", ["Red", "Blue"]]
        ]

        self.answers = [
            ["Yes", "Red"]
        ]

        election_title = "Example Election"

        self.election = {
            "election_title": election_title,
            "description": "This is an example election",
            "start_date": now,
            "end_date": ten_days_later,
            "creator_id": str(uuid.uuid4()),
            "master_ballot_title": election_title
        }

        self.master_ballot = {
            "master_ballot_title": election_title,
            "questions": json.dumps(self.questions),
        }

        self.ballot = {
            "ballot_id": str(uuid.uuid4()),
            "answers": json.dumps(self.answers),
            "master_ballot_title": election_title
        }

    def test_a_add_single_election(self):
        # Add our election to the table
        self.backend_io.create_election(self.master_ballot, self.election)

        # Verify that we are able to retrieve our added election
        election_title = self.election['election_title']
        retrieved_election = self.backend_io.get_election_by_title(election_title)
        assert retrieved_election is not None, \
            "An election with title {0} should have been stored in the database".format(election_title)

        # Verify retrieved election data was stored correctly
        assert retrieved_election['election_title'] == self.election['election_title']
        assert retrieved_election['description'] == self.election['description']
        assert retrieved_election['start_date'] == self.election['start_date']
        assert retrieved_election['end_date'] == self.election['end_date']
        assert retrieved_election['creator_id'] == self.election['creator_id']
        assert retrieved_election['master_ballot_title'] == self.election['master_ballot_title']

        # Verify that we are able to retrieve our added master_ballot
        retrieved_master_ballot = self.backend_io.get_master_ballot_by_title(election_title)
        assert retrieved_master_ballot is not None, \
            "A master ballot with the title {0} should have been stored in the database".format(election_title)

        # Verify retrieved master ballot data was stored correctly
        assert retrieved_master_ballot["master_ballot_title"] == self.master_ballot["master_ballot_title"]
        assert retrieved_master_ballot["questions"] == self.master_ballot["questions"]

    def test_b_add_single_ballot_to_election(self):
        # Add a single ballot to the previously created election
        self.backend_io.create_ballot(self.ballot)

        #  Verify that we are able to retrieve the ballot we just created
        retrieved_ballot = self.backend_io.get_ballot_by_id(self.ballot["ballot_id"])
        assert retrieved_ballot is not None, \
            "A ballot with id {0} should have been stored in the database".format(self.ballot["ballot_id"])

        # Verify retrieved ballot data was stored correctly.
        assert retrieved_ballot["ballot_id"] == self.ballot["ballot_id"]
        assert retrieved_ballot["answers"] == self.ballot["answers"]
        assert retrieved_ballot["master_ballot_title"] == self.ballot["master_ballot_title"]

    def test_c_election_with_dupe_election_title_not_added(self):
        # Attempt to add the same election / master ballot again fails
        self.failUnlessRaises(ValueError, self.backend_io.create_election, self.master_ballot, self.election)

