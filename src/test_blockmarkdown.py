import unittest
from blockmarkdown import (
    markdown_to_blocks,
    block_to_block_type,
    markdown_to_html_node,
    BlockType,
)

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        md = """
    This is **bolded** paragraph
    
    This is another paragraph with _italic_ text and `code` here
    This is the same paragraph on a new line
    
    - This is a list
    - with items
    """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                "- This is a list\n- with items",
            ],
        )

    def test_markdown_to_blocks_empty(self):
        md = """
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, [])
        
    def test_markdown_to_blocks_no_newline(self):
        md = "This is a single line without newlines"
        blocks = markdown_to_blocks(md)
        self.assertEqual(blocks, ["This is a single line without newlines"])
    def test_markdown_to_blocks_consecutive_newlines(self):
        md = """
        This is a line


        This is another line


        And yet another line
        """
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a line",
                "This is another line",
                "And yet another line",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODE)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)
        block = "- list\n- items"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)


class TestMarkdownToHtmlNode(unittest.TestCase):
    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_heading(self):
        md = "## Hello World"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><h2>Hello World</h2></div>")

    def test_quote(self):
        md = "> This is a quote\n> with two lines"
        node = markdown_to_html_node(md)
        self.assertEqual(node.to_html(), "<div><blockquote>This is a quote\nwith two lines</blockquote></div>")

    def test_unordered_list(self):
        md = "- item one\n- item two\n- item **three**"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ul><li>item one</li><li>item two</li><li>item <b>three</b></li></ul></div>",
        )

    def test_ordered_list(self):
        md = "1. first\n2. second\n3. third"
        node = markdown_to_html_node(md)
        self.assertEqual(
            node.to_html(),
            "<div><ol><li>first</li><li>second</li><li>third</li></ol></div>",
        )