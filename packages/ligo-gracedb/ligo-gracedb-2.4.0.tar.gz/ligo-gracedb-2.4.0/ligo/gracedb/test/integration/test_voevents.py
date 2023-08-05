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
import unittest
import os
from .base import TestGraceDb
from xml.etree import ElementTree as ET


class TestVOEvents(TestGraceDb):
    """Integration tests for VOEvents"""

    @classmethod
    def setUpClass(cls):
        super(TestVOEvents, cls).setUpClass()

        # Create event and get its graceid
        eventFile = os.path.join(cls.TEST_DATA_DIR, "cbc-lm.xml")
        r = cls._gracedb.createEvent("Test", "gstlal", eventFile, "LowMass")
        event = r.json()
        cls._graceid = event['graceid']

        # Upload fake skymap file to use later
        r = cls._gracedb.writeLog(
            cls._graceid, "Fake skymap file.", filename="fake_skymap.txt",
            filecontents="Fake skymap.", tagname="sky_loc"
        )

    # Helper functions --------------------------------------------------------
    def get_citations_dict(self, graceid, voevent_filename):
        """Gets a dictionary of ivorns and citation types"""

        # Get voevent file
        voevent_file_text = self._gracedb.files(
            graceid, voevent_filename
        ).read()

        # Parse XML
        voevent_xml = ET.fromstring(voevent_file_text)
        citations_dict = {}
        for citations in voevent_xml.iterfind('Citations'):
            for e in citations.iterfind('EventIVORN'):
                ivorn = e.text
                citations_dict[ivorn] = e.attrib['cite']
        return citations_dict

    def get_ivorn(self, graceid, voevent_filename):
        """Extracts ivorn"""
        # Get voevent file
        voevent_file_text = self._gracedb.files(
            graceid, voevent_filename
        ).read()
        return ET.fromstring(voevent_file_text).get('ivorn')

    # Tests -------------------------------------------------------------------
    def test_create_preliminary_voevent(self):
        """Create a preliminary VOEvent"""
        r = self._gracedb.createVOEvent(self._graceid, "Preliminary")
        rdict = r.json()
        self.assertTrue('voevent_type' in list(rdict))

    def test_retrieve_preliminary_voevent(self):
        """Retrieve preliminary VOEvent"""
        r = self._gracedb.voevents(self._graceid)
        voevent_list = r.json()['voevents']
        self.assertTrue(len(voevent_list) == 1)
        self.assertEqual(voevent_list[0]['voevent_type'], 'PR')

    def test_create_update_voevent(self):
        """Create an update VOEvent"""
        r = self._gracedb.createVOEvent(
            self._graceid, "Update", skymap_filename="fake_skymap.txt",
            skymap_type="FAKE", ProbHasRemnant=0.2, BBH=0.1, Terrestrial=0.3,
            MassGap=0.4
        )
        rdict = r.json()
        self.assertTrue('voevent_type' in list(rdict))

    def test_ivorns_unique(self):
        """Compare ivorns for preliminary and update VOEvents"""
        r = self._gracedb.voevents(self._graceid)
        voevent_list = r.json()['voevents']
        # Make sure there are 2 voevents
        self.assertTrue(len(voevent_list) == 2)

        # Make sure the ivorns are different
        voevent_dict = {v['voevent_type']: v for v in voevent_list}
        preliminary_ivorn = self.get_ivorn(
            self._graceid, voevent_dict['PR']['filename']
        )
        update_ivorn = self.get_ivorn(
            self._graceid, voevent_dict['UP']['filename']
        )
        self.assertNotEqual(preliminary_ivorn, update_ivorn)

    def test_citation_section(self):
        """Test VOEvent citations"""
        r = self._gracedb.voevents(self._graceid)
        voevent_list = r.json()['voevents']

        voevent_dict = {v['voevent_type']: v for v in voevent_list}
        preliminary_ivorn = self.get_ivorn(
            self._graceid, voevent_dict['PR']['filename']
        )
        update_citations = self.get_citations_dict(
            self._graceid, voevent_dict['UP']['filename']
        )
        self.assertEqual(update_citations[preliminary_ivorn], 'supersedes')

    def test_create_retraction_voevent(self):
        """Create a retraction VOEvent"""
        r = self._gracedb.createVOEvent(self._graceid, "Retraction")
        rdict = r.json()
        self.assertTrue('voevent_type' in list(rdict))

    def test_retraction_citations(self):
        """Test retraction VOEvent citations"""
        r = self._gracedb.voevents(self._graceid)
        voevent_list = r.json()['voevents']
        voevent_dict = {v['voevent_type']: v for v in voevent_list}

        # Parse retraction voevent and check for correct citations
        retraction_citations = self.get_citations_dict(
            self._graceid, voevent_dict['RE']['filename']
        )
        preliminary_ivorn = self.get_ivorn(
            self._graceid, voevent_dict['PR']['filename']
        )
        update_ivorn = self.get_ivorn(
            self._graceid, voevent_dict['UP']['filename']
        )
        self.assertEqual(retraction_citations[preliminary_ivorn], 'retraction')
        self.assertEqual(retraction_citations[update_ivorn], 'retraction')


# Define a custom test suite because there is some dependency between
# the successive individual tests; as a result, the order is important.
def VOEventTestSuite():
    suite = unittest.TestSuite()
    suite.addTest(TestVOEvents('test_create_preliminary_voevent'))
    suite.addTest(TestVOEvents('test_retrieve_preliminary_voevent'))
    suite.addTest(TestVOEvents('test_create_update_voevent'))
    suite.addTest(TestVOEvents('test_ivorns_unique'))
    suite.addTest(TestVOEvents('test_citation_section'))
    suite.addTest(TestVOEvents('test_create_retraction_voevent'))
    suite.addTest(TestVOEvents('test_retraction_citations'))
    return suite
