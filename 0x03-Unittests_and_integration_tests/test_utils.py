#!/usr/bin/env python3
"""Utils Unittest Module."""
import unittest
from parameterized import parameterized
from typing import Sequence, Mapping
from utils import access_nested_map, get_json, memoize
from unittest.mock import patch


class TestAccessNestedMap(unittest.TestCase):
    """Implement all unittest cases for access_nested_map function in utils."""

    @parameterized.expand([
            ({"a": 1}, ("a",), 1),
            ({"a": {"b": 2}}, ("a",), {"b": 2}),
            ({"a": {"b": 2}}, ("a", "b"), 2),
            ])
    def test_access_nested_map(self, nested_map: Mapping,
                               path: Sequence, expected):
        """Test if access nested map return the rightful output."""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a", )),
        ({"a": 1}, ("a", "b"))
        ])
    def test_access_nested_map_exception(self, nested_map: Mapping,
                                         path: Sequence):
        """Check if exception is being raise if wrong argument are pass."""
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """Implement all unittest cases for get_json function in utils."""

    @parameterized.expand([
        ('http://example.com', {"payload": True}),
        ('http://holberton.io', {"payload": False})
        ])
    @patch('utils.requests')
    def test_get_json(self, test_url: str, test_payload: Mapping, mock_req):
        """Test if get_json returns the rightful output."""
        mock_req.get.return_value.json.return_value = test_payload
        self.assertEqual(get_json(test_url), test_payload)


class TestMemoize(unittest.TestCase):
    """Implement all unittest cases for memoize function in utils."""
    def test_memoize(self):
        """Check if a_method is memoized."""
        class TestClass:

            def a_method(self):
                return 42

            @memoize
            def a_property(self):
                return self.a_method()
        test_inst = TestClass()
        with patch.object(
                TestClass, 'a_method', return_value=42) as mock_a_method:
            self.assertEqual(test_inst.a_property, 42)
            self.assertEqual(test_inst.a_property, 42)
            mock_a_method.assert_called_once()
