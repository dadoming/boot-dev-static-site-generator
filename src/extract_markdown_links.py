import re

IMG_REGEX = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
LINK_REGEX = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"


def extract_markdown_images(text: str) -> list[tuple[str, str]]:
    return re.findall(IMG_REGEX, text)


def extract_markdown_links(text: str) -> list[tuple[str, str]]:
    return re.findall(LINK_REGEX, text)
