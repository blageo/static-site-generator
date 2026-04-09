import os
import shutil
import sys
from blockmarkdown import markdown_to_html_node


def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)

    for entry in os.listdir(src):
        src_path = os.path.join(src, entry)
        dst_path = os.path.join(dst, entry)
        if os.path.isfile(src_path):
            print(f"Copying {src_path} -> {dst_path}")
            shutil.copy(src_path, dst_path)
        else:
            copy_static(src_path, dst_path)

def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    raise ValueError("Title not found in markdown")

def generate_page(from_path, template_path, to_path):
    print(f"Generating page from {from_path} using template {template_path} -> {to_path}")
    with open(from_path) as f:
        markdown = f.read()
        title = extract_title(markdown)
    with open(template_path) as f:
        template = f.read()
    html_content = markdown_to_html_node(markdown).to_html()

    # Replace placeholders in template
    html = template.replace("{{ Title }}", title)
    html = html.replace("{{ Content }}", html_content)

    # Write the generated HTML to the destination path, create any directories if there are any
    os.makedirs(os.path.dirname(to_path), exist_ok=True)
    with open(to_path, "w") as f:
        f.write(html)

def main():
    copy_static("static", "public")
    generate_page("content/index.md", "template.html", "public/index.html")


if __name__ == "__main__":
    main()