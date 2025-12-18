from textnode import TextNode, TextType
from util import extract_markdown_images, extract_markdown_links


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
):
    new_nodes = []
    for n in old_nodes:
        if n.text_type != TextType.TEXT:
            new_nodes.append(n)
            continue

        splitted_node = n.text.split(delimiter)
        if len(splitted_node) % 2 != 1:
            raise ValueError(f"matching closing delimiter '{str}' not found")
        for i in range(len(splitted_node)):
            if i % 2 == 1:
                new_node = TextNode(splitted_node[i], text_type)
                new_nodes.append(new_node)
            else:
                if splitted_node[i] == "":
                    continue
                new_node = TextNode(splitted_node[i], TextType.TEXT)
                new_nodes.append(new_node)
    return new_nodes


def split_nodes_bold(old_nodes: list[TextNode]):
    return split_nodes_delimiter(old_nodes, "**", TextType.BOLD)


def split_nodes_italic(old_nodes: list[TextNode]):
    return split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)


def split_nodes_code(old_nodes: list[TextNode]):
    return split_nodes_delimiter(old_nodes, "`", TextType.CODE)


def split_nodes_image(old_nodes: list[TextNode]):
    new_nodes = []
    for n in old_nodes:
        matches = extract_markdown_images(n.text)
        if len(matches) <= 0:
            new_nodes.append(n)
            continue
        mod_text = n.text
        for t in matches:
            image_alt = t[0]
            image_link = t[1]
            sections = mod_text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            mod_text = "".join(sections[1:])
        if mod_text != "":
            new_nodes.append(TextNode(mod_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]):
    new_nodes = []
    for n in old_nodes:
        matches = extract_markdown_links(n.text)
        if len(matches) <= 0:
            new_nodes.append(n)
            continue
        mod_text = n.text
        for t in matches:
            link_text = t[0]
            link_url = t[1]
            sections = mod_text.split(f"[{link_text}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            mod_text = "".join(sections[1:])
        if mod_text != "":
            new_nodes.append(TextNode(mod_text, TextType.TEXT))

    return new_nodes


def text_to_textnodes(text):
    node = TextNode(text, TextType.TEXT)
    res = split_nodes_link(
        split_nodes_image(
            split_nodes_bold(split_nodes_italic(split_nodes_code([node])))
        )
    )
    return res
