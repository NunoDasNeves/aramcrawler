#!/usr/bin/python3

import sys, logging, os, time
import pymysql.cursors
import daemon
from crawler import threads, database
import config

def startCrawler():
    #parse arguments, get options
    task = None
    daemon = False
    logFile = "/tmp/aramcrawler.log"
    for arg in sys.argv[1:]:
        if ("=" in arg):
            arg = arg.split("=")
            if arg[0] == "logfile":
                logFile = arg[1]
            elif arg[0] == "task":
                task = arg[1]
        elif arg == "--daemon":
            daemon = True

    # print a handy usage message if the user didn't enter enough options
    if task is None or task not in ["get-static","crawl-games","setup-tables"]:
        sys.stderr.write ("Usage: {0} task=get-static|crawl-games|setup-tables [logfile=[FILE]] [--daemon]\n".format(sys.argv[0]))
        exit(1)

    if task == "setup-tables":
        print ("WARNING: ALL current data will be DELETED. \nType \"yes\" to confirm or anything else to exit")
        if input().strip() == "yes":
            print ("Creating the tables")
            cnx = database.getConnection()
            database.setupTables(cnx)
            print ("Done")
        exit(0)

    if daemon == True:
        print ("Logging to {0}".format(logFile))
        # transform this process into a daemon
        # NOTE: we will use the current directory as the working directory
        context = daemon.DaemonContext(working_directory=os.getcwd())
        context.open()
        # initialize logging to file
        logging.basicConfig(
                filename=logFile, 
                format="%(asctime)s %(levelname)s %(message)s", 
                level=logging.INFO
            )
    else:
        logging.basicConfig(
                format="%(asctime)s %(levelname)s %(message)s", 
                level=logging.INFO
            )

    threads.startThreads(config.apiKeys, task)

if __name__ == "__main__":
    startCrawler();
