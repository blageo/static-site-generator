import unittest
from htmlnode import HTMLNode

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

if __name__ == "__main__":
	unittest.main()