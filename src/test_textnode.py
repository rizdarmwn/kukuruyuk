import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TYPE)
        node2 = TextNode("This is a text node", TextType.BOLD_TYPE)
        self.assertEqual(node, node2)

    def test_text_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD_TYPE)
        node2 = TextNode("This is a text node2", TextType.BOLD_TYPE)
        self.assertNotEqual(node, node2)

    def test_texttype_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC_TYPE)
        node2 = TextNode("This is a text node", TextType.BOLD_TYPE)
        self.assertNotEqual(node, node2)

    def test_if_url_is_none(self):
        node = TextNode("This is a text node", TextType.ITALIC_TYPE)
        self.assertEqual(node.url, None)

    def test_url_eq(self):
        node = TextNode(
            "This is a text node", TextType.BOLD_TYPE, "https://www.example.com"
        )
        node2 = TextNode(
            "This is a text node", TextType.BOLD_TYPE, "https://www.example.com"
        )
        self.assertEqual(node, node2)
        self.assertEqual(node.url, node2.url)
        self.assertNotEqual(node.url, None)
        self.assertNotEqual(node2.url, None)


if __name__ == "__main__":
    unittest.main()
