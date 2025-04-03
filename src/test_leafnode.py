import unittest
from leafnode import LeafNode


class TestHTMLNode(unittest.TestCase):
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

if __name__ == "__main__":

    unittest.main()