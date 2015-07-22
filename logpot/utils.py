#-*- coding: utf-8 -*-

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'gif', 'jpeg'])

import os
import yaml

def loadSiteConfig(app):
    configfile = os.path.join(app.root_path, 'config.yml')
    if os.path.exists(configfile):
        f = open(configfile, 'r')
        data = yaml.load(f)
        f.close()
    else:
        data = {}
        data["site_title"]          = "Logpot"
        data["site_subtitle"]       = "This is a simple blog system build with Flask."
        data["site_author"]         = "Logpot"
        data["enable_link_github"]  = False
        data["enable_profile_img"]  = False
        data["display_poweredby"]   = True
        saveSiteConfig(app, data)

    app.config['site_title']          = data['site_title']
    app.config['site_subtitle']       = data['site_subtitle']
    app.config['site_author']         = data['site_author']
    app.config['enable_link_github']  = data['enable_link_github']
    app.config['enable_profile_img']  = data['enable_profile_img']
    app.config['display_poweredby']   = data['display_poweredby']
    return data

def saveSiteConfig(app, data):
    configfile = os.path.join(app.root_path, 'config.yml')
    f = open(configfile, 'w')
    yaml.dump(
        data,
        f,
        encoding='utf8',
        allow_unicode=True,
        default_flow_style=False
    )
    f.close()
    return True
