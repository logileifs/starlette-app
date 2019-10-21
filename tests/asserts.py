import unittest as ut
tc = ut.TestCase()


def assert_equal(first, second, msg=None):
	return tc.assertEqual(first, second, msg)


def assert_true(expr, msg=None):
	return tc.assertTrue(expr, msg)


def assert_dict_equal(d1, d2, msg=None):
	return tc.assertDictEqual(d1, d2, msg=None)


def assert_not_none(obj, msg=None):
	return tc.assertIsNotNone(obj, msg)


def assert_not_equal(first, second, msg=None):
	return tc.assertNotEqual(first, second, msg)
