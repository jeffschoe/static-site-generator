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


def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes: 
        if old_node.text_type != TextType.TEXT: # is already LINK or something else
            new_nodes.append(old_node) # no change needed, add to list
            continue
        original_text = old_node.text # full text version of node, which is everything
        images = extract_markdown_images(original_text) # gives list of tuples like: [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')]
        if len(images) == 0: # no images found
            new_nodes.append(old_node) # append the plain text node
            continue
        for alt, url in images: # for each image tuple ('to boot dev', 'https://www.boot.dev')
            string_markdown = f"![{alt}]({url})" # string literal markdown of tuple, such as "![alt](url)""
            sections = original_text.split(string_markdown, 1) # split the text, at the "![alt](url)" into two parts
            before_split = sections[0] # text before the split
            after_split = sections[1] # text after the split
            if len(sections) != 2: # didn't split correctly, but this is almost never the case due to the regex extractor
                raise ValueError("invalid markdown, image section not closed")
            if before_split != "": # is not empty (there is plain text, so need a new TextNode)
                new_nodes.append(TextNode(before_split, TextType.TEXT)) # add that TextNode baby
            new_nodes.append(TextNode(alt, TextType.IMAGE, url)) # add the image node
            original_text = after_split # start looking at the next section of text (after_split) for next loop iteration
        if original_text != "": # add new text node if it's not an empty string (empty string nodes are not created)
            new_nodes.append(TextNode(original_text, TextType.TEXT))
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT: # is already LINK or something else
            new_nodes.append(old_node) # no change needed, add to list
            continue
        original_text = old_node.text # full text version of node, which is everything
        links = extract_markdown_links(original_text) # gives something like: [('to boot dev', 'https://www.boot.dev'), ('to youtube', 'https://www.youtube.com/@bootdotdev')] 
        if len(links) == 0: # no links found
            new_nodes.append(old_node) # append the plain text node
            continue
        for anchor, url in links: # for each link tuple ('to boot dev', 'https://www.boot.dev')
            string_markdown = f"[{anchor}]({url})" # string literal markdown of tuple, such as "[alt](url)""
            sections = original_text.split(string_markdown, 1) # split the text, at the "[alt](url)" into two parts
            before_split = sections[0] # text before the split
            after_split = sections[1] # text after the split
            if len(sections) != 2: # didn't split correctly, but this is almost never the case due to the regex extractor
                raise ValueError("invalid markdown, link section not closed")
            if before_split != "": # is not empty (there is plain text, so need a new TextNode)
                new_nodes.append(TextNode(before_split, TextType.TEXT))  # add that TextNode node baby
            new_nodes.append(TextNode(anchor, TextType.LINK, url)) # add the link node
            original_text = after_split # start looking at the next section of text (after_split) for next loop iteration
        if original_text != "": # add new text node if it's not an empty string (empty string nodes are not created)
            new_nodes.append(TextNode(original_text, TextType.TEXT))
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




