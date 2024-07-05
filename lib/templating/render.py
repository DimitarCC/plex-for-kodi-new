# coding=utf-8
import os

from .core import engine
from lib.util import DEF_THEME, ADDON, getSetting, translatePath, THEME_VERSION, setSetting, DEBUG


def render_templates(theme=None, templates=None, force=False):
    # apply theme if version changed
    theme = theme or getSetting('theme', DEF_THEME)
    target_dir = os.path.join(translatePath(ADDON.getAddonInfo('path')), "resources", "skins", "Main", "1080i")

    if not engine.initialized:
        engine.init(target_dir, os.path.join(target_dir, "templates"),
                    os.path.join(translatePath(ADDON.getAddonInfo("profile")), "templates"))

    # fixme: in-development, remove
    if DEBUG:
        engine.apply(theme, templates=templates)

    curThemeVer = getSetting('theme_version', 0)
    if curThemeVer < THEME_VERSION or force:
        setSetting('theme_version', THEME_VERSION)
        # apply seekdialog button theme
        engine.apply(theme, templates=templates)

    # lose template cache for performance reasons
    #fixme: create setting for this
    engine.loader.cache = {}
