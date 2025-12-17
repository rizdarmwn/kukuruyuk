from enum import Enum


class TextType(Enum):
    PLAIN_TYPE = 1
    BOLD_TYPE = 2
    ITALIC_TYPE = 3
    CODE_TYPE = 4
    LINK_TYPE = 5
    IMAGE_TYPE = 6


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
