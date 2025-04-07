class HTMLNode():
    def __init__(
            self, 
            tag = None, 
            value = None, 
            children = None, 
            props = None
            ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"

    def __eq__(self, other):
        if not isinstance(other, HTMLNode):
            return False
        return (self.tag == other.tag and
				self.value == other.value and
				self.children == other.children and
				self.props == other.props)

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        if not self.props:
            return ""
        return " ".join(map(lambda kv: f"{kv[0]}='{kv[1]}'", self.props.items()))


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value
        
        props_html = self.props_to_html()
        if props_html:
            props_html = " " + props_html

        return f"<{self.tag}{props_html}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("missing tag")
        if self.children is None:
            raise ValueError("missing children")
        if not isinstance(self.children, list):
            raise ValueError("children must be a list")
        
        props_html = self.props_to_html()
        if props_html:
            props_html = " " + props_html
        
        children_html = "".join(child.to_html() for child in self.children)

        return f"<{self.tag}{props_html}>{children_html}</{self.tag}>"