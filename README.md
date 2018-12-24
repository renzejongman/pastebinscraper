# pastebinscraper
Scrapes pastebin, stores the paste-keys in a local database and returns the ones that haven't been seen yet.

#
#           Pastebin Scraper
#   By:     Renze Jongman
#   Date:   24 December 2018
#
# scraper for the most recent pastebinposts, stores the keys in a database, and allows for inspection of the content by other scripts.
# You can write scripts to use the output of this one to search on pastebin for whatever you are interested in.
# Just make sure you:
#
# 1. create a PRO-account with Pastebin
# 2. Whitelist your IP on pastebin
# 3. Add the tables that are relevant to you (with email addresses, domains, BIN-numbers; whatever) (optional)
# 4. Write a script to pull the pastes and inspect them by calling the scraper class below
# 5. Set a cron-job to do it periodically (every minute or so)
