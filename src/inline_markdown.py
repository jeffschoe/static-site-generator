import re

from textnode import TextType, TextNode

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: # is already BOLD or something else
            new_nodes.append(old_node) # no change needed, add to list
            continue
        split_nodes = []
        sections = old_node.text.split(delimiter) # break the text up at the delimiters
        if len(sections) % 2 == 0: # check if it's even, means there are unmatched delimiters
            raise ValueError(f'invalid markdown, formatted section with delimiter "{delimiter}" not closed')
        for i in range(len(sections)):
            if sections[i] == "": # if empty string, don't bother appending an empty TextNode
                continue
            if i % 2 == 0: # index is even, meaning its plain text, append it
                split_nodes.append(TextNode(sections[i], TextType.TEXT)) # plain text nodes
            else:
                split_nodes.append(TextNode(sections[i], text_type)) # formatted nodes (BOLD, ITALIC, or CODE)
        new_nodes.extend(split_nodes)
    return new_nodes

def extract_markdown_images(text):
    """
    Takes raw markdown text and returns a list of tuples. 
    Each tuple should contain the alt text and the URL of any markdown images
    return [(alt text, url), (alt text, url)]
    """
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    """
    Extracts markdown links. 
    It should return tuples of anchor text and URLs
    return [(anchor text, url), (anchor text, url)]
    """
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches