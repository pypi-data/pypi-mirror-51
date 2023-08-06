# Copyright (C) 2018  The Software Heritage developers
# See the AUTHORS file at the top-level directory of this distribution
# License: GNU General Public License version 3, or any later version
# See top-level LICENSE file for more information

import datetime
import logging

from swh.model.hashutil import hash_to_bytes

from swh.loader.core.loader import BufferedLoader, UnbufferedLoader

from . import BaseLoaderTest


class DummyLoader:
    def cleanup(self):
        pass

    def prepare(self):
        pass

    def fetch_data(self):
        pass

    def store_data(self):
        pass

    def prepare_origin_visit(self):
        origin = self.storage.origin_get(
            self._test_prepare_origin_visit_data['origin'])
        self.origin = origin
        self.origin_url = origin['url']
        self.visit_date = datetime.datetime.utcnow()
        self.storage.origin_visit_add(origin['id'], self.visit_date)

    def parse_config_file(self, *args, **kwargs):
        return {
            'storage': {
                'cls': 'memory',
                'args': {
                }
            },

            'send_contents': True,
            'send_directories': True,
            'send_revisions': True,
            'send_releases': True,
            'send_snapshot': True,

            'content_packet_size': 2,
            'content_packet_size_bytes': 8,
            'directory_packet_size': 2,
            'revision_packet_size': 2,
            'release_packet_size': 2,

            'content_size_limit': 10000,
        }


class DummyUnbufferedLoader(DummyLoader, UnbufferedLoader):
    pass


class DummyBufferedLoader(DummyLoader, BufferedLoader):
    pass


class DummyBaseLoaderTest(BaseLoaderTest):
    def setUp(self):
        self.loader = self.loader_class(logging_class='dummyloader')
        self.loader.visit_type = 'git'
        # do not call voluntarily super().setUp()
        self.storage = self.loader.storage
        contents = [
            {
                'id': '34973274ccef6ab4dfaaf86599792fa9c3fe4689',
                'sha1': '34973274ccef6ab4dfaaf86599792fa9c3fe4689',
                'sha1_git': b'bar1',
                'sha256': b'baz1',
                'blake2s256': b'qux1',
                'status': 'visible',
                'data': b'data1',
                'length': 5,
            },
            {
                'id': '61c2b3a30496d329e21af70dd2d7e097046d07b7',
                'sha1': '61c2b3a30496d329e21af70dd2d7e097046d07b7',
                'sha1_git': b'bar2',
                'sha256': b'baz2',
                'blake2s256': b'qux2',
                'status': 'visible',
                'data': b'data2',
                'length': 5,
            },
        ]
        self.expected_contents = [content['id'] for content in contents]
        self.in_contents = contents.copy()
        for content in self.in_contents:
            content['sha1'] = hash_to_bytes(content['sha1'])
        self.in_directories = [
            {'id': hash_to_bytes(id_)}
            for id_ in [
                '44e45d56f88993aae6a0198013efa80716fd8921',
                '54e45d56f88993aae6a0198013efa80716fd8920',
                '43e45d56f88993aae6a0198013efa80716fd8920',
            ]
        ]
        person = {
            'name': b'John Doe',
            'email': b'john.doe@institute.org',
            'fullname': b'John Doe <john.doe@institute.org>'
        }
        self.in_revisions = [
            {
                'id': b'rev1',
                'date': None,
                'author': person,
                'committer': person
            },
            {
                'id': b'rev2',
                'date': None,
                'author': person,
                'committer': person
            },
        ]
        self.in_releases = [
            {
                'id': b'rel1',
                'date': None,
                'author': person
            },
            {
                'id': b'rel2',
                'date': None,
                'author': person
            },
        ]
        self.in_origin = {
            'type': self.loader.visit_type,
            'url': 'http://example.com/',
        }
        self.in_snapshot = {
            'id': b'snap1',
            'branches': {},
        }
        self.in_provider = {
            'provider_name': 'Test Provider',
            'provider_type': 'test_provider',
            'provider_url': 'http://example.org/metadata_provider',
            'metadata': {'working': True},
        }
        self.in_tool = {
            'name': 'Test Tool',
            'version': 'v1.2.3',
            'configuration': {'in_the_Matrix': 'maybe'},
        }

        self.storage.origin_add([self.in_origin])

        # used by prepare_origin_visit() when it gets called
        self.loader._test_prepare_origin_visit_data = {
            'origin': self.in_origin,
        }

    def tearDown(self):
        # do not call voluntarily super().tearDown()
        pass


class CoreUnbufferedLoaderTest(DummyBaseLoaderTest):
    loader_class = DummyUnbufferedLoader

    def test_unbuffered_loader(self):
        self.loader.load()  # initialize the loader

        self.loader.send_contents(self.in_contents[0:1])
        self.loader.send_directories(self.in_directories[0:1])
        self.loader.send_revisions(self.in_revisions[0:1])
        self.loader.send_releases(self.in_releases[0:1])

        self.assertCountContents(1)
        self.assertCountDirectories(1)
        self.assertCountRevisions(1)
        self.assertCountReleases(1)

        self.loader.send_contents(self.in_contents[1:])
        self.loader.send_directories(self.in_directories[1:])
        self.loader.send_revisions(self.in_revisions[1:])
        self.loader.send_releases(self.in_releases[1:])

        self.assertCountContents(len(self.in_contents))
        self.assertCountDirectories(len(self.in_directories))
        self.assertCountRevisions(len(self.in_revisions))
        self.assertCountReleases(len(self.in_releases))


