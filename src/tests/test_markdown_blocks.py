import unittest

from markdown_blocks import (
    BlockType,
    block_to_block_type,
    markdown_to_blocks,
    markdown_to_html_node,
)


class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_heading_paragraph_list(self):
        md = """# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item"""
        self.assertEqual(
            markdown_to_blocks(md),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_excessive_newlines(self):
        md = "first\n\n\n\n\nsecond\n\n\n"
        self.assertEqual(markdown_to_blocks(md), ["first", "second"])

    def test_strips_whitespace(self):
        md = "   first block   \n\n\tsecond block\t"
        self.assertEqual(markdown_to_blocks(md), ["first block", "second block"])

    def test_whitespace_only_block_removed(self):
        md = "first\n\n   \n\nsecond"
        self.assertEqual(markdown_to_blocks(md), ["first", "second"])

    def test_single_block(self):
        self.assertEqual(markdown_to_blocks("just one line"), ["just one line"])

    def test_empty(self):
        self.assertEqual(markdown_to_blocks(""), [])
        self.assertEqual(markdown_to_blocks("\n\n\n"), [])


class TestBlockToBlockType(unittest.TestCase):
    def check(self, block, expected):
        self.assertEqual(block_to_block_type(block), expected)

    def test_headings(self):
        for level in range(1, 7):
            self.check("#" * level + " heading", BlockType.HEADING)

    def test_heading_invalid(self):
        self.check("####### too many", BlockType.PARAGRAPH)
        self.check("#nospace", BlockType.PARAGRAPH)
        self.check("# ", BlockType.PARAGRAPH)

    def test_code(self):
        self.check("```\ncode here\nmore code\n```", BlockType.CODE)

    def test_code_invalid(self):
        self.check("```code```", BlockType.PARAGRAPH)
        self.check("```\nno closing fence", BlockType.PARAGRAPH)

    def test_quote(self):
        self.check(">one line", BlockType.QUOTE)
        self.check("> one\n> two\n>three", BlockType.QUOTE)

    def test_quote_invalid(self):
        self.check("> one\ntwo", BlockType.PARAGRAPH)

    def test_unordered_list(self):
        self.check("- one", BlockType.UNORDERED_LIST)
        self.check("- one\n- two\n- three", BlockType.UNORDERED_LIST)

    def test_unordered_list_invalid(self):
        self.check("-no space", BlockType.PARAGRAPH)
        self.check("- one\ntwo", BlockType.PARAGRAPH)
        self.check("* one", BlockType.PARAGRAPH)

    def test_ordered_list(self):
        self.check("1. one", BlockType.ORDERED_LIST)
        self.check("1. one\n2. two\n3. three", BlockType.ORDERED_LIST)

    def test_ordered_list_invalid(self):
        self.check("2. one\n3. two", BlockType.PARAGRAPH)
        self.check("1. one\n3. two", BlockType.PARAGRAPH)
        self.check("1. one\n1. two", BlockType.PARAGRAPH)
        self.check("1.one", BlockType.PARAGRAPH)
        self.check("1. one\ntwo", BlockType.PARAGRAPH)

    def test_ordered_list_double_digits(self):
        block = "\n".join(f"{i}. item" for i in range(1, 12))
        self.check(block, BlockType.ORDERED_LIST)

    def test_paragraph(self):
        self.check("just text", BlockType.PARAGRAPH)
        self.check("line one\nline two", BlockType.PARAGRAPH)

    def test_empty(self):
        self.check("", BlockType.PARAGRAPH)


if __name__ == "__main__":
    unittest.main()


class TestMarkdownToHtmlNode(unittest.TestCase):
    def html(self, md):
        return markdown_to_html_node(md).to_html()

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        self.assertEqual(
            self.html(md),
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        self.assertEqual(
            self.html(md),
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_headings(self):
        md = "# one\n\n### three with **bold**\n\n###### six"
        self.assertEqual(
            self.html(md),
            "<div><h1>one</h1><h3>three with <b>bold</b></h3><h6>six</h6></div>",
        )

    def test_quote(self):
        md = "> first line\n>second _line_"
        self.assertEqual(
            self.html(md),
            "<div><blockquote>first line second <i>line</i></blockquote></div>",
        )

    def test_unordered_list(self):
        md = "- one\n- **two**\n- three"
        self.assertEqual(
            self.html(md),
            "<div><ul><li>one</li><li><b>two</b></li><li>three</li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. one\n2. _two_\n3. three"
        self.assertEqual(
            self.html(md),
            "<div><ol><li>one</li><li><i>two</i></li><li>three</li></ol></div>",
        )

    def test_mixed_document(self):
        md = "# Title\n\nSome text\n\n- a\n- b\n\n1. x\n2. y"
        self.assertEqual(
            self.html(md),
            "<div><h1>Title</h1><p>Some text</p><ul><li>a</li><li>b</li></ul><ol><li>x</li><li>y</li></ol></div>",
        )

    def test_link_and_image_in_paragraph(self):
        md = "see [site](https://x.com) ![alt](https://x.com/a.png)"
        self.assertEqual(
            self.html(md),
            '<div><p>see <a href="https://x.com">site</a> <img src="https://x.com/a.png" alt="alt"></img></p></div>',
        )
