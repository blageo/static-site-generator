from textnode import TextNode, TextType
import re


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

def extract_markdown_links(text):
    pattern = r'\[([^\]]+)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return [(alt_text, url) for alt_text, url in matches]

def extract_markdown_images(text):
    pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    matches = re.findall(pattern, text)
    return [(alt_text, url) for alt_text, url in matches]
