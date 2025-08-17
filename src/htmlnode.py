

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
        raise NotImplementedError("to_html method not implemented") # Child classes will override this method to render themselves as HTML.
    
    def props_to_html(self): # return a string that represents the HTML attributes of the node
        if self.props is None:
            return "" # prevents errors is props is None
        props_html = ""
        for prop in self.props:
            props_html += f' {prop}="{self.props[prop]}"'
        return props_html

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, children: {self.children}, {self.props})"
    

class LeafNode(HTMLNode): # child class of HTMLNode
# A LeafNode is a type of HTMLNode that represents a single HTML tag with no children.
    def __init__(self, tag, value, props=None): # does not accept a children argument
        """
        It should not allow for any children
        The value data member should be required 
        (and tag even though the tag's value may be None), 
        while props can remain optional like the HTMLNode constructor.
        """
        super().__init__(tag, value, None, props) # takes arguments from init above, and pass them to HTMLNode constructor, which REQUIRES a children argument, so we must pass it None

    def to_html(self):
        if self.value is None:
            raise ValueError("invalid HTML: no value")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
    

class ParentNode(HTMLNode): # child class of HTMLNode
# A ParentNode will handle the nesting of HTML nodes inside of one another. Any HTML node that's not "leaf" node (i.e. it has children) is a "parent" node.
    def __init__(self, tag, children, props=None): # does not accept a children argument
        """
        The tag and children arguments are not optional
        It doesn't take a value argument
        props is optional
        (It's the exact opposite of the LeafNode class)
        """
        super().__init__(tag, None, children, props) # takes arguments from init above, and pass them to HTMLNode constructor, which REQUIRES a children argument, so we must pass it None

    def to_html(self):
        if self.tag is None:
            raise ValueError("invalid HTML: no tag")
        if self.children is None:
            raise ValueError("invalid HTML: no children")
        children_html = ""
        for child in self.children:
                children_html += child.to_html()
        return f"<{self.tag}{self.props_to_html()}>{children_html}</{self.tag}>"


    def __repr__(self):
        return f"ParentNode({self.tag}, children: {self.children}, {self.props})"