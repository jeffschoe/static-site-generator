from enum import Enum

from htmlnode import ParentNode
from inline_markdown import text_to_textnodes
from textnode import text_node_to_html_node, TextNode, TextType

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    ULIST = "unordered_list"
    OLIST = "ordered_list"



def markdown_to_blocks(markdown):
    split_text = markdown.split("\n\n")
    empty_removed = []
    for item in split_text:
        stripped_item = item.strip()
        if stripped_item: # not empty
            empty_removed.append(stripped_item)
    return empty_removed


def block_to_block_type(block):
    block_len = len(block)
    split_lines = block.split("\n")
    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    # commented code below is alternate in case we need checking for the block to not be empty after the " "
    """
    if block.startswith("#"):
        count = 0
        # Iterate through the characters of the block
        for char in block: # count is at the index we are checking each new loop
            # If the character is a '#', increment the count
            if char == "#":
                count += 1
            # If it's not a '#', we've found the end of the leading hashes, so break the loop
            else:
                break
        if 1 <= count <= 6 and block_len >= count + 2 and block[count] == " ":
            return BlockType.HEADING
    """
    if block.startswith("```") and block.endswith("```") and block_len >= 6:
        return BlockType.CODE
    if block.startswith(">"):
        for line in split_lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH 
        return BlockType.QUOTE
    if block.startswith("- "):
        for line in split_lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH 
        return BlockType.ULIST
    if block[0:3] == "1. ":
        num = 1
        for line in split_lines:
            expected = f"{num}. "
            if not line.startswith(expected):
                return BlockType.PARAGRAPH 
            num += 1
        return BlockType.OLIST
    return BlockType.PARAGRAPH 


def markdown_to_html_node(markdown): 
    # converts a full markdown document into a single parent HTMLNode
    # 1. split the markdown into blocks
    blocks = markdown_to_blocks(markdown)
    children = [] # children of the single parent HTMLNode
    for block in blocks:
        print(f"\n***DEBUG: block = {block}\n")
        
        # 2. determine block type
        html_node = block_to_html_node(block)
        
      
        # 3. based on the type of block, create a new HTMLNode with the proper data
        # will get something like BlockType.PARAGRAPH, or .QUOTE or .HEADING
        children.append(html_node)
    return ParentNode("div", children, None)
       

def block_to_html_node(block): # returns the HTMLNode based on the type
    block_type = block_to_block_type(block) # pass text block to function to get type
    if block_type == BlockType.PARAGRAPH:
        return paragraph_to_html_node(block)
    if block_type == BlockType.HEADING:
        return heading_to_html_node(block)
    if block_type == BlockType.CODE:
        return code_to_html_node(block)
    if block_type == BlockType.OLIST:
        return olist_to_html_node(block)
    if block_type == BlockType.ULIST:
        return ulist_to_html_node(block)
    if block_type == BlockType.QUOTE:
        return quote_to_html_node(block)
    raise ValueError("invalid block type")

def text_to_children(text):
    text_nodes = text_to_textnodes(text) # create textnodes
    children = []
    for text_node in text_nodes:
        html_node = text_node_to_html_node(text_node) # create htmlnodes
        children.append(html_node)
    return children

def paragraph_to_html_node(block):
    lines = block.split("\n") # split on newlines
    paragraph = " ".join(lines) # make into a paragraph
    children = text_to_children(paragraph) # create children
    return ParentNode("p", children)

def heading_to_html_node(block):
    level = 0
    for char in block:
        if char == "#":
            level += 1
        else:
            break
    if level + 1 >= len(block):
        raise ValueError(f"invalid heading level: {level}")
    text = block[level + 1 :]
    children = text_to_children(text)
    return ParentNode(f"h{level}", children)

def code_to_html_node(block):
    if not block.startswith("```") or not block.startswith("```"):
        raise ValueError("invalid code block")
    text = block[4:-3] # ignore the backticks
    raw_text_node = TextNode(text, TextType.TEXT)
    child = text_node_to_html_node(raw_text_node)
    code = ParentNode("code", [child]) # inner nesting
    return ParentNode("pre", [code]) # outer

def olist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[3:] # ignore the "#. "
        children = text_to_children(text)
        html_items.append(ParentNode("li", children)) # inner nest
    return ParentNode("ol", html_items) # outer

def ulist_to_html_node(block):
    items = block.split("\n")
    html_items = []
    for item in items:
        text = item[2:] # ignore the "- "
        children = text_to_children(text)
        html_items.append(ParentNode("li", children)) # inner nest
    return ParentNode("ul", html_items)


def quote_to_html_node(block):
    lines = block.split("\n")
    new_lines = []
    for line in lines:
        if not line.startswith(">"):
            raise ValueError("invalid quote block")
        new_lines.append(line.lstrip(">").strip())
    content = " ".join(new_lines)
    children = text_to_children(content)
    return ParentNode("blockquote", children)
