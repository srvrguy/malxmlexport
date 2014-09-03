#!/usr/bin/env python
# -*- coding: us-ascii -*-
# vim:ts=4:sw=4:softtabstop=4:smarttab:expandtab
#
from ConfigParser import SafeConfigParser
from optparse import OptionParser
from BeautifulSoup import BeautifulSoup
import requests
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


class LoginError(Exception):
    pass


def do_cleanup(keep, list_type):
    global save_path

    file_list = sorted([f for f in os.listdir(save_path) if f.startswith(list_type)])

    total_files = len(file_list)

    if total_files > keep:

        for x in range(total_files - keep):
            file_name = file_list[x]
            log.info('Removing %s' % file_name)
            os.remove(save_path + '/' + file_name)


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

    log.info("Downloading %s from %s%s" % (download_name, MAL_ROOT, download_link))

    r = session.get(
        MAL_ROOT + download_link,
        headers={"user-agent": user_agent}
    )

    export = open(save_path + '/' + download_name, 'w')

    export.write(r.content)


def cookie_login(username, password):
    global user_agent

    log.debug("Attempting to login to MAL")

    form_login = {'username': username, 'password': password, 'sublogin': 'Login'}
    r = session.post(
        MAL_ROOT + "/login.php",
        data=form_login,
        headers={"user-agent": user_agent}
    )

    text = BeautifulSoup(r.content)

    error_html = text.find('div', attrs={'class': 'badresult'})

    if error_html:
        error_msg = error_html.contents[0]
        pos = error_msg.find('.') + 1
        if pos > 0:
            raise LoginError(error_msg[:pos])
        else:
            raise LoginError(error_msg)


def main():
    global save_path, log
    global user_agent

    error = True

    parser = OptionParser()
    parser.add_option("-v", "--verbose", action="store_true", dest="verbose",
                      help="enable verbose messages")
    parser.add_option("-d", "--debug", action="store_true", dest="debug",
                      help="enable debug messages")

    (options, args) = parser.parse_args()

    if options.verbose:
        log.setLevel(logging.INFO)
    if options.debug:
        log.setLevel(logging.DEBUG)

    config = SafeConfigParser()
    config.read([os.path.expanduser('~/.malexport.conf')])

    try:
        save_path = config.get('global', 'save_path')
        user_agent = config.get('global', 'user_agent')
        keep_count = config.getint('global', 'keep')
        wants_anime = config.getboolean('global', 'anime')
        wants_manga = config.getboolean('global', 'manga')
        username = config.get('auth', 'username')
        password = config.get('auth', 'password')
    except Exception:
        log.critical("Could not load configuration data. Please make sure the "
                  "configuration file has been created and all values are "
                  "specified.")
        raise

    try:
        cookie_login(username, password)

        if wants_anime:
            do_export(1)
            do_cleanup(keep_count, 'animelist')

        if wants_manga:
            do_export(2)
            do_cleanup(keep_count, 'mangalist')

    except LoginError, (e):
        log.critical("Login Failed. MAL said: '%s'" % e.message)

    else:
        error = False

    finally:
        return int(error)


if __name__ == "__main__":
    sys.exit(main())
