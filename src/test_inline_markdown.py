import unittest

from inline_markdown import (
    split_nodes_delimiter,
    split_nodes_link,
    split_nodes_image,
    extract_markdown_images,
    extract_markdown_links
    )
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    
    def test_no_delimiters(self):
        node = TextNode("plain text", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("plain text", TextType.TEXT)])

    def test_single_bold_delimiter_pair(self):
        node = TextNode("hello **bold** world", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result, 
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" world", TextType.TEXT)
                ]
            )

    def test_single_italics_delimiter_pair(self):
        node = TextNode("hello _italic_ world", TextType.TEXT)
        result = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(
            result, 
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" world", TextType.TEXT)
                ]
            )


    def test_single_code_delimiter_pair(self):
        node = TextNode("hello `code` world", TextType.TEXT)
        result = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(
            result, 
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" world", TextType.TEXT)
                ]
            )


    def test_multiple_bold_delimiter_pair(self):
        node = TextNode("hello **bold** and **bold** world", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result, 
            [
                TextNode("hello ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" world", TextType.TEXT)
                ]
        )

    def test_multiple_bold_delimiter_pair_start_and_end(self):
        node = TextNode("**bold** hello **bold** and **bold** world **bold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result, 
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" hello ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" world ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
            ]
        )

    def test_mismatched_delimiters_bold(self):
        node = TextNode("hello **bold` world", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "**", TextType.BOLD)

    def test_mismatched_delimiters_italic(self):
        node = TextNode("hello _italic** world", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "_", TextType.ITALIC)

    def test_mismatched_delimiters_code(self):
        node = TextNode("hello `code_ world", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_non_text_node(self):
        node = TextNode("not TextType.TEXT", TextType.BOLD)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(result, [TextNode("not TextType.TEXT", TextType.BOLD)])

    def test_consecutive_delimiters(self):
        node = TextNode("**bold****alsobold**", TextType.TEXT)
        result = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(
            result, 
            [
                TextNode("bold", TextType.BOLD),
                TextNode("alsobold", TextType.BOLD), 
            ]
        )


class TestSplitNodesImage(unittest.TestCase):
    def test_split_image_multi_text_before_and_after_and_in_middle(self):
        node = TextNode(
            "This is text with a link ![to boot dev](https://www.boot.dev) and ![to youtube](https://www.youtube.com/@bootdotdev) lol ok?",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
                TextNode(" lol ok?", TextType.TEXT),
            ]
        )

    def test_split_image_multi_none_before_or_after_or_in_middle(self):
        node = TextNode(
            "![to boot dev](https://www.boot.dev)![to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode("to youtube", TextType.IMAGE, "https://www.youtube.com/@bootdotdev"),
            ]
        )

    def test_split_image_no_links(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertListEqual(new_nodes, [TextNode("just plain text", TextType.TEXT),])


class TestSplitNodesLink(unittest.TestCase):
    def test_split_link_multi_text_before_and_after_and_in_middle(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev) lol ok?",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
                TextNode(" lol ok?", TextType.TEXT),
            ]
        )

    def test_split_link_multi_none_before_or_after_or_in_middle(self):
        node = TextNode(
            "[to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_link([node])
        self.assertListEqual(
            new_nodes,
            [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
            ]
        )

    def test_split_link_no_links(self):
        node = TextNode("just plain text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertListEqual(new_nodes, [TextNode("just plain text", TextType.TEXT),])




class TestImageAndLinkRegex(unittest.TestCase):

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)
    
    def test_extract_markdown_images_multiple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![image](https://giantwombats.jpg)"
        )
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zjjcJKZ.png"),
                ("image", "https://giantwombats.jpg")
            ], 
            matches
        )

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev")], matches)

    def test_extract_markdown_links_multiple(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and a link [to good noods](https:www.goodnoodles.yum)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to good noods", "https:www.goodnoodles.yum")
            ], 
            matches
        )