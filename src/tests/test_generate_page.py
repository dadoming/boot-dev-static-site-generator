import os
import tempfile
import unittest

from generate_page import extract_title, generate_page


class TestExtractTitle(unittest.TestCase):
    def test_simple(self):
        self.assertEqual(extract_title("# Hello"), "Hello")

    def test_strips_whitespace(self):
        self.assertEqual(extract_title("#   Hello world   "), "Hello world")

    def test_title_not_on_first_line(self):
        self.assertEqual(extract_title("intro\n\n# Title\n\nbody"), "Title")

    def test_ignores_other_heading_levels(self):
        self.assertEqual(extract_title("## sub\n\n# Main"), "Main")

    def test_no_h1_raises(self):
        with self.assertRaises(Exception):
            extract_title("## only h2\n\ntext")

    def test_hash_without_space_raises(self):
        with self.assertRaises(Exception):
            extract_title("#nospace")

    def test_empty_raises(self):
        with self.assertRaises(Exception):
            extract_title("")


class TestGeneratePage(unittest.TestCase):
    def test_generates_page_and_creates_directories(self):
        with tempfile.TemporaryDirectory() as tmp:
            md_path = os.path.join(tmp, "page.md")
            template_path = os.path.join(tmp, "template.html")
            dest_path = os.path.join(tmp, "out", "nested", "index.html")
            with open(md_path, "w") as f:
                f.write("# My Title\n\nSome **bold** text")
            with open(template_path, "w") as f:
                f.write("<title>{{ Title }}</title><body>{{ Content }}</body>")

            generate_page(md_path, template_path, dest_path)

            with open(dest_path) as f:
                self.assertEqual(
                    f.read(),
                    "<title>My Title</title><body><div><h1>My Title</h1>"
                    "<p>Some <b>bold</b> text</p></div></body>",
                )
