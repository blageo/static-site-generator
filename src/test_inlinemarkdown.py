import unittest
from textnode import TextNode, TextType
from inlinemarkdown import split_nodes_delimiter, extract_markdown_images, extract_markdown_links


class TestSplitNodesDelimiter(unittest.TestCase):
    def test_split_nodes_delimiter_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_italic(self):
        node = TextNode("This is text with a _italically emphasized_ and other stuff", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("italically emphasized", TextType.ITALIC),
            TextNode(" and other stuff", TextType.TEXT),
        ])

    def test_split_nodes_delimiter_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_nodes_delimiter_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_split_nodes_delimiter_bold_and_italic(self):
        node = TextNode("**bold** and _italic_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "_", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_split_nodes_delimiter_no_delimiter(self):
        node = TextNode("This has no delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This has no delimiter", TextType.TEXT)])

    def test_split_nodes_delimiter_sequential(self):
        node = TextNode("**Bold****Another**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("Bold", TextType.BOLD),
            TextNode("Another", TextType.BOLD),
        ])


class TestExtractMarkdownLinks(unittest.TestCase):
    def test_extract_markdown_links(self):
        text = "This is a [link](https://example.com) and another [link](https://example2.com)"
        links = extract_markdown_links(text)
        self.assertEqual(links, [
            ("link", "https://example.com"),
            ("link", "https://example2.com"),
        ])

    def test_extract_markdown_links_no_links(self):
        text = "This is a text without links"
        links = extract_markdown_links(text)
        self.assertEqual(links, [])

    def test_extract_markdown_links_empty_string(self):
        text = ""
        links = extract_markdown_links(text)
        self.assertEqual(links, [])


class TestExtractMarkdownImages(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is an ![alt text](https://example.com/image.png) and another ![alt text](https://example2.com/image2.png)"
        images = extract_markdown_images(text)
        self.assertEqual(images, [
            ("alt text", "https://example.com/image.png"),
            ("alt text", "https://example2.com/image2.png"),
        ])
    
    def test_extract_markdown_images_no_images(self):
        text = "This is a text without images"
        images = extract_markdown_images(text)
        self.assertEqual(images, [])
    
    def test_extract_markdown_images_empty_string(self):
        text = ""
        images = extract_markdown_images(text)
        self.assertEqual(images, [])


if __name__ == "__main__":
    unittest.main()