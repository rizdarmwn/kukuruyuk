from typing import Optional, Self


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[list[Self]] = None,
        props: Optional[dict[str, str]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

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
        self, tag: str | None, value: str, props: dict[str, str] | None = None
    ):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value == "":
            raise ValueError
        if self.tag is None or self.tag == "":
            return self.value
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"
