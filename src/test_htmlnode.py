import unittest

from htmlnode import HTMLNode, LeafNode


class TestHTMLNode(unittest.TestCase):
    def setUp(self) -> None:
        self.tag = "a"
        self.value = "TestNode"
        self.children = [HTMLNode(value="Child")]
        self.props = {"href": "https://www.google.com", "target": "_blank"}
        self.node = HTMLNode(self.tag, self.value, self.children, self.props)

    def test_repr_is_eq(self):
        expected = f"""HTMLNode(
        tag: {self.tag}
        value: {self.value}
        children: {self.children}
        props: {self.props}
        )
        """

        actual = repr(self.node)

        self.assertEqual(expected, actual)

    def test_props_to_html_is_ok(self):
        expected = ' href="https://www.google.com" target="_blank"'
        actual = self.node.props_to_html()

        self.assertEqual(expected, actual)

    def test_props_to_html_is_empty_when_node_properties_are_empty(self):
        expected = ""
        actual = HTMLNode().props_to_html()

        self.assertEqual(expected, actual)

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a_with_props(self):
        node = LeafNode("a", "Click it, baby!", {"href": "https//www.google.com"})
        self.assertEqual(
            node.to_html(), '<a href="https//www.google.com">Click it, baby!</a>'
        )

    def test_leaf_to_html_h1(self):
        node = LeafNode("h1", "Hello, world!")
        self.assertEqual(node.to_html(), "<h1>Hello, world!</h1>")



if __name__ == "__main__":
    unittest.main()
