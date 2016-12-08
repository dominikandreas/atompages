# coding: utf-8

import os,sys,re
import time
import shutil
import logging
import collections
import pkgutil
from jinja2 import Environment, FileSystemLoader, Template
import codecs


class Page(object):
    def __init__(self, template_path, out_path, env, **kwargs):
        self.template_path = template_path
        self.out_path = out_path
        self.name = os.path.splitext(os.path.basename(out_path))[0]
        self.env = env
        self.extension = os.path.splitext(template_path)[1]
        self.source = codecs.open(template_path, mode="r", encoding="utf-8").read()
        self.update_vars(**kwargs)
        self.metadata = {}

    def update_vars(self, **kwargs):
        self.__dict__.update(kwargs)

    def update_metadata(self, **kwargs):
        self.metadata.update(kwargs)

    def update_output(self):
        print("compiling %s"%self.template_path)
        variables = self.metadata.copy()
        variables.update({"page":self.__dict__})
        self.output = self.env.from_string(self.source).render(**variables)

    def write(self):
        print("writing %s"%self.out_path)
        codecs.open(self.out_path, "wb", encoding="utf-8",
                                errors="xmlcharrefreplace").write(self.output)

def recursive_map(fkt, lst):
    """ recursively applies the function fkt to every elemenent and sublist of lst"""
    return [recursive_map(fkt,item) if type(item) is list else fkt(item) for item in lst]

def get_source_structure(root, path, dir_exclude_regex=".*/static|.*/templates", filter_fkt=lambda s: s is s):
    get_name = lambda s: os.path.splitext(os.path.basename(s))[0]
    for entry in os.listdir(root+"/"+path):
        if dir_exclude_regex is not None and re.search(dir_exclude_regex, root+"/"+ path):
            return
        if os.path.isdir(root+"/"+path+"/"+entry) and filter_fkt(entry):
            children = sorted(list(get_source_structure(root, path +"/" + entry, dir_exclude_regex, filter_fkt)))
            if len(children)>0:
                yield [get_name(entry), children]
        elif filter_fkt(entry):
                yield [get_name(entry), path+"/"+entry]

def get_output_structure(source_structure, language):
    def fix_umlaute(menuitems):
        for umlaut, fix in {u'Ä':u'Ae',u'Ö':u'Oe',u'Ü':u'Ue',u'ä':u'ae',u'ö':u'oe',u'ü':u'ue'}.items():
            menuitems = recursive_map(lambda s: s.replace(umlaut,fix) if s.startswith("/") else s, menuitems)
        return menuitems

    def get_name_from_path(p):
        p = p[1:] if p.startswith("/") else p
        fix_name = lambda s: "_".join(s.split("_")[1:]) if "_" in s else s

        if re.match("^[/]*[0-9]+$", p.split("_")[0]):
            p = "/".join([fix_name(s) for s in p.split("/")])
        if re.match("^[/]*%s$"%language, p.split("_")[0]):
            p = "/".join([fix_name(s) for s in p.split("/")])
            
        return p.replace("_"," ")
    print(source_structure)
    return fix_umlaute(recursive_map(get_name_from_path, source_structure))

def get_pages(env, src_path, target_path, current_root, src_structure, out_structure):
    pages = []
    for (src_name, src_child), (out_name, out_child) in zip(src_structure, out_structure):
        if type(out_child) is list:
            [pages.append(p) for p in
                  get_pages(env, src_path, target_path,
                    current_root+"/"+out_name+"/", src_child, out_child)]
        else:
            if not os.path.isdir(os.path.dirname(target_path+"/"+out_child)):
                os.makedirs(os.path.dirname(target_path+"/"+out_child))
            pages.append(Page(src_path +"/"+ src_child, target_path+"/"+out_child,
                    env, siblings=out_structure, link=out_child))
    return pages


def write_pages(project_root, pages, menu, lang):
    import plugins
    plugins.apply_preprocessing(project_root, pages, menu, lang)

    variables = plugins.get_global_variables(project_root, pages, menu, lang)
    variables.update({"menu":menu, "lang":lang})
    for page in pages:
        page.update_metadata(**variables)

    for page in pages:
        page.update_output()

    plugins.apply_postprocessing(project_root, pages, menu, lang)
    for page in pages:
        page.write()

def get_menu(out_structure, pages, language):
    for item, children in out_structure:
        if type(children) is list:
            yield (item, list(get_menu(children, pages, language)))
        else:
            for page in pages:
                if page.link == children:
                    page.link = "/%s/%s"%(language,page.link)
                    yield (item, page)
                    break

def build_site(base_dir=None, languages=("en","de")):
    #base_dir = os.getcwd(); languages=("de","en")
    if base_dir is None:
        base_dir = os.path.dirname(os.path.abspath(__file__))

    base_dir = os.path.abspath(base_dir)
    sys.path.insert(-1, base_dir)
    print("building project in directory %s"%base_dir)
    try:
        import plugins
    except Exception as e:
        logging.exception(e)
        print("\nPlugins module not found in your project directory.\nEither it's not there, or one of the modules has an error. Try running\npython -m atompages init\nagain if you're not sure why this failes\n\n")

    src_path = base_dir+"/source/pages"
    static_path = base_dir+"/source/static"

    template_path = os.path.abspath(base_dir + "/source/templates")
    target_path = os.path.abspath(base_dir + "/output")

    env = Environment(loader=FileSystemLoader([template_path, src_path]))

    has_no_lang = lambda s: not "_" in s or not True in [l in s.split("_")[:-1] for l in languages]
    has_lang = lambda s,lng:  "_" in s and s.split("_")[-2] == lng
    extensions = [".html",".md"]
    has_ext = lambda s: not "." in s or True in [s.endswith(ext) for ext in extensions]
    filterfkt = lambda s, lng: (has_lang(s,lng) or has_no_lang(s)) and has_ext(s)

    shutil.rmtree(target_path, ignore_errors=True)
    plugins.compile_sass(base_dir, static_path)
    shutil.copytree(static_path, target_path+"/static")

    for lng in languages:
        print("processing language %s"%lng)
        src_structure = list(get_source_structure(src_path,"", filter_fkt=lambda s: filterfkt(s, lng)))
        out_structure = get_output_structure(src_structure, lng)

        pages = get_pages(env, src_path, target_path+"/"+lng, "", src_structure, out_structure)
        menu = list(get_menu(out_structure, pages, lng))
        write_pages(base_dir, pages, menu, lng)

    with open(target_path+"/index.html", "w") as f:
        f.write("""<head><script>window.location = "/%s/index.html"</script></head>"""%languages[0])

    with open(target_path + "/mtime.html", "w") as f:
        f.write(str(time.time()))

if __name__ == "__main__":
    build_site()
