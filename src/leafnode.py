from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if not self.value:
            raise ValueError
        if not self.tag:
            return self.value

        html_str = f"<{self.tag}"
        html_str += self.props_to_html()
        html_str += ">"
        html_str += self.value
        html_str += f"</{self.tag}>"

        return html_str

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props})"
