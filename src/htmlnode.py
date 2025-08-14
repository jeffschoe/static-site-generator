

class HTMLNode(): # a "node" in an HTML document tree (like a <p> tag and its contents, or an <a> tag and its contents). It can be block level or inline, and is designed to only output HTML.
    def __init__(self, tag=None, value=None, children=None, props=None):
        '''    
        An HTMLNode without a tag will just render as raw text
        An HTMLNode without a value will be assumed to have children
        An HTMLNode without children will be assumed to have a value
        An HTMLNode without props simply won't have any attributes
        '''
        self.tag = tag # A string representing the HTML tag name (e.g. "p", "a", "h1", etc.)
        self.value = value # A string representing the value of the HTML tag (e.g. the text inside a paragraph)
        self.children = children # A list of HTMLNode objects representing the children of this node
        self.props = props # A dictionary of key-value pairs representing the attributes of the HTML tag. For example, a link (<a> tag) might have {"href": "https://www.google.com"}

    def to_html(self):
        raise NotImplementedError # Child classes will override this method to render themselves as HTML.
    
    def props_to_html(self): # return a string that represents the HTML attributes of the node
        props = []
        for key in self.props:
            props.append(f' {key}="{self.props[key]}"')
        final_props = "".join(props)
        return final_props
    
    def __eq__(self, other):
        # compare all attribues of classes and return TRUE if all are equal
        return (
            self.tag == other.tag
            and self.value == other.value
            and self.children == other.children
            and self.props == other.props
        )


    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"