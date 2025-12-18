from enum import Enum

from src.htmlnode import LeafNode


class TextType(Enum):
    TEXT = 1
    BOLD = 2
    ITALIC = 3
    CODE = 4
    LINK = 5
    IMAGE = 6


class TextNode:
    def __init__(self, text: str, text_type: TextType, url: str | None = None):
        self.text = text
        self.text_type = text_type
        self.url = url

    def __eq__(self, other) -> bool:
        if isinstance(other, TextNode):
            return (
                self.text == other.text
                and self.text_type == other.text_type
                and self.url == other.url
            )
        return NotImplemented

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type.value}, {self.url})"


def text_node_to_html_node(text_node: TextNode):
    match text_node.text_type:
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
            raise ValueError("text type is not on enum")
