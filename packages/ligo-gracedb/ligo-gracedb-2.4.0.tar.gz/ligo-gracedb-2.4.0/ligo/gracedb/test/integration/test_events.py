# -*- coding: utf-8 -*-
# Copyright (C) Brian Moe, Branson Stephens (2015)
#
# This file is part of gracedb
#
# gracedb is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# It is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with gracedb.  If not, see <http://www.gnu.org/licenses/>.
from __future__ import print_function
import random
import os
from datetime import datetime

from six.moves import range

from .base import TestGraceDb


class TestEvents(TestGraceDb):
    """Integration tests for event creation and annotation"""

    @classmethod
    def setUpClass(cls):
        # Create an event for testing so we don't have to create a lot of
        # events for all of the unit tests.
        super(TestEvents, cls).setUpClass()

        # For testing of labels and offline variable
        cls._labelName = "DQV"
        cls._offline = False

        # Create event and get its graceid
        cls._eventFile = os.path.join(cls.TEST_DATA_DIR, "cbc-lm.xml")
        cls._createdEvent = cls._gracedb.createEvent(
            "Test", "gstlal", cls._eventFile, "LowMass", offline=cls._offline
        ).json()
        cls._eventId = cls._createdEvent["graceid"]

    def test_root(self):
        """Did root resource retrieval succeed?"""
        self.assertTrue("CBC" in self._gracedb.groups)

    def test_get_events(self):
        """
        Get the events resource.
        Make sure first event looks like an event.
        """
        events = self._gracedb.events()
        for event in events:
            self.assertTrue('graceid' in event)
            break

    def test_create_log(self):
        """Create an event log message"""
        message = "Message is {0}".format(random.random())
        resp = self._gracedb.writeLog(self._eventId, message)
        self.assertEqual(resp.status, 201)
        new_log_uri = resp.getheader('Location')
        new_log = resp.json()
        self.assertEqual(new_log_uri, new_log['self'])
        check_new_log = self._gracedb.get(new_log_uri).json()
        self.assertEqual(check_new_log['comment'], message)

    def test_get_log(self):
        """Retrieve event log"""
        logs = self._gracedb.logs(self._eventId).json()
        self.assertTrue('numRows' in logs)

    def test_create_emobservation(self):
        """Create an EM observation entry."""
        comment = "Message is {0}".format(random.random())
        # Let's put in some made-up values
        raList = [1.0, 1.0, 1.0]
        raWidthList = 1.0
        decList = [1.0, 1.0, 1.0]
        decWidthList = 1.0
        dt = datetime(1900, 1, 1, 1, 1, 1)
        startTimeList = [dt.isoformat() for i in range(3)]
        durationList = 1.0
        resp = self._gracedb.writeEMObservation(
            self._eventId, 'Test', raList, raWidthList, decList, decWidthList,
            startTimeList, durationList, comment
        )
        self.assertEqual(resp.status, 201)
        new_emobservation_uri = resp.getheader('Location')
        new_emobservation = resp.json()
        self.assertEqual(new_emobservation_uri, new_emobservation['self'])
        check_new_emobservation = \
            self._gracedb.get(new_emobservation_uri).json()
        self.assertEqual(check_new_emobservation['comment'], comment)

    def test_get_emobservations(self):
        """Retrieve EM Observation List"""
        emos = self._gracedb.emobservations(self._eventId).json()
        self.assertTrue('numRows' in emos)

    def test_upload_large_file(self):
        """
        Upload a large file.
        Issue https://bugs.ligo.org/redmine/issues/951
        """
        uploadFile = os.path.join(self.TEST_DATA_DIR, "big.data")
        r = self._gracedb.writeLog(self._eventId, "FILE UPLOAD", uploadFile)
        self.assertEqual(r.status, 201)  # CREATED
        r_content = r.json()
        link = r_content['file']
        # Load file
        with open(uploadFile, 'rb') as fh:
            filecontents = fh.read()
        # Get file
        api_file = self._gracedb.get(
            self._gracedb.files(self._eventId).json()['big.data']
        ).read()

        # Check
        self.assertEqual(filecontents, api_file)
        self.assertEqual(filecontents, self._gracedb.get(link).read())

    def test_upload_file(self):
        """Upload and re-upload a file"""

        uploadFile = os.path.join(self.TEST_DATA_DIR, "upload.data")
        r = self._gracedb.writeLog(self._eventId, "FILE UPLOAD", uploadFile)
        self.assertEqual(r.status, 201)  # CREATED
        r_content = r.json()
        link = r_content['file']

        # Load file
        with open(uploadFile, 'rb') as fh:
            filecontents = fh.read()
        # Get file
        api_file = self._gracedb.get(
            self._gracedb.files(self._eventId).json()['upload.data']
        ).read()

        # Check
        self.assertEqual(filecontents, api_file)
        self.assertEqual(filecontents, self._gracedb.get(link).read())

        # Re-upload slightly different file.
        uploadFile2 = os.path.join(self.TEST_DATA_DIR, "upload2.data")
        r = self._gracedb.writeLog(
            self._eventId, "FILE UPLOAD", filename="upload2.data",
            filecontents=open(uploadFile2, 'r')
        )
        self.assertEqual(r.status, 201)  # CREATED
        r_content = r.json()
        link2 = r_content['file']

        # Load file
        with open(uploadFile2, 'rb') as fh:
            filecontents = fh.read()
        # Get file
        api_file = self._gracedb.get(
            self._gracedb.files(self._eventId).json()['upload2.data']
        ).read()

        # Check
        self.assertEqual(filecontents, api_file)
        self.assertEqual(filecontents, self._gracedb.get(link2).read())
        self.assertNotEqual(link, link2)

    def test_files(self):
        """Get file info"""
        r = self._gracedb.files(self._eventId)
        event = r.json()
        self.assertEqual(r.status, 200)
        self.assertTrue(isinstance(event, dict))

    def test_create_cwb(self):
        """Create a CWB event"""
        """burst-cwb.txt"""
        eventFile = os.path.join(self.TEST_DATA_DIR, "burst-cwb.txt")
        r = self._gracedb.createEvent("Test", "CWB", eventFile)
        self.assertEqual(r.status, 201)  # CREATED
        cwb_event = r.json()
        self.assertEqual(cwb_event['group'], "Test")
        self.assertEqual(cwb_event['pipeline'], "CWB")
        self.assertEqual(float(cwb_event['gpstime']), 1042312876.5090)

    def test_create_lowmass(self):
        """Create a Low Mass event"""
        """cbc-lm.xml"""
        # This is done with the initially created event.
        pass

    def test_create_mbta(self):
        """Create an MBTA event"""
        """cbc-mbta.xml"""
        eventFile = os.path.join(self.TEST_DATA_DIR, "cbc-mbta.xml")
        mbta_event = self._gracedb.createEvent(
            "Test", "MBTAOnline", eventFile
        ).json()
        self.assertEqual(mbta_event['group'], "Test")
        self.assertEqual(mbta_event['pipeline'], "MBTAOnline")
        self.assertEqual(float(mbta_event['gpstime']), 1078903329.421037)
        original_far = 4.006953918826065e-7
        self.assertTrue(
            (mbta_event['far'] - original_far) < original_far * 1e-14
        )

    def test_create_olib(self):
        """Create an oLIB event"""
        eventFile = os.path.join(self.TEST_DATA_DIR, "olib-test.json")
        event = self._gracedb.createEvent("Test", "oLIB", eventFile).json()
        self.assertEqual(event['group'], "Test")
        self.assertEqual(event['pipeline'], "oLIB")
        self.assertEqual(event['far'], 7.22e-06)
        self.assertEqual(
            event['extra_attributes']['LalInferenceBurst']['bci'],
            1.111
        )

    def test_create_spiir(self):
        """Create a spiir event"""
        eventFile = os.path.join(self.TEST_DATA_DIR, "spiir-test.xml")
        event = self._gracedb.createEvent("Test", "spiir", eventFile).json()
        self.assertEqual(event['group'], "Test")
        self.assertEqual(event['pipeline'], "spiir")
        self.assertEqual(event['far'], 3.27e-07)
        self.assertEqual(
            event['extra_attributes']['CoincInspiral']['mass'],
            3.98
        )

    def test_create_hardwareinjection(self):
        """Create a HardwareInjection event"""
        """sim-inj.xml"""
        eventFile = os.path.join(self.TEST_DATA_DIR, "sim-inj.xml")
        # Don't need to specify source_channel or destination_channel
        hardwareinjection_event = self._gracedb.createEvent(
            "Test", "HardwareInjection", eventFile, instrument="H1",
            source_channel="", destination_channel=""
        ).json()
        self.assertEqual(hardwareinjection_event['group'], "Test")
        self.assertEqual(
            hardwareinjection_event['pipeline'],
            "HardwareInjection"
        )
        self.assertEqual(hardwareinjection_event['instruments'], "H1")

    def test_replace_event(self):
        graceid = self._eventId

        old_event = self._gracedb.event(graceid).json()
        self.assertEqual(old_event['group'], "Test")
        self.assertEqual(old_event['search'], "LowMass")
        self.assertEqual(float(old_event['gpstime']), 971609248.151741)

        replacementFile = os.path.join(self.TEST_DATA_DIR, "cbc-lm2.xml")

        response = self._gracedb.replaceEvent(graceid, replacementFile)
        self.assertEqual(response.status, 202)

        new_event = self._gracedb.event(graceid).json()
        self.assertEqual(new_event['group'], "Test")
        self.assertEqual(new_event['search'], "LowMass")
        self.assertEqual(float(new_event['gpstime']), 971609249.151741)

    def test_upload_binary(self):
        """
        Test workaround for Python bug
        http://bugs.python.org/issue11898
        Raises exception if workaround fails.
        """
        uploadFile = os.path.join(self.TEST_DATA_DIR, "upload.data.gz")
        r = self._gracedb.writeLog(self._eventId, "FILE UPLOAD", uploadFile)
        self.assertEqual(r.status, 201)  # CREATED

    def test_unicode_param(self):
        """
        Test workaround for Python bug
        http://bugs.python.org/issue11898
        Raises exception if workaround fails.
        """
        uploadFile = os.path.join(self.TEST_DATA_DIR, "upload.data.gz")
        r = self._gracedb.writeLog(self._eventId, "FILE UPLOAD", uploadFile)
        self.assertEqual(r.status, 201)  # CREATED

    def test_label_event(self):
        """Label an event"""
        r = self._gracedb.writeLabel(self._eventId, self._labelName)
        self.assertEqual(r.status, 201)  # CREATED
        r = self._gracedb.labels(self._eventId, self._labelName)
        self.assertEqual(r.status, 200)
        label = r.json()
        self.assertEqual(self._labelName, label['name'])

    def test_remove_label_event(self):
        """Remove label added by test_label_event"""
        r = self._gracedb.removeLabel(self._eventId, self._labelName)
        self.assertEqual(r.status, 204)
        api_labels = self._gracedb.labels(self._eventId).json()['labels']
        label_list = [l['name'] for l in api_labels]
        self.assertNotIn(self._labelName, label_list)

    def test_offline_param(self):
        """
        Tests whether offline parameter is transmitted to database
        properly or not. Creates an event with offline=True and checks it;
        also checks createdEvent, which uses offline=False.
        """
        self.assertEqual(self._createdEvent['offline'], self._offline)
        r = self._gracedb.createEvent(
            "Test", "gstlal", self._eventFile, search="LowMass", offline=True
        )
        temp = r.json()
        self.assertEqual(temp['offline'], True)

    def test_logger(self):
        import logging
        import ligo.gracedb.rest
        import ligo.gracedb.logging

        logging.basicConfig()
        log = logging.getLogger('testing')
        log.propagate = False   # Don't write to console

        graceid = self._eventId

        handler = \
            ligo.gracedb.logging.GraceDbLogHandler(self._gracedb, graceid)
        try:
            log.addHandler(handler)
            try:
                message = "Message is {0}".format(random.random())
                log.warning(message)
            finally:
                log.removeHandler(handler)
        finally:
            # Close the log handler in order to join with the writing thread.
            handler.close()

        event_logs = self._gracedb.logs(graceid).read()
        self.assertTrue(message.encode() in event_logs)
