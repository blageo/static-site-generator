from textnode import TextNode, TextType
import re


def text_to_textnodes(text):
    new_nodes = []
    nodes = [TextNode(text, TextType.TEXT)]
    delimiters = [
        ("**", TextType.BOLD),
        ("_", TextType.ITALIC),
        ("`", TextType.CODE),
        ("~~", TextType.STRIKETHROUGH),
    ]
    
    if not text:
        return new_nodes
    
    for delimiter, text_type in delimiters:
        nodes = split_nodes_delimiter(nodes, delimiter, text_type)

    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)

    new_nodes.extend(nodes) 
    
    return new_nodes


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        split = []
        parts = node.text.split(delimiter)

        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid markdown Syntax (unmatched delimiter): {delimiter}")
        
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                split.append(TextNode(parts[i], TextType.TEXT))
            else:
                split.append(TextNode(parts[i], text_type))
        new_nodes.extend(split)
    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if not node.text.strip():
            new_nodes.append(node)
            continue


        split = []
        last_index = 0

        for match in re.finditer(r'\[([^\]]+)\]\(([^)]+)\)', node.text):
            start, end = match.span()
            alt_text, url = match.groups()

            if last_index < start:
                split.append(TextNode(node.text[last_index:start], TextType.TEXT))
            split.append(TextNode(alt_text.strip(), TextType.LINK, url.strip()))
            last_index = end

        if last_index < len(node.text):
            split.append(TextNode(node.text[last_index:], TextType.TEXT))

        new_nodes.extend(split)

    return new_nodes


def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        if not node.text.strip():
            new_nodes.append(node)
            continue

        split = []
        last_index = 0

        for match in re.finditer(r'!\[([^\]]*)\]\(([^)]+)\)', node.text):
            start, end = match.span()
            alt_text, url = match.groups()

            if last_index < start:
                split.append(TextNode(node.text[last_index:start], TextType.TEXT))
            split.append(TextNode(alt_text.strip(), TextType.IMAGE, url.strip()))
            last_index = end

        if last_index < len(node.text):
            split.append(TextNode(node.text[last_index:], TextType.TEXT))

        new_nodes.extend(split)

    return new_nodes


def extract_markdown_links(text):
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return [(alt_text.strip(), url.strip()) for alt_text, url in matches]


def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return [(alt_text, url) for alt_text, url in matches]


def debug():
	text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
	print(text_to_textnodes(text))

if __name__ == "__main__":
	debug()