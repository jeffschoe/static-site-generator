import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(node, node2) # Test that first and second are equal. If the values do not compare equal, the test will fail.

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2) # Test that first and second are NOT equal. If the values do not compare equal, the test will pass.

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.TEXT)
        node2 = TextNode("This is a text node2", TextType.TEXT)
        self.assertNotEqual(node, node2) # Test that first and second are NOT equal. If the values do not compare equal, the test will pass.

    def test_no_url(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        self.assertIsNone(node.url) # test if there is no URL

    def test_eq_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
        node2 = TextNode("This is a text node", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node.url, node2.url) # test if urls are equal

    def test_eq_false_text_type(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2) # Test that TextType of the first and second are NOT equal. If the values do not compare equal, the test will pass.

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, text, https://www.boot.dev)", repr(node)
        )

if __name__ == "__main__": # evaluates to TRUE if this script/file is run directly, so code below executes. If you import this script to someting else, this will be FALSE and the code below will not execute
    unittest.main() # automatically searches for all classes that inherit from unittest.TestCase in the current module. For us, this is TestTextNode.
    # for each method that matches the test_ prefix, unittest.main() creates a test case and executes it. test_eq is one example.
    
    