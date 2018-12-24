#! /usr/bin/env Python3
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

import os, sqlite3, requests, logging
from sqlite3 import Error
from pathlib import Path



logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


class scraper:


    def __init__(self):
        self.current_dir = os.path.dirname(os.path.abspath(__file__))
        
        self.DATABASE = "{}/data/pastebinscraper.db".format(self.current_dir)
        self.USERNAME = "" # Pastebin username
        self.PASSWORD = "" # Pastebin password


        # Sets SQL-commands for creating the paste-table.
        self.pastes_sql = """
        CREATE TABLE IF NOT EXISTS pastes (
        id integer PRIMARY KEY,
        paste_key text NOT NULL,
        title text,
        date integer NOT NULL,
        user text,
        size integer NOT NULL
        );
        """

    def check_db(self):
        # checks if the database exists. If not: it creates one, with one table for the pastes. Returns True if the database is already present.
        
        db = Path(self.DATABASE)
        if db.is_file():
            logging.debug("database found at {}".format(self.DATABASE))
            return True
                         
        else:
            logging.debug("No database found. Creating a new one.")
            conn = s.db_connect()
            if conn is not None:
                self.create_tables(conn, pastes_sql)

                logging.debug("Created the database.")
            return False


    def db_connect(self):
        # Sets up the connection to the database and returns the connection as an object.

        try:
            conn = sqlite3.connect(self.DATABASE)
            return conn
        except Error as e:
            print(e)

        return None


    def create_tables(self, conn, logic):
        # Create tables in the database
        # A table for the pastes itself is created automatically on first run. More tables can be created for bespoke monitoring however.

        try:
            c = conn.cursor()
            c.execute(logic)
        except Error as e:
            print(e)


    def pull_new_pastes(self, conn):
        # Checks Pastebin for pastes that are not in the local database yet (by key), and returns a list of every paste thats new.
        # Pastebin allows for a maximum of 250 on it's API.


        newPastes = []
        r = requests.get('https://scrape.pastebin.com/api_scraping.php?limit=250')
        pastelist =  r.json()
        for x in range(len(pastelist)):
                pastekey = pastelist[x]['key']
                newPastes.append(pastekey)

                c = conn.cursor()

                #Check if the key is already in the database
                c.execute("SELECT paste_key from pastes WHERE paste_key = '{}';".format(pastekey))
                exist = c.fetchone()
                
                if exist is not None: 
                    #key is in the database.

                    logging.debug("paste with key {} already present in the database!".format(pastekey))
                else:
                    #Key is not in the database and needs processing.

            
                    sql = "INSERT INTO pastes(paste_key,title,date,user,size) VALUES ('{}','{}',{},'{}',{});".format(pastekey, pastelist[x]['title'],pastelist[x]['date'], pastelist[x]['user'], pastelist[x]['size'])
                
                    with conn:
                        try:
                            c.execute(sql)
                        except Error as e:
                            logging.error(e)
                    logging.debug('New paste found. Added {} to the database and processing'.format(pastekey))
        return newPastes


if __name__ == "__main__":
    print("\n***** PASTEBIN SCRAPER\n***** By Renze Jongman\n*****\n***** This is not a stand-alone script. Use it to pull a list of Pastebin-posts and process them in another script of your own.\n\n\n")
    
    



    
