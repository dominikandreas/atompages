import os
import time

def preprocess(project_root, pages, menu, lang):
    for page in pages:
        page.mtime = os.path.getmtime(page.template_path)
        page.modified = time.ctime(page.mtime)
        page.ctime = os.path.getmtime(page.template_path)
        page.created = time.ctime(page.ctime)
