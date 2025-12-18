import unittest

from block import BlockType, block_to_block_type


class TestBlock(unittest.TestCase):
    def test_block_to_block_type_heading(self):
        block = "# This is a heading"

        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_paragraph(self):
        block = "This is a paragraph of text. It has some **bold** and _italic_ words inside of it."

        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_unordered_list(self):
        block = """- This is the first list item in a list block
- This is a list item
- This is another list item"""

        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_ordered_list(self):
        block = """1. This is the first list item in a list block
2. This is a list item
3. This is another list item"""

        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_quote_block(self):
        block = """> This is the first list item in a list block
> This is a list item
> This is another list item"""

        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_code_blocks(self):
        block = """```def test():
            code
        ```"""

        self.assertEqual(block_to_block_type(block), BlockType.CODE)
