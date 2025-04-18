from textnode import TextNode, TextType
from inlinemarkdown import text_to_textnodes





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