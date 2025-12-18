import re


def extract_markdown_images(text: str):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def extract_markdown_links(text: str):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches


def markdown_to_blocks(markdown: str):
    new_blocks = []
    blocks = markdown.split("\n\n")
    for block in blocks:
        if block == "":
            continue
        new_blocks.append(block.strip())
    return new_blocks


def extract_title(markdown: str):
    h1 = markdown.split(" ", 1)
    if h1[0] != "#":
        raise Exception("markdown is not an h1")
    h1 = h1[1].split("\n", 1)
    return h1[0].strip()
