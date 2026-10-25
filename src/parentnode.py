from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag=tag, children=children, props=props)

    def to_html(self):
        if not self.tag:
            raise ValueError("Cannot generate html, no tag")
        if not self.children:
            raise ValueError("Cannot generate html, no children")

        html_str = f"<{self.tag}"
        html_str += self.props_to_html()
        html_str += ">"
        for children in self.children:
            html_str += children.to_html()
        html_str += f"</{self.tag}>"

        return html_str
