from unittest import TestCase

from microanalyser.importer import JSONImporter
from microanalyser.model import Service, Database, CommunicationPattern, MessageBroker, MessageRouter

class TestYMLloaderNodes(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_nodes.json'
        self.importer = JSONImporter()
        self.microtosca = self.importer.Import(file)

    def test_service(self):
        s1 = self.microtosca['my_service']
        self.assertIsInstance(s1, Service)
        self.assertEqual(s1.name, "my_service")
    
    def test_database(self):
        db = self.microtosca['my_database']
        self.assertIsInstance(db, Database)
        self.assertEqual(db.name, "my_database")
    
    def test_messagebroker(self):
        mb = self.microtosca['my_messagebroker']
        self.assertIsInstance(mb, MessageBroker)
        self.assertEqual(mb.name, "my_messagebroker")
    
    def test_messagerouter(self):
        mr = self.microtosca['my_messagerouter']
        self.assertIsInstance(mr, MessageRouter)
        self.assertEqual(mr.name, "my_messagerouter")

