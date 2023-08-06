from unittest import TestCase

from microfreshener.core.importer import YMLImporter
from microfreshener.core.exporter import YMLExporter
from microfreshener.core.model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH
from microfreshener.core.importer.ymltype import  YML_INTERACTION
from microfreshener.core.importer.ymltype import YML_RELATIONSHIP_T, YML_RELATIONSHIP_D, YML_RELATIONSHIP_C, YML_RELATIONSHIP_CD, YML_RELATIONSHIP_TC, YML_RELATIONSHIP_TD, YML_RELATIONSHIP_TCD
from microfreshener.core.model.type import MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY,MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY

class TestYmlExporterRelationships(TestCase):

    @classmethod
    def setUpClass(self):
        file = 'data/tests/test_relationships_properties.yml'
        importer = YMLImporter()
        self.microtosca = importer.Import(file)
        self.exporter = YMLExporter()

    def test_relationship(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target")
        self.assertEqual(rel_dict[YML_INTERACTION], "target")

    def test_relationship_t(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_t")
        self.assertEqual(rel_dict[YML_INTERACTION]['node'], "target_t")
        self.assertEqual(rel_dict[YML_INTERACTION]["relationship"], "t")
    
    def test_relationship_c(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_c")
        self.assertEqual(rel_dict[YML_INTERACTION]['node'], "target_c")
        self.assertEqual(rel_dict[YML_INTERACTION]["relationship"], "c")
    
    def test_relationship_d(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_d")
        self.assertEqual(rel_dict[YML_INTERACTION]['node'], "target_d")
        self.assertEqual(rel_dict[YML_INTERACTION]["relationship"], "d")
    
    def test_relationship_tc(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_tc")
        self.assertEqual(rel_dict[YML_INTERACTION]['node'], "target_tc")
        self.assertEqual(rel_dict[YML_INTERACTION]["relationship"], "tc")
    
    def test_relationship_td(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_td")
        self.assertEqual(rel_dict[YML_INTERACTION]['node'], "target_td")
        self.assertEqual(rel_dict[YML_INTERACTION]["relationship"], "td")
    
    def test_relationship_cd(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_cd")
        self.assertEqual(rel_dict[YML_INTERACTION]['node'], "target_cd")
        self.assertEqual(rel_dict[YML_INTERACTION]["relationship"], "cd")
    
    def test_relationship_tcd(self):
        rel_dict = self._transform_relationship_from_source_to_target("source", "target_tcd")
        self.assertEqual(rel_dict[YML_INTERACTION]['node'], "target_tcd")
        self.assertEqual(rel_dict[YML_INTERACTION]["relationship"], "tcd")
    
    def _transform_relationship_from_source_to_target(self, source_name, target_name):
        source = self.microtosca[source_name]
        target = self.microtosca[target_name]
        link_to_target = [
            link for link in source.interactions if link.target == target]
        self.assertEqual(len(link_to_target), 1)
        rel_dict = self.exporter._transform_relationship(link_to_target[0])
        return rel_dict
    


    def test_build_relationship_templates_t(self):
        rel = self.exporter.build_relationship_templates()
        self.assertDictEqual(rel[YML_RELATIONSHIP_T], {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY: True}})
        self.assertTrue(MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY not in rel[YML_RELATIONSHIP_T])
        self.assertTrue(MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY not in rel[YML_RELATIONSHIP_T])

    def test_build_relationship_templates_d(self):
        rel = self.exporter.build_relationship_templates()
        self.assertDictEqual(rel[YML_RELATIONSHIP_D], {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY: True}})
        self.assertTrue(MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY not in rel[YML_RELATIONSHIP_T])
        self.assertTrue(MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY not in rel[YML_RELATIONSHIP_T])

    def test_build_relationship_templates_c(self):
        rel = self.exporter.build_relationship_templates()
        self.assertDictEqual(rel[YML_RELATIONSHIP_C], {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY: True}})
        self.assertTrue(MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY not in rel[YML_RELATIONSHIP_T])
        self.assertTrue(MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY not in rel[YML_RELATIONSHIP_T])

    def test_build_relationship_templates_tc(self):
        rel = self.exporter.build_relationship_templates()
        self.assertDictEqual(rel[YML_RELATIONSHIP_TC], {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY: True, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY: True}})
        self.assertTrue(MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY not in rel[YML_RELATIONSHIP_T])
    
    def test_build_relationship_templates_td(self):
        rel = self.exporter.build_relationship_templates()
        self.assertDictEqual(rel[YML_RELATIONSHIP_TD], {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY: True, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY: True}})
        self.assertTrue(MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY not in rel[YML_RELATIONSHIP_T])
        
    def test_build_relationship_templates_cd(self):
        rel = self.exporter.build_relationship_templates()
        self.assertDictEqual(rel[YML_RELATIONSHIP_CD], {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY: True, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY: True}})
        self.assertTrue(MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY not in rel[YML_RELATIONSHIP_T])
    
    def test_build_relationship_templates_tcd(self):
        rel = self.exporter.build_relationship_templates()
        self.assertDictEqual(rel[YML_RELATIONSHIP_TCD], {"type": MICROTOSCA_RELATIONSHIPS_INTERACT_WITH, "properties": {MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_TIMEOUT_PROPERTY: True,MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_CIRCUIT_BREAKER_PROPERTY: True, MICROTOSCA_RELATIONSHIPS_INTERACT_WITH_DYNAMIC_DISCOVEY_PROPERTY: True}})
        





