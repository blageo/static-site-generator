import unittest
from blockmarkdown import (
    markdown_to_blocks,
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