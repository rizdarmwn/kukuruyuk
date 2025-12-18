import unittest

from util import (
    extract_markdown_images,
    extract_markdown_links,
    extract_title,
    markdown_to_blocks,
)


class TestUtil(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual(
            [
                ("to boot dev", "https://www.boot.dev"),
                ("to youtube", "https://www.youtube.com/@bootdotdev"),
            ],
            matches,
        )

    def test_markdown_to_blocks(self):
        md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_with_one_line(self):
        md = "This is **bolded** paragraph"

        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is **bolded** paragraph"])

    def test_markdown_to_blocks_with_empty_string(self):
        md = ""
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])

    def test_extract_title(self):
        md = "# Hello"
        expected = "Hello"
        actual = extract_title(md)
        self.assertEqual(actual, expected)

    def test_extract_title_with_false_value(self):
        md = "## World"
        with self.assertRaises(Exception):
            extract_title(md)

    def test_extract_title_with_no_splits(self):
        md = "Word"
        with self.assertRaises(Exception):
            extract_title(md)
