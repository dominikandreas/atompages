# coding: utf-8

import os, sys, logging, webbrowser, cherrypy

from threading import Thread, Timer

logger = logging.getLogger(__name__)

def serve(directory, listen, port, callback=None):
    """
    Starts a webserver in the output directory using a random free port and
    opens a browser tab to the content

        parameters:
            directory: root of the project, defaults to current directory
    """
    if directory is None:
        raise RuntimeError("directory not set")
    elif port is None:
        raise RuntimeError("port not set")

    logger.info('serving {}, listening on {}:{}'.format(directory, listen, port))

    static_dir_config = {
        'tools.staticdir.root': os.path.abspath(directory),
        "tools.staticdir.dir":  './',
        "tools.staticdir.on":   True
    }

    class Root:
        @cherrypy.expose
        def index(self):
            with open(os.path.join(directory, "index.html")) as stream:
                return stream.read()

    global_options = {
        'server.socket_host':   listen,
        'server.socket_port':   port,
        'engine.autoreload.on': False
    }

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
            Timer(1.5, webbrowser.open_new_tab, args=["http://localhost:%i" % port]).start()

        cherrypy.quickstart(Root(), '/',  config={"/": static_dir_config})
    except (KeyboardInterrupt, SystemExit):
        sys.exit()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
