#!/usr/bin/python3

import sys, logging, os, time
import pymysql.cursors
import daemon

VERSION = "0.1"

def startCrawler():
    #parse arguments, get options
    credFile="credentials"
    for arg in sys.argv:
        if ("=" in arg):
            arg = arg.split("=")
            if arg[0] == "credentials":
                credFile = arg[1]

    # get credentials, put em in a dict
    creds = {"api-server": "oce", "db-host": "localhost", "db-charset": "utf8mb4"}
    f = open(credFile, "r")
    for line in f:
        line = line.strip()
        if ("=" in line):
            line = line.split("=")
            creds[line[0]] = line[1]
    if "api-url" not in creds:
        creds["api-url"] = "{0}api.pvp.net/api/lol/{0}/v2.2/".format(creds["api-server"])
    f.close()

    # transform this process into a daemon
    # NOTE: we will use the current directory as the working directory (for logging etc)
    context = daemon.DaemonContext(working_directory=os.getcwd())
    context.open()

    # initialize logger
    logging.basicConfig(filename="crawler.log", format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
    logging.info("Starting ARAM crawler v{0}".format(VERSION))

    # connect to mysql database
    #logging.info("Connecting to mysql database at {0}".format(creds["db-host"]))
    '''conn = pymysql.connect(
            host=creds["db-host"],
            user=creds["db-user"],
            password=creds["db-password"],
            db=creds["db-name"],
            charset=creds["db-charset"],
            cursorclass=pymysql.cursors.DictCursor)

    conn.close()'''

    WAITTIME = 1

    # start main loop
    while True:
        startTime = time.time()
        # Here is where we do things
        # --------------------------
        logging.info("Making one query")
        time.sleep(1.2)
        # --------------------------
        waitPeriod = WAITTIME-(time.time()-startTime)
        if waitPeriod > 0:
            logging.info("Waiting {0}".format(waitPeriod))
            time.sleep(waitPeriod)

if __name__ == "__main__":
    startCrawler();
