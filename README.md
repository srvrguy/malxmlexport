Simple MAL XML Exporter
=======================

This is a simple script that automates the download of your anime and manga
lists from the MyAnimeList website.

Normally, exporting your anime and manga list from MyAnimeList is a manual
task that requires going to a special export page and downloading each file
manually. This script allows you to put in your credentials and then download
any of your lists by simply running it. Use this as a scheduled task to make
regular backups for safe keeping.

This project is not sponsored by, endorsed by, or affiliated with MyAnimeList, a
property of CraveOnline, LLC.


Requirements
------------
This tool was tested and developed with Python 2.7 and uses the BeautifulSoup
and request modules. You will need to have these installed to run the tool.

You can install the modules using the pip tool or the way you would normally
install Python modules.

This script has only been tested under OS X and Linux.


Installation
------------
Place the main python script in the directory of your choosing.

Make a copy of malexport.conf.sample and save it as .malexport.conf in your
home directory. You will need to edit the values in the file to include the
username and password you use for your MyAnimeList account and a whitelisted
user agent for the MAL website.

To download XML backups, simply run the script.


Contributing
------------
Contributions are welcome as either pull requests, patches, or even bug reports.


License
-------
The Simple MAL XML Exporter is Copyright © 2014 Michael Johnson. It is licensed
under the Simplified BSD License.