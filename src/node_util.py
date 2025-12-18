from block import BlockType, block_to_block_type
from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType, text_node_to_html_node
from util import extract_markdown_images, extract_markdown_links, markdown_to_blocks


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
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


def split_nodes_bold(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_delimiter(old_nodes, "**", TextType.BOLD)


def split_nodes_italic(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_delimiter(old_nodes, "_", TextType.ITALIC)


def split_nodes_code(old_nodes: list[TextNode]) -> list[TextNode]:
    return split_nodes_delimiter(old_nodes, "`", TextType.CODE)


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
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


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
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


def text_to_textnodes(text: str):
    node = TextNode(text, TextType.TEXT)
    res = split_nodes_link(
        split_nodes_image(
            split_nodes_bold(split_nodes_italic(split_nodes_code([node])))
        )
    )
    return res


def text_to_children(text: str):
    new_nodes = []
    nodes = text_to_textnodes(text)
    for node in nodes:
        html_node = text_node_to_html_node(node)
        new_nodes.append(html_node)

    return new_nodes


def markdown_to_html_node(markdown: str):
    blocks = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks:
        node = None
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH:
                lines = block.split("\n")
                block = " ".join(lines)
                children = text_to_children(block)
                node = ParentNode("p", children)
            case BlockType.CODE:
                block = block.strip("```")
                block = block.split("\n", 1)[1]
                code_node = text_node_to_html_node(TextNode(block, TextType.CODE))
                node = ParentNode("pre", [code_node])
            case BlockType.HEADING:
                heading = block.split(" ", 1)
                block = heading[1]
                children = text_to_children(block)
                node = ParentNode(f"h{len(heading[0])}", children)
            case BlockType.ORDERED_LIST:
                li_nodes = []
                lines = block.split("\n")
                for line in lines:
                    ol = line.split(" ", 1)
                    words = ol[1]
                    li_nodes.append(ParentNode("li", text_to_children(words)))

                node = ParentNode("ol", li_nodes)
            case BlockType.UNORDERED_LIST:
                li_nodes = []
                lines = block.split("\n")
                for line in lines:
                    ol = line.split(" ", 1)
                    words = ol[1]
                    li_nodes.append(ParentNode("li", text_to_children(words)))
                node = ParentNode("ul", li_nodes)
            case BlockType.QUOTE:
                lines = block.split("\n")
                filtered_lines = []
                for line in lines:
                    filtered_lines.append(line.lstrip(">").strip())
                children = text_to_children(" ".join(filtered_lines))
                node = ParentNode("blockquote", children)
        nodes.append(node)
    html_node = ParentNode("div", nodes)
    return html_node
