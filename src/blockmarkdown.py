from textnode import TextNode, TextType
from inlinemarkdown import text_to_textnodes
from enum import Enum
import re

class BlockType(Enum):
	PARAGRAPH = "PARAGRAPH"
	HEADING = "HEADING"
	CODE = "CODE"
	QUOTE = "QUOTE"
	UNORDERED_LIST = "UNORDERED_LIST"
	ORDERED_LIST = "ORDERED_LIST"


def markdown_to_blocks(markdown):
	block_strings = []
	current_block = []

	for line in markdown.split('\n'):
		if line.strip() == '':
			if current_block:
				block_strings.append('\n'.join(current_block).strip())
				current_block = []
		else:
			current_block.append(line.strip())

	if current_block:
		block_strings.append('\n'.join(current_block).strip())

	return block_strings

def block_to_block_type(block):
	lines = block.split('\n')
    
    # Check for heading
	if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
		return BlockType.HEADING
    
    # Check for code block
	if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
		return BlockType.CODE

	# Check for quote
	if block.startswith("> "):
		for line in lines:
			if not line.startswith("> "):
				return BlockType.PARAGRAPH
		return BlockType.QUOTE
	
	# Check for list
	if block.startswith("- "):
		for line in lines:
			if not line.startswith("- "):
				return BlockType.PARAGRAPH
		return BlockType.UNORDERED_LIST
	
	# Check for ordered list
	if block.startswith("1. "):
		i = 1
		for line in lines:
			if not line.startswith(f"{i}. "):
				return BlockType.PARAGRAPH
			i += 1
		return BlockType.ORDERED_LIST
	return BlockType.PARAGRAPH