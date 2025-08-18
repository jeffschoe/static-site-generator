from enum import Enum
from htmlnode import LeafNode


class TextType(Enum):
    TEXT = "text"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode: # represents the various types of inline text that can exist in HTML and Markdown
    def __init__(self, text, text_type, url=None):
        self.text = text # the text content of this node
        self.text_type = text_type # the type of text this node contains, which is a member of the TextType enum.
        self.url = url # the URL of the link or image

    def __eq__(self, other):
        # compare all attributes of classes and return TRUE if all are equal
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self):
        # returns a string presentation of the TextNode object
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})" # .value used to access enum value
    
def text_node_to_html_node(text_node):
    match text_node.text_type: # match/case statement validates against our TextType class
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:  # Default case
            raise ValueError(f"invalid text type: {text_node.text_type}")
        
            

