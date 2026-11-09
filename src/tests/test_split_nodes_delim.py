import unittest

from split_nodes_delim import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "`", TextType.CODE),
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
        )

    def test_bold(self):
        node = TextNode("Some **bold** text", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "**", TextType.BOLD),
            [
                TextNode("Some ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text", TextType.TEXT),
            ],
        )

    def test_multiple_delimited(self):
        node = TextNode("_a_ and _b_", TextType.TEXT)
        self.assertEqual(
            split_nodes_delimiter([node], "_", TextType.ITALIC),
            [
                TextNode("a", TextType.ITALIC),
                TextNode(" and ", TextType.TEXT),
                TextNode("b", TextType.ITALIC),
            ],
        )

    def test_no_delimiter(self):
        node = TextNode("plain text", TextType.TEXT)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [node])

    def test_non_text_node_untouched(self):
        node = TextNode("already `bold`", TextType.BOLD)
        self.assertEqual(split_nodes_delimiter([node], "`", TextType.CODE), [node])

    def test_multiple_nodes(self):
        nodes = [
            TextNode("x `y`", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
        ]
        self.assertEqual(
            split_nodes_delimiter(nodes, "`", TextType.CODE),
            [
                TextNode("x ", TextType.TEXT),
                TextNode("y", TextType.CODE),
                TextNode("bold", TextType.BOLD),
            ],
        )

    def test_unmatched_raises(self):
        node = TextNode("broken `code", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)


class TestSplitNodesImage(unittest.TestCase):
    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            split_nodes_image([node]),
        )

    def test_image_only(self):
        node = TextNode("![alt](https://x.com/a.png)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("alt", TextType.IMAGE, "https://x.com/a.png")],
            split_nodes_image([node]),
        )

    def test_image_at_start_with_trailing_text(self):
        node = TextNode("![alt](https://x.com/a.png) trailing", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("alt", TextType.IMAGE, "https://x.com/a.png"),
                TextNode(" trailing", TextType.TEXT),
            ],
            split_nodes_image([node]),
        )

    def test_adjacent_images(self):
        node = TextNode(
            "![a](https://x.com/a.png)![b](https://x.com/b.png)", TextType.TEXT
        )
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://x.com/a.png"),
                TextNode("b", TextType.IMAGE, "https://x.com/b.png"),
            ],
            split_nodes_image([node]),
        )

    def test_duplicate_images(self):
        node = TextNode(
            "![a](https://x.com/a.png) and ![a](https://x.com/a.png)", TextType.TEXT
        )
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://x.com/a.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://x.com/a.png"),
            ],
            split_nodes_image([node]),
        )

    def test_no_images(self):
        node = TextNode("just plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_links_not_split(self):
        node = TextNode("a [link](https://boot.dev) here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_non_text_node_untouched(self):
        node = TextNode("![a](https://x.com/a.png)", TextType.BOLD)
        self.assertListEqual([node], split_nodes_image([node]))

    def test_multiple_nodes(self):
        nodes = [
            TextNode("one ![a](https://x.com/a.png)", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode("![b](https://x.com/b.png) two", TextType.TEXT),
        ]
        self.assertListEqual(
            [
                TextNode("one ", TextType.TEXT),
                TextNode("a", TextType.IMAGE, "https://x.com/a.png"),
                TextNode("bold", TextType.BOLD),
                TextNode("b", TextType.IMAGE, "https://x.com/b.png"),
                TextNode(" two", TextType.TEXT),
            ],
            split_nodes_image(nodes),
        )


class TestSplitNodesLink(unittest.TestCase):
    def test_split_links(self):
        node = TextNode(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)",
            TextType.TEXT,
        )
        self.assertListEqual(
            [
                TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode(
                    "to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"
                ),
            ],
            split_nodes_link([node]),
        )

    def test_link_only(self):
        node = TextNode("[boot](https://boot.dev)", TextType.TEXT)
        self.assertListEqual(
            [TextNode("boot", TextType.LINK, "https://boot.dev")],
            split_nodes_link([node]),
        )

    def test_link_with_trailing_text(self):
        node = TextNode("[boot](https://boot.dev) is great", TextType.TEXT)
        self.assertListEqual(
            [
                TextNode("boot", TextType.LINK, "https://boot.dev"),
                TextNode(" is great", TextType.TEXT),
            ],
            split_nodes_link([node]),
        )

    def test_no_links(self):
        node = TextNode("just plain text", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_images_not_split(self):
        node = TextNode("an ![image](https://x.com/a.png) here", TextType.TEXT)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_non_text_node_untouched(self):
        node = TextNode("[boot](https://boot.dev)", TextType.CODE)
        self.assertListEqual([node], split_nodes_link([node]))

    def test_images_then_links(self):
        node = TextNode(
            "![img](https://x.com/a.png) and [link](https://boot.dev)", TextType.TEXT
        )
        self.assertListEqual(
            [
                TextNode("img", TextType.IMAGE, "https://x.com/a.png"),
                TextNode(" and ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            split_nodes_link(split_nodes_image([node])),
        )


class TestTextToTextNodes(unittest.TestCase):
    def test_all_types(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            text_to_textnodes(text),
        )

    def test_plain_text(self):
        self.assertListEqual(
            [TextNode("just text", TextType.TEXT)], text_to_textnodes("just text")
        )

    def test_bold_only(self):
        self.assertListEqual(
            [TextNode("bold", TextType.BOLD)], text_to_textnodes("**bold**")
        )

    def test_bold_and_italic_adjacent(self):
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode("italic", TextType.ITALIC),
            ],
            text_to_textnodes("**bold**_italic_"),
        )

    def test_code_contents_not_parsed(self):
        self.assertListEqual(
            [
                TextNode("run ", TextType.TEXT),
                TextNode("my_var **x** [a](b)", TextType.CODE),
            ],
            text_to_textnodes("run `my_var **x** [a](b)`"),
        )

    def test_url_with_underscores(self):
        self.assertListEqual(
            [
                TextNode("see ", TextType.TEXT),
                TextNode("docs", TextType.LINK, "https://x.com/some_page_name"),
                TextNode(" ", TextType.TEXT),
                TextNode("now", TextType.ITALIC),
            ],
            text_to_textnodes("see [docs](https://x.com/some_page_name) _now_"),
        )

    def test_multiple_images_and_links(self):
        self.assertListEqual(
            [
                TextNode("a", TextType.IMAGE, "https://x.com/a.png"),
                TextNode(" ", TextType.TEXT),
                TextNode("b", TextType.LINK, "https://b.com"),
                TextNode(" ", TextType.TEXT),
                TextNode("c", TextType.IMAGE, "https://x.com/c.png"),
            ],
            text_to_textnodes(
                "![a](https://x.com/a.png) [b](https://b.com) ![c](https://x.com/c.png)"
            ),
        )

    def test_unmatched_delimiter_raises(self):
        with self.assertRaises(Exception):
            text_to_textnodes("this **is broken")


if __name__ == "__main__":
    unittest.main()
