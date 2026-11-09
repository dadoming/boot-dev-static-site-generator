import re
from enum import StrEnum

from htmlnode import HTMLNode
from parentnode import ParentNode
from split_nodes_delim import text_to_textnodes
from textnode import TextNode, TextType, text_node_to_html_node


class BlockType(StrEnum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    blocks = (block.strip() for block in markdown.split("\n\n"))
    return [block for block in blocks if block]


def block_to_block_type(block: str) -> BlockType:
    if re.match(r"#{1,6} \S", block):
        return BlockType.HEADING
    if re.fullmatch(r"```\n.*```", block, re.DOTALL):
        return BlockType.CODE
    if re.fullmatch(r">.*(\n>.*)*", block):
        return BlockType.QUOTE
    if re.fullmatch(r"- .*(\n- .*)*", block):
        return BlockType.UNORDERED_LIST
    if re.fullmatch(r"\d+\. .*(\n\d+\. .*)*", block):
        numbers = [int(n) for n in re.findall(r"^(\d+)\. ", block, re.MULTILINE)]
        if numbers == list(range(1, len(numbers) + 1)):
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def text_to_children(text: str) -> list[HTMLNode]:
    return [text_node_to_html_node(node) for node in text_to_textnodes(text)]


def block_to_html_node(block: str) -> HTMLNode:
    match block_to_block_type(block):
        case BlockType.HEADING:
            hashes, text = block.split(" ", 1)
            return ParentNode(f"h{len(hashes)}", text_to_children(text))
        case BlockType.CODE:
            code = TextNode(
                block.removeprefix("```\n").removesuffix("```"), TextType.TEXT
            )
            return ParentNode(
                "pre", [ParentNode("code", [text_node_to_html_node(code)])]
            )
        case BlockType.QUOTE:
            lines = [re.sub(r"^> ?", "", line) for line in block.split("\n")]
            return ParentNode("blockquote", text_to_children(" ".join(lines)))
        case BlockType.UNORDERED_LIST:
            items = [line[2:] for line in block.split("\n")]
            return ParentNode("ul", list_items(items))
        case BlockType.ORDERED_LIST:
            items = [line.split(". ", 1)[1] for line in block.split("\n")]
            return ParentNode("ol", list_items(items))
        case _:
            return ParentNode("p", text_to_children(" ".join(block.split("\n"))))


def list_items(items: list[str]) -> list[HTMLNode]:
    return [ParentNode("li", text_to_children(item)) for item in items]


def markdown_to_html_node(markdown: str) -> HTMLNode:
    blocks = markdown_to_blocks(markdown)
    return ParentNode("div", [block_to_html_node(block) for block in blocks])
