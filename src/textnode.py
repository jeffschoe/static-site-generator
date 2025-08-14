from enum import Enum


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
    


