import re
from enum import Enum


class BlockType(Enum):
    PARAGRAPH = 1
    HEADING = 2
    CODE = 3
    QUOTE = 4
    UNORDERED_LIST = 5
    ORDERED_LIST = 6


def is_block_headings(markdown: str):
    match = re.match(r"^(#{1,6})\s+(.*)$", markdown)
    return True if match else False


def is_block_code_blocks(markdown: str):
    match = re.match(r"```([\s\S]*?)```", markdown)
    return True if match else False


def is_block_quote_block(markdown: str):
    match = re.match(r">{1}\s+(.*)", markdown)
    return True if match else False


def is_block_unordered_list_block(markdown: str):
    match = re.match(r"-{1}\s+(.*)", markdown)
    return True if match else False


def is_block_ordered_list_block(markdown: str):
    match = re.match(r"(\d+)\.{1}\s+(.*)", markdown)
    return True if match else False


def block_to_block_type(markdown: str):
    if is_block_headings(markdown):
        return BlockType.HEADING
    elif is_block_code_blocks(markdown):
        return BlockType.CODE
    elif is_block_quote_block(markdown):
        return BlockType.QUOTE
    elif is_block_unordered_list_block(markdown):
        return BlockType.UNORDERED_LIST
    elif is_block_ordered_list_block(markdown):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
