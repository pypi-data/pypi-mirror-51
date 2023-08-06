from unittest import TestCase

from microfreshener.core.importer import JSONImporter
from microfreshener.core.errors import ImporterError
from microfreshener.core.model import Service, Datastore, CommunicationPattern, MessageBroker, MessageRouter
from microfreshener.core.importer.jsontype import JSON_NODE_SERVICE, JSON_NODE_DATABASE, JSON_NODE_MESSAGE_BROKER, JSON_NODE_MESSAGE_ROUTER


class TestJSONImporterNodes(TestCase):

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
        self.assertIsInstance(db, Datastore)
        self.assertEqual(db.name, "my_database")

    def test_messagebroker(self):
        mb = self.microtosca['my_messagebroker']
        self.assertIsInstance(mb, MessageBroker)
        self.assertEqual(mb.name, "my_messagebroker")

    def test_messagerouter(self):
        mr = self.microtosca['my_messagerouter']
        self.assertIsInstance(mr, MessageRouter)
        self.assertEqual(mr.name, "my_messagerouter")

    def load_test_exceptions(self):
        with self.assertRaises(ImporterError):
            self.importer.load_node_from_json({"notype": JSON_NODE_SERVICE, "name": "prova"})
        with self.assertRaises(ImporterError):
            self.importer.load_node_from_json({"type": JSON_NODE_SERVICE, "noname": "prova"})
        with self.assertRaises(ImporterError):
            self.importer.load_node_from_json({"notype": JSON_NODE_SERVICE, "noname": "prova"})
        with self.assertRaises(ImporterError):
            self.importer.load_node_from_json({})

    def test_load_node_service(self):
        node = self.importer.load_node_from_json(
            {"type": JSON_NODE_SERVICE, "name": "prova"})
        self.assertIsInstance(node, Service)
        self.assertEqual(node.name, "prova")

    def test_load_node_database(self):
        node = self.importer.load_node_from_json(
            {"type": JSON_NODE_DATABASE, "name": "provadb"})
        self.assertIsInstance(node, Datastore)
        self.assertEqual(node.name, "provadb")

    def test_load_node_message_broker(self):
        node = self.importer.load_node_from_json(
            {"type": JSON_NODE_MESSAGE_BROKER, "name": "provamb"})
        self.assertIsInstance(node, MessageBroker)
        self.assertEqual(node.name, "provamb")

    def test_load_node_message_router(self):
        node = self.importer.load_node_from_json(
            {"type": JSON_NODE_MESSAGE_ROUTER, "name": "provamr"})
        self.assertIsInstance(node, MessageRouter)
        self.assertEqual(node.name, "provamr")
