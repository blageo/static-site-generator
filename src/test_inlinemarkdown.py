import unittest
from textnode import TextNode, TextType
from inlinemarkdown import text_to_textnodes, split_nodes_delimiter, split_nodes_link, split_nodes_image, extract_markdown_images, extract_markdown_links

class TestTestToTextNodes(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is a **bold** and _italic_ and `code` and ~~strikethrough~~ and [link](https://example.com) and ![image](https://example.com/image.png)"
        expected_nodes = [
            TextNode("This is a ", TextType.TEXT),
            TextNode("bold", TextType.BOLD),
            TextNode(" and ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.TEXT),
            TextNode("code", TextType.CODE),
            TextNode(" and ", TextType.TEXT),
            TextNode("strikethrough", TextType.STRIKETHROUGH),
            TextNode(" and ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://example.com"),
            TextNode(" and ", TextType.TEXT),
            TextNode("image", TextType.IMAGE, "https://example.com/image.png"),
        ]
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, expected_nodes)
    
    def test_text_to_text_nodes_empty(self):
        text = ""
        expected_nodes = []
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, expected_nodes)

    def test_text_to_text_nodes_no_delimiters(self):
        text = "This is a plain text without any formatting."
        expected_nodes = [TextNode(text, TextType.TEXT)]
        new_nodes = text_to_textnodes(text)
        self.assertEqual(new_nodes, expected_nodes)


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


class TestSplitNodesLink(unittest.TestCase):
    def test_split_nodes_link(self):
        node = TextNode("This is a [clickable link](https://example.com) and another [clickable link](https://example2.com)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("clickable link", TextType.LINK, "https://example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("clickable link", TextType.LINK, "https://example2.com"),
        ])

    def test_split_nodes_link_no_links(self):
        node = TextNode("This is a text without links", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("This is a text without links", TextType.TEXT)])

    def test_split_nodes_link_empty_string(self):
        node = TextNode("", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [TextNode("", TextType.TEXT)])

    def test_split_nodes_link_extra_whitespace(self):
        node = TextNode("This is a [ clickable link ]( https://example.com ) and another [ clickable link ]( https://example2.com )", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("clickable link", TextType.LINK, "https://example.com"),
            TextNode(" and another ", TextType.TEXT),
            TextNode("clickable link", TextType.LINK, "https://example2.com"),
        ])

    def test_split_nodes_link_empty_alt_text(self):
        node = TextNode("This is a [ ](https://example.com) with an empty alt text", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(new_nodes, [
            TextNode("This is a ", TextType.TEXT),
            TextNode("", TextType.LINK, "https://example.com"),
            TextNode(" with an empty alt text", TextType.TEXT),
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

    def test_extract_markdown_links_extra_whitespace(self):
        text = "[  alt text  ](  https://example.com  )"
        assert extract_markdown_links(text) == [
            ("alt text", "https://example.com"),
        ]


class TestExtractMarkdownImages(unittest.TestCase):
    def test_split_image(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
            ],
            new_nodes,
        )

    def test_split_image_single(self):
        node = TextNode(
            "![image](https://www.example.COM/IMAGE.PNG)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("image", TextType.IMAGE, "https://www.example.COM/IMAGE.PNG"),
            ],
            new_nodes,
        )

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )


if __name__ == "__main__":
    unittest.main()