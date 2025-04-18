import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode

class TestHTMLNode(unittest.TestCase):
	def test_eq(self):
		node1 = HTMLNode("p", "Hello", [], {"class": "text"})
		node2 = HTMLNode("p", "Hello", [], {"class": "text"})
		self.assertEqual(node1, node2)

		node3 = HTMLNode("div", None, [HTMLNode("span", "Child")], {})
		node4 = HTMLNode("div", None, [HTMLNode("span", "Child")], {})
		self.assertEqual(node3, node4)

	def test_not_eq(self):
		node1 = HTMLNode("p", "Hello", [], {"class": "text"})
		node2 = HTMLNode("p", "Hello", [], {"id": "unique"})
		self.assertNotEqual(node1, node2)

		node3 = HTMLNode("div", "Text", [], {})
		node4 = HTMLNode("div", None, [], {})
		self.assertNotEqual(node3, node4)

		node5 = HTMLNode("h1", "Title", None, None)
		node6 = HTMLNode("h2", "Title", None, None)
		self.assertNotEqual(node5, node6)

	def test_props_to_html(self):
		node = HTMLNode("a", "Click here", [], {"href": "https://example.com", "target": "_blank"})
		self.assertEqual(node.props_to_html(), "href='https://example.com' target='_blank'")

		node_empty_props = HTMLNode("p", "No props", [], {})
		self.assertEqual(node_empty_props.props_to_html(), "")

		node_none_props = HTMLNode("p", "No props", [])
		self.assertEqual(node_none_props.props_to_html(), "")

	def test_to_html(self):
		node = HTMLNode("p", "Some text")
		with self.assertRaises(NotImplementedError):
			node.to_html()


class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_a(self):
        node = LeafNode("a", "Go to google.com!", {"href": "https://www.google.com"})
        self.assertEqual(node.to_html(), "<a href='https://www.google.com'>Go to google.com!</a>")

    def test_leaf_to_html_img(self):
        node = LeafNode("img", "Alt text", {"src": "image.jpg"})
        self.assertEqual(node.to_html(), "<img src='image.jpg'>Alt text</img>")

    def test_leaf_to_html_input(self):
        node = LeafNode("input", "Default text", {"type": "text", "name": "username"})
        self.assertEqual(node.to_html(), "<input type='text' name='username'>Default text</input>")

    def test_leaf_to_html_em(self):
        node = LeafNode("em", "emphasized text")
        self.assertEqual(node.to_html(), "<em>emphasized text</em>")

    def test_leaf_to_html_no_tag(self):
        node = LeafNode(None, "Just some text")
        self.assertEqual(node.to_html(), "Just some text")

    def test_leaf_to_html_no_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
            

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
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertTrue("missing children" in str(context.exception))

    def test_to_html_with_no_tag(self):
        parent_node = ParentNode("", None)
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertTrue("missing tag" in str(context.exception))
    
    def test_to_html_children_not_list(self):
        parent_node = ParentNode("div", "not a list")
        with self.assertRaises(ValueError) as context:
            parent_node.to_html()
        self.assertTrue("children must be a list" in str(context.exception))
    
    def test_to_html_with_multiple_children(self):
        child1 = LeafNode("span", "first child")
        child2 = LeafNode("b", "second child")
        child3 = LeafNode("i", "third child")
        parent_node = ParentNode("div", [child1, child2, child3])
    
        self.assertEqual(
            parent_node.to_html(),
            "<div><span>first child</span><b>second child</b><i>third child</i></div>"
        )

    def test_to_html_with_props(self):
        child_node = LeafNode("a", "Go to google.com!", {"href": "https://www.google.com"})
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><a href='https://www.google.com'>Go to google.com!</a></div>"
        )

if __name__ == "__main__":
	unittest.main()