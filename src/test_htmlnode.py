import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode


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


class TestLeafNode(unittest.TestCase):
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

    def test_leaf_to_html_with_no_value(self):
        node = LeafNode("h1", "")
        self.assertEqual(node.to_html(), "<h1></h1>")

    def test_leaf_to_html_with_no_tag(self):
        node = LeafNode(tag=None, value="No Tag")
        self.assertEqual(node.to_html(), "No Tag")


class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_no_children(self):
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

    def test_to_html_with_no_tag(self):
        parent_node = ParentNode("", [])
        self.assertEqual(parent_node.to_html(), "<></>")

    def test_to_html_with_multiple_children(self):
        child_node1 = LeafNode("h1", "child1")
        child_node2 = LeafNode("b", "child2")
        child_node3 = LeafNode("b", "child3")
        parent_node = ParentNode("div", [child_node1, child_node2, child_node3])

        expected = "<div><h1>child1</h1><b>child2</b><b>child3</b></div>"
        self.assertEqual(parent_node.to_html(), expected)


if __name__ == "__main__":
    unittest.main()
