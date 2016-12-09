import os, sys
import logging
import cherrypy
import webbrowser
from threading import Thread, Timer
import socket
import time
try: input=raw_input
except: pass
#for debugging
__file__ = __file__ if "__file__" in locals() else os.getcwd()
base_dir = os.path.dirname(__file__)

def on_windows():
    return os.name == 'nt'

def exit_err(msg):
    print(msg)
    exit()

def copy_folder(src, dest):
    #shutils fails to copy when destination exists, this seemed more reliable
    if on_windows():
        os.system('xcopy "%s" "%s" /E /I'%(src,dest))
    else:
        os.system('cp -rf "%s" "%s"'%(src,dest))

develop_script =  \
"""
cd %~dp0
python -m atompages develop"""  if on_windows() else \
"""
#!/bin/sh
cd $(dirname $0)
python -m atompages develop
"""


def init(root=None):
    """ initialize a new project.

    parameters:
        root: root of the project, defaults to current directory
    """
    root = os.getcwd() if root is None else root

    if os.path.isdir(root+"/source/"):
        print("'source' folder already exists, Existing files may be overwritten!")
    if input("Enter y to confirm to create project in %s\
                    \nor anything else to abort\n"%root).lower() =="y":

        copy_folder(base_dir+"/project_template/source", root+"/source")
        copy_folder(base_dir+"/project_template/plugins", root+"/plugins")

        script_filename = "develop.bat" if on_windows() else "develop.sh"
        with open(script_filename, "w") as f:
            f.write(develop_script)

        generate(root=root)

        print("\nDone. Start %s and let the magic happen"%script_filename)

def webserve(root=None, port=None, callback=None):
    """ starts a webserver in the output directory using a random free port
    and opens a browser tab to the content

        parameters:
            root: root of the project, defaults to current directory"""

    root = os.getcwd() if root is None else root
    def get_open_port():
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("",0))
        s.listen(1)
        port = s.getsockname()[1]
        s.close()
        return port

    static_dir_config = {
        'tools.staticdir.root': root+"/output/",
        "tools.staticdir.dir": "./",
        "tools.staticdir.on": True}
    class Root:
        @cherrypy.expose
        def index(self):
            return open(root+"/output/index.html").read()

    port = get_open_port() if port is None else port
    global_options = {'server.socket_host':'127.0.0.1', 'server.socket_port':port,
                    'engine.autoreload.on': False}
    cherrypy.config.update(global_options)
    cherrypy.log.access_file = None
    for handler in tuple(cherrypy.log.access_log.handlers):
        cherrypy.log.access_log.removeHandler(handler)
    cherrypy.log.access_log.propagate = False

    try:
        if callback is not None:
            t = Thread(target=callback)
            t.daemon = True
            t.start()
            Timer(1.5, webbrowser.open_new_tab, args=["http://localhost:%i"%port]).start()
        cherrypy.quickstart(Root(), '/',  config={"/": static_dir_config})
    except (KeyboardInterrupt, SystemExit):
        sys.exit()



def develop(root=None, port=None):
    """ Start project development mode
    Opens a webbrowser pointing to your compiled webpage
    Automatically listens for file changes in source and recompiles

    parameters:
        root: root of the project, defaults to current directory
    """
    root = os.getcwd() if root is None else root
    sys.argv.insert(-1,"dev=true")

    def callback():
        from atompages import autocompiler
        autocompiler.main(root=root)
    #webserve needs to be started as main thread, hence the callback
    import time
    webserve(root=root, callback=callback)

def generate(root=None):
    """generates the web page

        parameters:
            root: root of the project, defaults to current directory"""
    root = os.getcwd() if root is None else root
    from atompages import generate_pages
    generate_pages.build_site(root)

def get_images(base_dir="./"):
    """return the markdown include code for all images in base_dir (default: current directory)
    """
    base_dir = os.path.abspath(base_dir).replace("\\","/")
    if not "/static/img/" in base_dir:
        raise RuntimeError("Images need to be located in the /static/img/ folder of your project")
    img_paths = sum([[root+"/"+f for f in files] for root, folders, files in os.walk(base_dir)], [])

    img_paths = filter(lambda i: True in [i.lower().endswith(s) for s in ['jpg','png','gif']], img_paths)
    img_paths = [p.replace("//","/") for p in img_paths]
    img_paths = ["![](/static/img/%s)" % (img.split("/static/img/")[-1].replace("\\","/")) for img in img_paths]

    for entry in img_paths:
        print(entry)

cmdline_functions = {"init": init, "develop":develop, "webserve":webserve,
                     "generate": generate, "get_images": get_images}

def print_help(fkt_name):
    fkt = cmdline_functions[fkt_name]
    print("\nhelp for %s:\n\n %s\n"%(fkt_name, fkt.__doc__))


def main():
    try:
        target = sys.argv[1]
        options = dict([tuple(arg.split("=")[:2]) for arg in sys.argv[2:] if "=" in arg])

        cmdline_functions[target](**options)
    except Exception as e:
        logging.exception(e)
        if "target" in locals() and target in cmdline_functions:
            print_help(target)
        else:
            print("Available commands:")
            for fkt in cmdline_functions:
                print_help(fkt)
    except KeyboardInterrupt:
        exit()

if __name__ == "__main__":
    main()
