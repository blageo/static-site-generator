from textnode import TextNode, TextType
from leafnode import LeafNode


def text_node_to_html_node(text_node):
    text_type = text_node.text_type
    match text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise Exception("unknown text type")

def main():
    node = TextNode("boop boop beep beep", TextType.LINK, "https://www.boot.dev")
    print(node)

if __name__ == "__main__":
    main()