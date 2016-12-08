import sys
import pkgutil
import sass
from jinja2 import Template
from operator import itemgetter

from . import pre_processors, post_processors, global_variables

def compile_sass(project_root, base_path):
    """ renders scss file using style variables given by metadata, then compiles scss to css"""
    from .global_variables import metadata
    styles = metadata.get_options(project_root)["styles"]
    scss_source = open(base_path+"/sass/main.scss.tmpl","r").read()
    scss_with_variables = Template(scss_source).render(styles=styles)
    open(base_path+"/sass/main.scss", "w").write(scss_with_variables)

    from sassutils.builder import build_directory
    build_directory(base_path+"/sass", base_path+"/css")

def get_submodules(package):
    prefix = package.__name__ + "."
    return [(modname.replace(prefix, ""), __import__(modname, fromlist="dummy"))
     for importer, modname, ispkg in pkgutil.iter_modules(package.__path__, prefix)]

def get_global_variables(project_root, pages, menu, lang):
    return {plugin_name:plugin_module.return_variables(project_root, pages, menu, lang)
            for plugin_name, plugin_module in get_submodules(global_variables)
            if not plugin_name.startswith("_")}

def apply_preprocessing(project_root, pages, menu, lang):
    for name, pre_processor in sorted(get_submodules(pre_processors), key=itemgetter(0)):
        print("applying pre-processor %s"%name)
        pre_processor.preprocess(project_root, pages, menu, lang)

def apply_postprocessing(project_root, pages, menu, lang):
    for name, pre_processor in sorted(get_submodules(post_processors), key=itemgetter(0)):
        print("applying post-processor %s"%name)
        pre_processor.preprocess(project_root, pages, menu, lang)
