import unittest
from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_neq(self):
        node = TextNode("This is a plain text node", TextType.TEXT)
        node2 = TextNode("This is a bold text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_url(self):
        node = TextNode("This is a plain text node", TextType.TEXT, None)
        node2 = TextNode("This is a plain text node", TextType.TEXT, None)
        self.assertEqual(node, node2)

    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_bold(self):
        html_node = text_node_to_html_node(TextNode("bold", TextType.BOLD))
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "bold")

    def test_italic(self):
        html_node = text_node_to_html_node(TextNode("italic", TextType.ITALIC))
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "italic")

    def test_code(self):
        html_node = text_node_to_html_node(TextNode("print()", TextType.CODE))
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "print()")

    def test_link(self):
        node = TextNode("click", TextType.LINKS, "https://x.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.props, {"href": "https://x.com"})

    def test_image(self):
        node = TextNode("alt text", TextType.IMAGES, "https://x.com/i.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props, {"src": "https://x.com/i.png", "alt": "alt text"}
        )


if __name__ == "__main__":
    unittest.main()
