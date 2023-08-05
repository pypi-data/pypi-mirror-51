from tests.test_enforcer import get_examples, get_enforcer
from unittest import TestCase


class TestRbacApi(TestCase):
    def test_get_roles_for_user(self):
        e = get_enforcer(get_examples("rbac_model.conf"), get_examples("rbac_policy.csv"))

        self.assertEqual(e.get_roles_for_user('alice'), ['data2_admin'])
        self.assertEqual(e.get_roles_for_user('bob'), [])
        self.assertEqual(e.get_roles_for_user('data2_admin'), [])
        self.assertEqual(e.get_roles_for_user('non_exist'), [])

    def test_get_users_for_role(self):
        e = get_enforcer(get_examples("rbac_model.conf"), get_examples("rbac_policy.csv"))

        self.assertEqual(e.get_users_for_role('data2_admin'), ['alice'])

    def test_has_role_for_user(self):
        e = get_enforcer(get_examples("rbac_model.conf"), get_examples("rbac_policy.csv"))

        self.assertTrue(e.has_role_for_user('alice', 'data2_admin'))
        self.assertFalse(e.has_role_for_user('alice', 'data1_admin'))

    def test_add_role_for_user(self):
        e = get_enforcer(get_examples("rbac_model.conf"), get_examples("rbac_policy.csv"))
        e.add_role_for_user('alice', 'data1_admin')
        self.assertEqual(e.get_roles_for_user('alice'), ['data2_admin', 'data1_admin'])

    def test_delete_role_for_user(self):
        e = get_enforcer(get_examples("rbac_model.conf"), get_examples("rbac_policy.csv"))
        e.add_role_for_user('alice', 'data1_admin')
        self.assertEqual(e.get_roles_for_user('alice'), ['data2_admin', 'data1_admin'])

        e.delete_role_for_user('alice', 'data1_admin')
        self.assertEqual(e.get_roles_for_user('alice'), ['data2_admin'])

    def test_delete_roles_for_user(self):
        e = get_enforcer(get_examples("rbac_model.conf"), get_examples("rbac_policy.csv"))
        e.delete_roles_for_user('alice')
        self.assertEqual(e.get_roles_for_user('alice'), [])

    def test_delete_user(self):
        e = get_enforcer(get_examples("rbac_model.conf"), get_examples("rbac_policy.csv"))
        e.delete_user('alice')
        self.assertEqual(e.get_roles_for_user('alice'), [])

    def test_delete_role(self):
        e = get_enforcer(get_examples("rbac_model.conf"), get_examples("rbac_policy.csv"))
        e.delete_role('data2_admin')
        self.assertTrue(e.enforce('alice', 'data1', 'read'))
        self.assertFalse(e.enforce('alice', 'data1', 'write'))
        self.assertFalse(e.enforce('alice', 'data2', 'read'))
        self.assertFalse(e.enforce('alice', 'data2', 'write'))
        self.assertFalse(e.enforce('bob', 'data1', 'read'))
        self.assertFalse(e.enforce('bob', 'data1', 'write'))
        self.assertFalse(e.enforce('bob', 'data2', 'read'))
        self.assertTrue(e.enforce('bob', 'data2', 'write'))

    def test_delete_permission(self):
        e = get_enforcer(get_examples("basic_without_resources_model.conf"),
                         get_examples("basic_without_resources_policy.csv"))
        e.delete_permission('read')
        self.assertFalse(e.enforce('alice', 'read'))
        self.assertFalse(e.enforce('alice', 'write'))
        self.assertFalse(e.enforce('bob', 'read'))
        self.assertTrue(e.enforce('bob', 'write'))

    def test_add_permission_for_user(self):
        e = get_enforcer(get_examples("basic_without_resources_model.conf"),
                         get_examples("basic_without_resources_policy.csv"))
        e.delete_permission('read')
        e.add_permission_for_user('bob', 'read')
        self.assertTrue(e.enforce('bob', 'read'))
        self.assertTrue(e.enforce('bob', 'write'))

    def test_delete_permission_for_user(self):
        e = get_enforcer(get_examples("basic_without_resources_model.conf"),
                         get_examples("basic_without_resources_policy.csv"))
        e.add_permission_for_user('bob', 'read')

        self.assertTrue(e.enforce('bob', 'read'))
        e.delete_permission_for_user('bob', 'read')
        self.assertFalse(e.enforce('bob', 'read'))
        self.assertTrue(e.enforce('bob', 'write'))

    def test_delete_permissions_for_user(self):
        e = get_enforcer(get_examples("basic_without_resources_model.conf"),
                         get_examples("basic_without_resources_policy.csv"))
        e.delete_permissions_for_user('bob')

        self.assertTrue(e.enforce('alice', 'read'))
        self.assertFalse(e.enforce('bob', 'read'))
        self.assertFalse(e.enforce('bob', 'write'))

    def test_get_permissions_for_user(self):
        e = get_enforcer(get_examples("basic_without_resources_model.conf"),
                         get_examples("basic_without_resources_policy.csv"))
        self.assertEqual(e.get_permissions_for_user('alice'), [['alice', 'read']])

    def test_has_permission_for_user(self):
        e = get_enforcer(get_examples("basic_without_resources_model.conf"),
                         get_examples("basic_without_resources_policy.csv"))
        self.assertTrue(e.has_permission_for_user('alice', *['read']))
        self.assertFalse(e.has_permission_for_user('alice', *['write']))
        self.assertFalse(e.has_permission_for_user('bob', *['read']))
        self.assertTrue(e.has_permission_for_user('bob', *['write']))

    def test_enforce_implicit_roles_api(self):
        e = get_enforcer(get_examples("rbac_model.conf"),
                         get_examples("rbac_with_hierarchy_policy.csv"))

        self.assertTrue(e.get_permissions_for_user('alice') == [["alice", "data1", "read"]])
        self.assertTrue(e.get_permissions_for_user('bob') == [["bob", "data2", "write"]])

        self.assertTrue(e.get_implicit_roles_for_user('alice') == ['admin', 'data1_admin', 'data2_admin'])
        self.assertTrue(e.get_implicit_roles_for_user('bob') == [])

    def test_enforce_implicit_roles_with_domain(self):
        e = get_enforcer(get_examples("rbac_with_domains_model.conf"),
                         get_examples("rbac_with_hierarchy_with_domains_policy.csv"))

        self.assertTrue(e.get_roles_for_user_in_domain('alice', 'domain1') == ['role:global_admin'])
        self.assertTrue(
            e.get_implicit_roles_for_user('alice', 'domain1') == ["role:global_admin", "role:reader", "role:writer"])

    def test_enforce_implicit_permissions_api(self):
        e = get_enforcer(get_examples("rbac_model.conf"),
                         get_examples("rbac_with_hierarchy_policy.csv"))
        self.assertTrue(e.get_permissions_for_user('alice') == [["alice", "data1", "read"]])
        self.assertTrue(e.get_permissions_for_user('bob') == [["bob", "data2", "write"]])
        self.assertTrue(e.get_implicit_permissions_for_user('alice') == [
            ['alice', 'data1', 'read'],
            ['data1_admin', 'data1', 'read'],
            ['data1_admin', 'data1', 'write'],
            ['data2_admin', 'data2', 'read'],
            ['data2_admin', 'data2', 'write']])
        self.assertTrue(e.get_implicit_permissions_for_user('bob') == [["bob", "data2", "write"]])

    def test_enforce_implicit_permissions_api_with_domain(self):
        e = get_enforcer(get_examples("rbac_with_domains_model.conf"),
                         get_examples("rbac_with_hierarchy_with_domains_policy.csv"))

        self.assertTrue(e.get_roles_for_user_in_domain('alice', 'domain1') == ['role:global_admin'])
        self.assertTrue(e.get_implicit_roles_for_user('alice', 'domain1') ==
                        ['role:global_admin', 'role:reader', 'role:writer'])
        self.assertTrue(e.get_implicit_permissions_for_user('alice', 'domain1') == [
            ['alice', 'domain1', 'data2', 'read'],
            ["role:reader", "domain1", "data1", "read"],
            ["role:writer", "domain1", "data1", "write"]])
        self.assertTrue(e.get_implicit_permissions_for_user('bob', 'domain1') == [])

    def test_enforce_get_users_in_domain(self):
        e = get_enforcer(get_examples("rbac_with_domains_model.conf"),
                         get_examples("rbac_with_domains_policy.csv"))
        self.assertTrue(e.get_users_for_role_in_domain('admin', 'domain1') == ['alice'])
        self.assertTrue(e.get_users_for_role_in_domain('non_exist', 'domain1') == [])
        self.assertTrue(e.get_users_for_role_in_domain('admin', 'domain2') == ['bob'])
        self.assertTrue(e.get_users_for_role_in_domain('non_exist', 'domain2') == [])
        e.delete_roles_for_user_in_domain('alice', 'admin', 'domain1')
        e.add_role_for_user_in_domain('bob', 'admin', 'domain1')
        self.assertTrue(e.get_users_for_role_in_domain('admin', 'domain1') == ['bob'])
        self.assertTrue(e.get_users_for_role_in_domain('non_exist', 'domain1') == [])
        self.assertTrue(e.get_users_for_role_in_domain('admin', 'domain2') == ['bob'])
        self.assertTrue(e.get_users_for_role_in_domain('non_exist', 'domain2') == [])

    def test_enforce_user_api_with_domain(self):
        e = get_enforcer(get_examples("rbac_with_domains_model.conf"),
                         get_examples("rbac_with_domains_policy.csv"))
        self.assertEqual(e.get_users_for_role_in_domain('admin', 'domain1'), ['alice'])
        self.assertEqual(e.get_users_for_role_in_domain('non_exist', 'domain1'), [])
        self.assertEqual(e.get_users_for_role_in_domain('admin', 'domain2'), ['bob'])
        self.assertEqual(e.get_users_for_role_in_domain('non_exist', 'domain2'), [])

        e.delete_roles_for_user_in_domain('alice', 'admin', 'domain1')
        e.add_role_for_user_in_domain('bob', 'admin', 'domain1')

        self.assertEqual(e.get_users_for_role_in_domain('admin', 'domain1'), ['bob'])
        self.assertEqual(e.get_users_for_role_in_domain('non_exist', 'domain1'), [])
        self.assertEqual(e.get_users_for_role_in_domain('admin', 'domain2'), ['bob'])
        self.assertEqual(e.get_users_for_role_in_domain('non_exist', 'domain2'), [])

    def test_enforce_get_roles_with_domain(self):
        e = get_enforcer(get_examples("rbac_with_domains_model.conf"),
                         get_examples("rbac_with_domains_policy.csv"))
        self.assertEqual(e.get_roles_for_user_in_domain('alice', 'domain1'), ['admin'])
        self.assertEqual(e.get_roles_for_user_in_domain('bob', 'domain1'), [])
        self.assertEqual(e.get_roles_for_user_in_domain('admin', 'domain1'), [])
        self.assertEqual(e.get_roles_for_user_in_domain('non_exist', 'domain1'), [])

        self.assertEqual(e.get_roles_for_user_in_domain('alice', 'domain2'), [])
        self.assertEqual(e.get_roles_for_user_in_domain('bob', 'domain2'), ['admin'])
        self.assertEqual(e.get_roles_for_user_in_domain('admin', 'domain2'), [])
        self.assertEqual(e.get_roles_for_user_in_domain('non_exist', 'domain2'), [])

        e.delete_roles_for_user_in_domain('alice', 'admin', 'domain1')
        e.add_role_for_user_in_domain('bob', 'admin', 'domain1')

        self.assertEqual(e.get_roles_for_user_in_domain('alice', 'domain1'), [])
        self.assertEqual(e.get_roles_for_user_in_domain('bob', 'domain1'), ['admin'])
        self.assertEqual(e.get_roles_for_user_in_domain('admin', 'domain1'), [])
        self.assertEqual(e.get_roles_for_user_in_domain('non_exist', 'domain1'), [])

        self.assertEqual(e.get_roles_for_user_in_domain('alice', 'domain2'), [])
        self.assertEqual(e.get_roles_for_user_in_domain('bob', 'domain2'), ['admin'])
        self.assertEqual(e.get_roles_for_user_in_domain('admin', 'domain2'), [])
        self.assertEqual(e.get_roles_for_user_in_domain('non_exist', 'domain2'), [])
