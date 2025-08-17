import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


class TestHMTLNode(unittest.TestCase):
    # HTML node tests
    def test_to_html_props(self):
        node = HTMLNode(
            "div",
            "Hello, world!",
            None,
            {"class": "greeting", "href": "https://boot.dev"},
        )
        self.assertEqual(
            node.props_to_html(),
            ' class="greeting" href="https://boot.dev"',
        )

    def test_values(self):
        node = HTMLNode(
            "div",
            "I wish I could read",
        )
        self.assertEqual(
            node.tag,
            "div",
        )
        self.assertEqual(
            node.value,
            "I wish I could read",
        )
        self.assertEqual(
            node.children,
            None,
        )
        self.assertEqual(
            node.props,
            None,
        )

    def test_repr(self):
        node = HTMLNode(
            "p",
            "What a strange world",
            None,
            {"class": "primary"},
        )
        self.assertEqual(
            node.__repr__(),
            "HTMLNode(p, What a strange world, children: None, {'class': 'primary'})",
        )

    # Leaf Node tests
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Hello, world!")
        self.assertEqual(node.to_html(), "<a>Hello, world!</a>")

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")

    def test_leaf_to_html_props(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com">Click me!</a>'
            )

    def test_leaf_no_value(self):
        node = LeafNode("a", None, {"href": "https://www.google.com"})
        with self.assertRaises(ValueError): 
            # tells unittest "expect that the code inside this block will raise a ValueError exception, and if it does, the test passes."
            node.to_html()

    def test_leaf_no_tag(self):
        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(
            node.to_html(),
            "Click me!"
        )

    # Parent Node tests
    def test_to_html_without_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError) as context: 
            # tells unittest "expect that the code inside this block will raise a ValueError exception, and if it does, the test passes."
            parent_node.to_html()
        self.assertEqual(str(context.exception), "invalid HTML: no tag")
    
    def test_to_html_without_children(self):
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context: 
            # tells unittest "expect that the code inside this block will raise a ValueError exception, and if it does, the test passes."
            parent_node.to_html()
        self.assertEqual(str(context.exception), "invalid HTML: no children")
    
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_empty_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_multiple_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
            )
    
    def test_to_html_with_nested_parent(self):
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ]
                    
                ),
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<div><p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p><b>Bold text</b>Normal text<i>italic text</i>Normal text</div>"
            )

    def test_to_html_with_props(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node], {"class": "container", "id": "main"})
        self.assertEqual(
            parent_node.to_html(),
            '<div class="container" id="main"><span>child</span></div>'
            )

    def test_to_html_with_props_and_nested_props(self):
        child_node = LeafNode("a", "link", {"href": "https://example.com"})
        parent_node = ParentNode("div", [child_node], {"class": "wrapper"})
        self.assertEqual(
            parent_node.to_html(), 
            '<div class="wrapper"><a href="https://example.com">link</a></div>'
            )

    def test_to_html_with_mixed_children_types(self):
        # Mix of LeafNodes and ParentNodes as siblings
        leaf1 = LeafNode("span", "text1")
        nested_parent = ParentNode("p", [LeafNode("b", "bold")])
        leaf2 = LeafNode("span", "text2")
        
        parent = ParentNode("div", [leaf1, nested_parent, leaf2])
        expected = "<div><span>text1</span><p><b>bold</b></p><span>text2</span></div>"
        self.assertEqual(parent.to_html(), expected)

    def test_to_html_with_deep_nesting(self):
        # Test 3+ levels deep
        deep_leaf = LeafNode("strong", "very nested")
        level2 = ParentNode("em", [deep_leaf])
        level1 = ParentNode("p", [level2])
        root = ParentNode("div", [level1])
        
        expected = "<div><p><em><strong>very nested</strong></em></p></div>"
        self.assertEqual(root.to_html(), expected)




if __name__ == "__main__": # evaluates to TRUE if this script/file is run directly, so code below executes. If you import this script to someting else, this will be FALSE and the code below will not execute
    unittest.main() # automatically searches for all classes that inherit from unittest.TestCase in the current module. For us, this is TestTextNode.
    # for each method that matches the test_ prefix, unittest.main() creates a test case and executes it. test_eq is one example.
    