class CoreBufferedLoaderTest(DummyBaseLoaderTest):
    loader_class = DummyBufferedLoader

    def test_buffered_loader(self):
        self.loader.load()  # initialize the loader

        self.loader.maybe_load_contents(self.in_contents[0:1])
        self.loader.maybe_load_directories(self.in_directories[0:1])
        self.loader.maybe_load_revisions(self.in_revisions[0:1])
        self.loader.maybe_load_releases(self.in_releases[0:1])

        self.assertCountContents(0)
        self.assertCountDirectories(0)
        self.assertCountRevisions(0)
        self.assertCountReleases(0)

        self.loader.maybe_load_contents(self.in_contents[1:])
        self.loader.maybe_load_directories(self.in_directories[1:])
        self.loader.maybe_load_revisions(self.in_revisions[1:])
        self.loader.maybe_load_releases(self.in_releases[1:])

        self.assertCountContents(len(self.in_contents))
        self.assertCountDirectories(len(self.in_directories))
        self.assertCountRevisions(len(self.in_revisions))
        self.assertCountReleases(len(self.in_releases))

    def test_directory_cascade(self):
        """Checks that sending a directory triggers sending contents"""
        self.loader.load()  # initialize the loader

        self.loader.maybe_load_contents(self.in_contents[0:1])
        self.loader.maybe_load_directories(self.in_directories)

        self.assertCountContents(1)
        self.assertCountDirectories(len(self.in_directories))

    def test_revision_cascade(self):
        """Checks that sending a revision triggers sending contents and
        directories."""

        self.loader.load()  # initialize the loader

        self.loader.maybe_load_contents(self.in_contents[0:1])
        self.loader.maybe_load_directories(self.in_directories[0:1])
        self.loader.maybe_load_revisions(self.in_revisions)

        self.assertCountContents(1)
        self.assertCountDirectories(1)
        self.assertCountRevisions(len(self.in_revisions))

    def test_release_cascade(self):
        """Checks that sending a release triggers sending revisions,
        contents, and directories."""
        self.loader.load()  # initialize the loader

        self.loader.maybe_load_contents(self.in_contents[0:1])
        self.loader.maybe_load_directories(self.in_directories[0:1])
        self.loader.maybe_load_revisions(self.in_revisions[0:1])
        self.loader.maybe_load_releases(self.in_releases)

        self.assertCountContents(1)
        self.assertCountDirectories(1)
        self.assertCountRevisions(1)
        self.assertCountReleases(len(self.in_releases))

    def test_snapshot_cascade(self):
        """Checks that sending a snapshot triggers sending releases,
        revisions, contents, and directories."""
        self.loader.load()  # initialize the loader

        self.loader.maybe_load_contents(self.in_contents[0:1])
        self.loader.maybe_load_directories(self.in_directories[0:1])
        self.loader.maybe_load_revisions(self.in_revisions[0:1])
        self.loader.maybe_load_releases(self.in_releases[0:1])
        self.loader.maybe_load_snapshot(self.in_snapshot)

        self.assertCountContents(1)
        self.assertCountDirectories(1)
        self.assertCountRevisions(1)
        self.assertCountReleases(1)
        self.assertCountSnapshots(1)

    def test_origin_metadata(self):
        self.loader.load()

        provider_id = self.loader.send_provider(self.in_provider)
        tool_id = self.loader.send_tool(self.in_tool)

        self.loader.send_origin_metadata(
            self.loader.visit_date, provider_id,
            tool_id, {'test_metadata': 'foobar'})

        self.assertOriginMetadataContains(
            self.in_origin['type'], self.in_origin['url'],
            {'test_metadata': 'foobar'})

        with self.assertRaises(AssertionError):
            self.assertOriginMetadataContains(
                self.in_origin['type'], self.in_origin['url'],
                {'test_metadata': 'foobarbaz'})

        with self.assertRaises(Exception):
            self.assertOriginMetadataContains(
                self.in_origin['type'], self.in_origin['url'] + 'blah',
                {'test_metadata': 'foobar'})


def test_loader_logger_default_name():
    loader = DummyBufferedLoader()
    assert isinstance(loader.log, logging.Logger)
    assert loader.log.name == \
        'swh.loader.core.tests.test_loader.DummyBufferedLoader'

    loader = DummyUnbufferedLoader()
    assert isinstance(loader.log, logging.Logger)
    assert loader.log.name == \
        'swh.loader.core.tests.test_loader.DummyUnbufferedLoader'


def test_loader_logger_with_name():
    loader = DummyBufferedLoader('some.logger.name')
    assert isinstance(loader.log, logging.Logger)
    assert loader.log.name == \
        'some.logger.name'
