#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
from ConfigParser import SafeConfigParser
import requests
from BeautifulSoup import BeautifulSoup
import logging
import os
import sys

MAL_ROOT = "http://myanimelist.net"
user_agent = ""  # Set in main() during the config read

session = requests.Session()

save_path = ''

log = logging.getLogger('malexport')
log_format = logging.Formatter('[%(levelname)s] %(message)s')

log_handler = logging.StreamHandler()
log_handler.setFormatter(log_format)

log.addHandler(log_handler)


def do_export(item_type):
    global user_agent, save_path, log

    url_params = {'go': 'export'}
    form_export = {'subexport': 'Export My List', 'type': item_type}

    r = session.post(
        MAL_ROOT + "/panel.php",
        params=url_params,
        data=form_export,
        headers={"user-agent": user_agent}
    )

    text = BeautifulSoup(r.content)

    download_html = text.find('div', attrs={'class': 'goodresult'}).a

    download_link = download_html.get('href')
    download_name = download_html.contents[0]

    log.info("Downloading list %s from %s" % (download_name, download_link))

    r = session.get(
        MAL_ROOT + download_link,
        headers={"user-agent": user_agent}
    )

    export = open(save_path + '/' + download_name, 'w')

    export.write(r.content)


def cookie_login(username, password):
    global user_agent

    form_login = {'username': username, 'password': password, 'sublogin': 'Login'}
    session.post(
        MAL_ROOT + "/login.php",
        data=form_login,
        headers={"user-agent": user_agent}
    )


def main():
    global save_path, log
    global user_agent

    error = False

    config = SafeConfigParser()
    config.read([os.path.expanduser('~/.malexport.conf')])

    try:
        save_path = config.get('global', 'save_path')
        user_agent = config.get('global', 'user_agent')
        wants_anime = config.getboolean('global', 'anime')
        wants_manga = config.getboolean('global', 'manga')
        username = config.get('auth', 'username')
        password = config.get('auth', 'password')
    except Exception:
        log.fatal("Could not load configuration data. Please make sure the "
                  "configuration file has been created and all values are "
                  "specified.")
        raise

    try:
        cookie_login(username, password)

        if wants_anime:
            do_export(1)

        if wants_manga:
            do_export(2)

    except:
        raise

    return int(error)


if __name__ == "__main__":
    sys.exit(main())
