# coding: utf-8

import logging, os, shutil, click

from simple_tools.interaction import confirm

from atompages import generate_pages, autocompiler, server

BASE_DIR = os.path.dirname(__file__)

@click.group()
@click.option('-l', '--debug/--no-debug', default=False)
def main(debug):
    logging.basicConfig(
        level=logging.DEBUG if debug else logging.INFO,
        format='%(asctime)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )

@main.command()
@click.argument('root', default=os.getcwd(), type=click.Path(file_okay=False, writable=True))
def init(root):
    """
    Initialize a new project.

    parameters:
        root: root of the project, defaults to current directory
    """
    root = os.path.abspath(root)

    source_path = os.path.join(root, 'source')
    plugin_path = os.path.join(root, 'plugins')

    if os.path.isdir(source_path):
        print("Source folder {} already exists, existing files may be overwritten!".format(source_path))
    if os.path.isdir(plugin_path):
        print("Plugin folder {} already exists, existing files may be overwritten!".format(source_path))

    if confirm('Create project in {}'.format(root)):
        shutil.copytree(os.path.join(BASE_DIR, "project_template/source"), source_path)
        shutil.copytree(os.path.join(BASE_DIR, "project_template/plugins"), plugin_path)

    generate_pages.build_site(root)

@main.command()
@click.argument('root', default=os.getcwd(), type=click.Path(file_okay=False, writable=True))
def generate(root):
    """
    Generate output from sources.
    """
    root = os.path.abspath(root)

    generate_pages.build_site(root)

@main.command()
@click.option('-p', '--port', default=8080, type=int)
@click.argument('root', default=os.getcwd(), type=click.Path(file_okay=False))
def develop(port, root):
    """
    Start project development mode

    Opens a webbrowser pointing to your compiled webpage Automatically listens
    for file changes in source and recompiles

    parameters:
        root: root of the project, defaults to current directory
    """
    root = os.path.abspath(root)

    def callback():
        autocompiler.main(root=root)

    output_path = os.path.join(root, 'output')

    # serve needs to be started as main thread, hence the callback
    server.serve(output_path, '127.0.0.1', port, callback=callback)

@main.command()
@click.option('-p', '--port', default=8080, type=int)
@click.argument('root', default=os.getcwd(), type=click.Path(file_okay=False))
def serve(port, root):
    output_path = os.path.join(root, 'output')

    server.serve(output_path, '127.0.0.1', port)

@main.command()
@click.argument('root', default=os.getcwd(), type=click.Path(file_okay=False))
def get_images(root):
    """
    Return the markdown include code for all images in base_dir (default: current directory)
    """
    root = os.path.abspath(root)

    if not "static/img" in root:
        raise RuntimeError("Images need to be located in the /static/img/ folder of your project")

    img_paths = sum([[os.path.join(root, f) for f in files] for root, folders, files in os.walk(root)], [])

    img_paths = filter(lambda i: True in [i.lower().endswith(s) for s in ['jpg','png','gif']], img_paths)
    img_paths = [p.replace("//","/") for p in img_paths]
    img_paths = ["![](/static/img/%s)" % (img.split("/static/img/")[-1].replace("\\","/")) for img in img_paths]

    for entry in img_paths:
        print(entry)

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
