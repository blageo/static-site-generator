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

def generate_page(basepath, from_path, template_path, to_path):
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
    html = html.replace('href="/', f'href="{basepath}')
    html = html.replace('src="/', f'src="{basepath}')

    # Write the generated HTML to the destination path, create any directories if there are any
    os.makedirs(os.path.dirname(to_path), exist_ok=True)
    with open(to_path, "w") as f:
        f.write(html)

def generate_pages_recursive(basepath, content_dir, template_path, dest_dir):
    for entry in os.listdir(content_dir):
        src_path = os.path.join(content_dir, entry)
        dst_path = os.path.join(dest_dir, entry)
        if os.path.isfile(src_path) and src_path.endswith(".md"):
            generate_page(basepath, src_path, template_path, dst_path.replace(".md", ".html"))
        elif os.path.isdir(src_path):
            generate_pages_recursive(basepath, src_path, template_path, dst_path)

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"
    copy_static("static", "docs")
    open("docs/.nojekyll", "w").close()  # Create .nojekyll to prevent GitHub Pages from ignoring files starting with _
    generate_pages_recursive(basepath, "content", "template.html", "docs")


if __name__ == "__main__":
    main()