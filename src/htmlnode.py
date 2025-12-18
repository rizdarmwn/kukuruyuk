from typing import Optional, Self


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list[Self]] = None,
        props: Optional[dict[str, str | None]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError("to html is not implemented")

    def props_to_html(self):
        str_builder = [""]
        if self.props is None or len(self.props) == 0:
            return ""

        for p in self.props:
            str_builder.append(f'{p}="{self.props[p]}"')

        return " ".join(str_builder)

    def __repr__(self):
        return f"""HTMLNode(
        tag: {self.tag}
        value: {self.value}
        children: {self.children}
        props: {self.props}
        )
        """


class LeafNode(HTMLNode):
    def __init__(
        self, tag: str | None, value: str, props: dict[str, str | None] | None = None
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("value is missing")
        if self.tag is None:
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"


class ParentNode(HTMLNode):
    def __init__(self, tag: str, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("tag is missing")

        if self.children is None:
            raise ValueError("children is missing")

        str_builder = []
        for c in self.children:
            str_builder.append(c.to_html())
        joined = "".join(str_builder)

        return f"<{self.tag}>{joined}</{self.tag}>"
