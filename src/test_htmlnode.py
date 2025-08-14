import unittest

from htmlnode import HTMLNode


class TestHMTLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        node2 = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        self.assertEqual(node, node2) # Test that first and second are equal. If the values do not compare equal, the test will fail.

    def test_eq_false(self):
        node = HTMLNode(None, None, None, {"href": "https://www.boot.dev"})
        node2 = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        self.assertNotEqual(node, node2) # Test that first and second are NOT equal. If the values do not compare equal, the test will pass.

    def test_eq_false2(self):
        node = HTMLNode("p", None, None, None)
        node2 = HTMLNode("a", None, None, None)
        self.assertNotEqual(node.tag, node2.tag) # Test that first and second are NOT equal. If the values do not compare equal, the test will pass.

    def test_no_props(self):
        node = HTMLNode(None, None, None, None)
        self.assertIsNone(node.props) # test if there is no props

    def test_eq_props(self):
        node = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        node2 = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        self.assertEqual(node.props, node2.props) # test if props are equal

    def test_eq_false_props(self):
        node = HTMLNode(None, None, None, {"href": "https://www.boot.dev"})
        node2 = HTMLNode(None, None, None, {"href": "https://www.google.com"})
        self.assertNotEqual(node.props, node2.props) # Test that props of the first and second are NOT equal. If the values do not compare equal, the test will pass.

    def test_props_to_html(self):
        node = HTMLNode(None, None, None, {"a": "https://www.boot.dev", "href": "https://www.google.com"})
        self.assertEqual(
            ' a="https://www.boot.dev" href="https://www.google.com"', node.props_to_html()
        )

    def test_repr(self):
            node = HTMLNode("p", "generic paragraph text", None, {"href": "https://www.google.com"})
            self.assertEqual(
                "HTMLNode(p, generic paragraph text, None, {'href': 'https://www.google.com'})", repr(node)
            )

if __name__ == "__main__": # evaluates to TRUE if this script/file is run directly, so code below executes. If you import this script to someting else, this will be FALSE and the code below will not execute
    unittest.main() # automatically searches for all classes that inherit from unittest.TestCase in the current module. For us, this is TestTextNode.
    # for each method that matches the test_ prefix, unittest.main() creates a test case and executes it. test_eq is one example.
    