# coding: utf-8

import os, sys, logging, re, threading

from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from atompages.generate_pages import build_site

logger = logging.getLogger(__name__)

class FileEventHandler(FileSystemEventHandler):
    def __init__(self, updateFkt):
        self.updateFkt = updateFkt
        self.last_files = []
        self.updateFkt(["."])
        self.hashes = {}

        self.on_moved = self.on_created = self.on_deleted = self.on_modified = self.somethings_changed

    def check_has_really_changed(self, paths):
        def check_path(path):
            if not os.path.isfile(path):
                return False
            if not path in self.hashes:
                self.hashes[path] = os.path.getmtime(path)
                return True
            if not os.path.getmtime(path) == self.hashes[path]:
                self.hashes[path] = os.path.getmtime(path)
                return True
        return True in [check_path(path) for path in paths]

    def somethings_changed(self, event=None):
        try:
            if event is not None:
                self.last_files.append(event.src_path)
                if self.check_has_really_changed(self.last_files):
                    logger.info("\nChanged files: \n  %s\n" % "\n  ".join(self.last_files))
                    threading.Thread(target=self.updateFkt(self.last_files[:])).start()
                    self.last_files = []
        except Exception as e:
            logger.exception(e)


def main(root, src_path=None, threaded=True):
    src_path = os.path.join(root, "source") if src_path is None else src_path

    def update_fkt(src_paths, ignore_patterns=[".*.scss.css$", ".*.scss$",".*\.pyc$", ".*\\output.*"]):
        print("Checking update for \n%s"%"\n".join(src_paths))
        for path in src_paths:
            if not True in [not not re.match(pat,path) for pat in ignore_patterns]:
                logger.info("Building site for %s"%path)
                return build_site(root)
            else:
                logger.info("File matches ignore pattern: %s"%path)
        #if False in [True in [not not re.match(pat, path) for pat in ignore_patterns] for path in src_paths]:
    #        build_site(root)


    event_handler = FileEventHandler(update_fkt)
    observer = Observer()
    observer.schedule(event_handler, src_path, recursive=True)

    if threaded:
        threading.Thread(target=observer.start, args=[]).start()
    else:
        try:
            observer.start()
        except KeyboardInterrupt:
            observer.stop()
        observer.join()

# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4 fenc=utf-8
