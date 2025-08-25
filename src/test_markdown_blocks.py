import unittest


from markdown_blocks import (
    markdown_to_blocks,
    block_to_block_type,
    BlockType,

)


class MarkdownToHTML(unittest.TestCase):

    def test_block_to_block_type_paragraph(self):
        md = "This is **bolded** paragraph"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_heading_one(self):
        md = "# Heading one text"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_two(self):
        md = "## Heading two text"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_three(self):
        md = "### Heading three text"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_four(self):
        md = "#### Heading four text"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_five(self):
        md = "##### Heading five text"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_six(self):
        md = "###### Heading six text"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.HEADING)

    def test_block_to_block_type_heading_six(self):
        md = "####### Heading seven text which is an error"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.PARAGRAPH)

    def test_block_to_block_type_code(self):
        md = "```Code text```"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.CODE)

    def test_block_to_block_type_quote(self):
        md = ">Quote text"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.QUOTE)

    def test_block_to_block_type_unordered_list(self):
        md = "- Unordered list item 1\n- Unordered list item 2"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.ULIST)

    def test_block_to_block_type_ordered_list(self):
        md = "1. Ordered list item 1\n2. Ordered list item 2"
        result = block_to_block_type(md)
        self.assertEqual(result, BlockType.OLIST)



    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """

This is an _italic_ and **bolded** and `coded` paragraph



- This is a list
- with items

"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is an _italic_ and **bolded** and `coded` paragraph",
                "- This is a list\n- with items",
            ],
        )