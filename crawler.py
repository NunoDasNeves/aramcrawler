#!/usr/bin/python3

import sys, logging, os, time
import pymysql.cursors
import daemon
import threading, queue

VERSION = "0.1"
# 500 requests every 10 minutes = 1.2 requests per second. Plus an extra 0.01 just in case
API_WAIT = 1.21

def startCrawler():
    #parse arguments, get options
    credFile = None
    task = None
    makeTables = False
    logFile = "crawler.log"
    for arg in sys.argv[1:]:
        if ("=" in arg):
            arg = arg.split("=")
            if arg[0] == "credentials":
                credFile = arg[1]
            elif arg[0] == "logfile":
                logFile = arg[1]
            elif arg[0] == "task":
                task = arg[1]
        elif arg == "--example-creds":
            task = "example-creds"

    # print a handy usage message if the user didn't enter enough options
    if task is None or task not in ["get-static","crawl-games-daemon","setup-tables"]:
        sys.stderr.write ("Usage: {0} [task=get-static|crawl-games-daemon|setup-tables credentials=[FILE] logfile=[FILE]] [--example-creds]\n".format(sys.argv[0]))
        exit(1)

    if task in ["get-static", "crawl-games-daemon", "setup-tables"] and credFile == None:
        sys.stderr.write("Please include a credentials file\n")
        exit(1)

    # print out a helpful example of what a credentials file should look like
    if task == "example-creds":
        print ("api-keys=key1,key2\napi-server=na\ndb-host=localhost\ndb-name=mydb\ndb-user=root\ndb-password=root\ndb-charset=utf8mb64")
        exit(0)

    # get credentials, put em in a dict
    creds = {"api-server": "oce", "db-host": "localhost", "db-charset": "utf8mb4"}
    f = open(credFile, "r")
    for line in f:
        line = line.strip()
        if ("=" in line):
            line = line.split("=")
            if line[0] == "api-keys":
                creds["api-keys"] = []
                for key in line[1].split(","):
                    creds["api-keys"].append(key)
            else:
                creds[line[0]] = line[1]
    # construct api url
    if "api-url" not in creds:
        creds["api-url"] = "{0}api.pvp.net/api/lol/{0}/v2.2/".format(creds["api-server"])
    f.close()

    # make sure we have database credentials
    if any(c not in creds for c in ["db-host", "db-name", "db-user", "db-password"]):
        sys.stderr.write("Database credentials missing!\n")
        exit(1)

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

    if task == "setup-tables":
        print ("WARNING: ALL current data will be DELETED. \nType \"yes\" to confirm or anything else to exit")
        if input().strip() == "yes":
            print ("doing the tables")
            print ("done")
            #setupTables(conn)
        exit(0)

    if "api-keys" not in creds or len(creds["api-keys"]) == 0:
        sys.stderr.write("No api-keys found!")
        exit(1)

    # create our list of api tasks to do
    taskList = queue.Queue()

    if task == "crawl-games-daemon":
        # transform this process into a daemon
        # NOTE: we will use the current directory as the working directory (for logging etc)
        context = daemon.DaemonContext(working_directory=os.getcwd())
        context.open()

        print ("Logging to {0}".format(logFile))
        # initialize logging to file
        logging.basicConfig(filename=logFile, format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
        logging.info("Starting ARAM crawler v{0}".format(VERSION))
        # TODO: add tasks here
    elif task == "get-static":
        logging.basicConfig(format="%(asctime)s %(levelname)s %(message)s", level=logging.INFO)
        logging.info("Getting static champions and items data")
        # TODO: add tasks here

    # for each api key, start a new thread
    for key in creds["api-keys"]:
        t = ApiThread(key)
        t.daemon = False
        t.start()

class ApiThread(threading.Thread):
    def __init__(self, apiKey, taskList):
        threading.Thread.__init__(self)
        self.apiKey = apiKey
        self.taskList = taskList
    def run(self):
        while True:
            startTime = time.time()
            # Here is where we do things
            # --------------------------
            logging.info("Making one query")
            time.sleep(0.8)
            # --------------------------
            waitPeriod = API_WAIT-(time.time()-startTime)
            if waitPeriod > 0:
                logging.info("Waiting {0}".format(waitPeriod))
                time.sleep(waitPeriod)


if __name__ == "__main__":
    startCrawler();
