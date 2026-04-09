from textnode import TextNode, TextType, text_node_to_html_node
from htmlnode import LeafNode, ParentNode
from inlinemarkdown import text_to_textnodes
from enum import Enum

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

def text_to_children(text):
    return [text_node_to_html_node(tn) for tn in text_to_textnodes(text)]

def heading_node(block):
    level = 0
    for ch in block:
        if ch == '#':
            level += 1
        else:
            break
    text = block[level + 1:]
    return ParentNode(f"h{level}", text_to_children(text))

def code_node(block):
    lines = block.split('\n')
    content = '\n'.join(lines[1:-1]) + '\n'
    return ParentNode("pre", [ParentNode("code", [text_node_to_html_node(TextNode(content, TextType.TEXT))])])

def quote_node(block):
    lines = block.split('\n')
    text = '\n'.join(line[2:] for line in lines)
    return ParentNode("blockquote", text_to_children(text))

def unordered_list_node(block):
    items = [ParentNode("li", text_to_children(line[2:])) for line in block.split('\n')]
    return ParentNode("ul", items)

def ordered_list_node(block):
    items = []
    for i, line in enumerate(block.split('\n'), 1):
        items.append(ParentNode("li", text_to_children(line[len(f"{i}. "):])))
    return ParentNode("ol", items)

def paragraph_node(block):
    return ParentNode("p", text_to_children(' '.join(block.split('\n'))))

def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    block_nodes = []

    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            block_nodes.append(paragraph_node(block))
        elif block_type == BlockType.HEADING:
            block_nodes.append(heading_node(block))
        elif block_type == BlockType.CODE:
            block_nodes.append(code_node(block))
        elif block_type == BlockType.QUOTE:
            block_nodes.append(quote_node(block))
        elif block_type == BlockType.UNORDERED_LIST:
            block_nodes.append(unordered_list_node(block))
        elif block_type == BlockType.ORDERED_LIST:
            block_nodes.append(ordered_list_node(block))
        else:
            raise ValueError(f"Unknown block type: {block_type}")

    return ParentNode("div", block_nodes)