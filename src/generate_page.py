import os

from markdown_blocks import markdown_to_html_node


def extract_title(markdown: str) -> str:
    for line in markdown.split("\n"):
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("No header found")


def generate_page(from_path: str, template_path: str, dest_path: str) -> None:
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f:
        markdown = f.read()
    with open(template_path) as f:
        template = f.read()

    content = markdown_to_html_node(markdown).to_html()
    title = extract_title(markdown)
    page = template.replace("{{ Title }}", title).replace("{{ Content }}", content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    with open(dest_path, "w") as f:
        f.write(page)


def generate_pages_recursive(
    dir_path_content: str, template_path: str, dest_dir_path: str
) -> None:
    for entry in os.listdir(dir_path_content):
        src = os.path.join(dir_path_content, entry)
        if os.path.isfile(src):
            if entry.endswith(".md"):
                dest = os.path.join(dest_dir_path, entry.removesuffix(".md") + ".html")
                generate_page(src, template_path, dest)
        else:
            generate_pages_recursive(
                src, template_path, os.path.join(dest_dir_path, entry)
            )
