import unittest
from parentnode import ParentNode
from leafnode import LeafNode

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