import unittest
from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", "link", None, {"href": "boot.dev", "target": "_blank"})
        self.assertEqual(node.props_to_html(), " href=boot.dev target=_blank")

    def test_props_to_html_empty(self):
        node = HTMLNode("p", "text")
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_not_implemented(self):
        node = HTMLNode("p", "text")
        with self.assertRaises(NotImplementedError):
            node.to_html()


if __name__ == "__main__":
    unittest.main()
