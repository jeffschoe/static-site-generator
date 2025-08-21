import unittest

from inline_markdown import (
    split_nodes_delimiter,
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