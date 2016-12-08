import os
import time
import markdown
import codecs

from ..global_variables import metadata

md_extensions = ['markdown.extensions.extra',
                 'markdown.extensions.meta',
                 'markdown.extensions.sane_lists',
                 'markdown.extensions.toc']

def get_metadata(project_root, page, markdown_metadata):
    markdown_metadata = {k:v[0] for k,v in markdown_metadata.items()}
    default_meta = {"title": page.name,
                    "date": time.ctime(os.path.getctime(page.template_path)),
                    "description": "",
                    "category": "default",
                    "author": metadata.get_options(project_root)["default_author"]}
    default_meta.update(markdown_metadata)
    return default_meta


def preprocess(project_root, pages, menu, lang):
    md = markdown.Markdown(extensions=md_extensions)

    for page in pages:
        if page.extension == ".md":
            markdown_source = md.convert(page.source)
            page.source = """{% extends "page.html" %}
            {% block content %}
            """+markdown_source+"""
            {% endblock %}"""
            page.TOC = md.toc
            page.update_vars(**get_metadata(project_root, page, md.Meta))
            page.ext = ".html"
            page.link = page.link.replace(".md",".html")
            page.out_path = os.path.splitext(page.out_path)[0] + ".html"

    def recursive_map(fkt, lst):
        """ recursively applies the function fkt to every elemenent and sublist of lst"""
        return [recursive_map(fkt,item) if type(item) is list else fkt(item) for item in lst]
    fix_menu = lambda e: e.link.replace(".md",".html") if type(e) is page else e
    for i in range(len(menu)):
        menu[i] = recursive_map(fix_menu, menu[i])
