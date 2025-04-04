from htmlnode import HTMLNode

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
    