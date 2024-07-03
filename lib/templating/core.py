# coding=utf-8
import os
import glob

from kodi_six import xbmcvfs

from lib.logging import log as LOG, log_error as ERROR
from .util import deep_update
from .filters import *
from .themes import THEMES


def prepare_theme_data(thm):
    theme_data = {"INHERIT": thm}
    final_data = {}

    # data stack
    data_stack = []
    theme_tree = []

    # build inheritance stack
    while "INHERIT" in theme_data:
        inherit_from = theme_data.pop("INHERIT")
        theme_data = copy.deepcopy(THEMES[inherit_from])
        data_stack.append(theme_data)
        theme_tree.append(inherit_from)

    while data_stack:
        deep_update(final_data, data_stack.pop())

    return {"theme": final_data}


class TemplateEngine(object):
    loader = None
    target_dir = None
    template_dir = None
    initialized = False
    TEMPLATES = None

    def init(self, target_dir, template_dir, paths):
        self.target_dir = target_dir
        self.template_dir = template_dir
        self.get_available_templates()

        LOG("Looking for templates in: {}", paths)
        self.prepare_loader(paths)
        self.initialized = True

    def get_available_templates(self):
        tpls = []
        for f in glob.iglob(os.path.join(self.template_dir, "*.tpl.xml")):
            tpls.append(f.split("script-plex-")[1].split(".tpl.xml")[0])
        self.TEMPLATES = tpls

    def prepare_loader(self, fns):
        self.loader = ibis.loaders.FileLoader(*fns)
        ibis.loader = self.loader

    def compile(self, fn, data):
        template = self.loader(fn)
        return template.render(data)

    def write(self, template, data):
        try:
            # write final file
            f = xbmcvfs.File(os.path.join(self.target_dir, "script-plex-{}.xml".format(template)), "w")
            f.write(data)
            f.close()
            return True
        except:
            ERROR("Couldn't write script-plex-{}.xml".format(template))
            return False

    def apply(self, theme=None, templates=None):
        templates = self.TEMPLATES if templates is None else templates
        theme_data = prepare_theme_data(theme)

        applied = []
        for template in templates:
            compiled_template = self.compile("script-plex-{}.tpl.xml".format(template), theme_data)
            if self.write(template, compiled_template):
                applied.append(template)
            else:
                raise Exception("Couldn't write script-plex-{}.tpl.xml".format(template))
        LOG('Using theme {} for: {}'.format(theme, applied))


engine = TemplateEngine()