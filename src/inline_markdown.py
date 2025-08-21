from textnode import TextType, TextNode

"""
def split_nodes_delimiter(old_nodes, delimiter, text_type):
   
    new_nodes = []
    
    for old_node in old_nodes:
        if old_node.text_type == TextType.TEXT: # only do parsing on TEXT types
            sections = old_node.text.split(delimiter)
            if len(sections) % 2 == 0: # check if it's even, means there are unmatched delimiters
                raise ValueError(
                    f"invalid markdown, formatted section not closed, delimiter not closed: {delimiter}"
                    )
            # else, delimiters are matched, good
            for i, section in enumerate(sections):
                if i % 2 == 0: # index is even, meaning its plain text
                    new_nodes.append(TextNode(section, TextType.TEXT))
                else:
                    new_nodes.append(TextNode(section, text_type))
        else:
            new_nodes.append(old_node)
                
    return new_nodes 
"""

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
