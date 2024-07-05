# coding=utf-8

THEMES = {
    "base": {
        # general config
        "assets": {
            "buttons": {
                "base": "script.plex/buttons/",
                "focusSuffix": "-focus",
            }
        },
        "buttons": {
            "useFocusColor": True,
            "useNoFocusColor": True,
            "zoomPlayButton": False,
            "focusColor": None,
            "noFocusColor": None
        },

        # specific interface config
        "episodes": {
            "use_button_bg": False,
            "button_bg_color": None,
            "buttongroup": {
                "posy": None
            },
            # this button group will only exist when multiple media files for an episode exist, it adds another button
            "buttongroup_1300": {
                "posy": None
            },
            # applies to the main buttons
            "buttons": {
                "width": None,
                "height": None,
            }
        }
    },
    "classic": {
        "INHERIT": "base",
        "episodes": {
            "buttongroup": {
                "posy": 393
            },
            "buttongroup_1300": {
                "posy": "412.5"
            },
            "buttons": {
                "width": 176,
                "height": 140
            },
            "buttons_1300": {
                "width": 161,
                "height": 125
            }
        }
    },
    "modern": {
        "INHERIT": "base",
        "assets": {
            "buttons": {
                "base": "script.plex/buttons/player/modern/",
                "focusSuffix": "",
            }
        },
        "buttons": {
            "useFocusColor": False,
            "zoomPlayButton": True,
            "noFocusColor": "88FFFFFF"
        },
        "episodes": {
            "buttongroup": {
                "posy": 393
            },
            "buttongroup_1300": {
                "posy": 393
            },
            "buttons": {
                "width": 131,
                "height": 104,
            },
            "buttons_1300": {
                "width": 131,
                "height": 104
            }
        }
    },
    "modern-colored": {
        "INHERIT": "modern",
        "buttons": {
            "useFocusColor": True,
            "zoomPlayButton": False,
        }
    },
    "modern-dotted": {
        "INHERIT": "modern",
        "assets": {
            "buttons": {
                "base": "script.plex/buttons/player/modern-dotted/",
                "focusSuffix": "-focus",
            }
        },
        "buttons": {
            "useFocusColor": False,
            "zoomPlayButton": False,
        }
    }
}