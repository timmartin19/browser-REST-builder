from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from ripozo import restmixins, Relationship, ListRelationship
import unittest2

from rest_builder.models import ResourceModel, RelationshipModel, ManagerModel


class TestModels(unittest2.TestCase):
    def test_resource_pks(self):
        """Test the pk creation"""
        res = ResourceModel(_pks='["id", "pk"]')
        self.assertListEqual(res.pks, ['id', 'pk'])
        res.pks = ['id']
        self.assertListEqual(res.pks, ['id'])
        self.assertEqual('["id"]', res._pks)

    def test_resource_init(self):
        """ResourceModel __init__"""
        res = ResourceModel()
        self.assertEqual(restmixins.CRUDL, res.restmixin_class)

    def test_relationship_query_args(self):
        rel = RelationshipModel()
        self.assertListEqual(rel.query_args, [])
        rel.query_args = ['first']
        self.assertEqual(rel._query_args, '["first"]')

    def test_relationship_property_map(self):
        rel = RelationshipModel()
        self.assertDictEqual(rel.property_map, {})
        rel.property_map = dict(x=1)
        self.assertDictEqual(rel.property_map, dict(x=1))

    def test_relationship_create_relationship(self):
        rel = RelationshipModel(is_list=True, name='blah')
        self.assertIsInstance(rel.relationship, ListRelationship)
        rel.is_list = False
        self.assertIsInstance(rel.relationship, Relationship)
        self.assertFalse(isinstance(rel, ListRelationship))

    def test_manager_create_fields(self):
        man = ManagerModel()
        self.assertListEqual(man.create_fields, [])
        man.create_fields = ['id']
        self.assertEqual(man._create_fields, '["id"]')

    def test_manager_update_fields(self):
        man = ManagerModel()
        self.assertListEqual(man.update_fields, [])
        man.update_fields = ['id']
        self.assertEqual(man._update_fields, '["id"]')

    def test_manager_list_fields(self):
        man = ManagerModel()
        self.assertListEqual(man.list_fields, [])
        man.list_fields = ['id']
        self.assertEqual(man._list_fields, '["id"]')
