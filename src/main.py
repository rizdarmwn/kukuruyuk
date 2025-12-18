import os
import shutil
import sys

from node_util import markdown_to_html_node
from util import extract_title


def generate_page(from_path, template_path, dest_path, base_path):
    print(f"Generating path from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
        html = markdown_to_html_node(md).to_html()
        title = extract_title(md)

    with open(template_path, "r") as t:
        tmpl = t.read()
        tmpl = tmpl.replace("{{ Title }}", title)
        tmpl = tmpl.replace("{{ Content }}", html)
        tmpl = tmpl.replace('href="/', f'href="{base_path}')
        tmpl = tmpl.replace('src="/', f'src="{base_path}')

    with open(dest_path, "w") as w:
        w.write(tmpl)
    f.close()
    t.close()
    w.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, base_path):
    dirs = os.listdir(dir_path_content)
    for dir in dirs:
        new_src = os.path.join(dir_path_content, dir)
        new_dst = os.path.join(dest_dir_path, dir)
        if not os.path.exists(dest_dir_path):
            os.mkdir(dest_dir_path)
        if os.path.isfile(new_src):
            file_dst = new_dst.replace(".md", ".html")
            generate_page(new_src, template_path, file_dst, base_path)
        else:
            generate_pages_recursive(new_src, template_path, new_dst, base_path)


def copy_contents(src, dst):
    if os.path.exists(dst):
        print(f"Deleting directory: {dst}")
        shutil.rmtree(dst)
    dirs = os.listdir(src)
    for dir in dirs:
        new_src = os.path.join(src, dir)
        new_dst = os.path.join(dst, dir)
        if os.path.isfile(new_src):
            if not os.path.exists(dst):
                os.mkdir(dst)
            print(f"Copying file: {new_src} to {new_dst}")
            shutil.copy(new_src, new_dst)
        else:
            copy_contents(new_src, new_dst)


def main():
    basepath = sys.argv[1] if sys.argv[1] != "" else "/"
    copy_contents("static/", "docs/")
    generate_pages_recursive(f"content/", f"template.html", f"docs/", basepath)


if __name__ == "__main__":
    main()
