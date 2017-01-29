#!/usr/bin/python3

import logging, time
import threading, queue
from crawler import database

# 500 requests every 10 mins = 1 request per 1.2 seconds
API_WAIT = 1.21
# our queue of tasks to do
tasks = queue.Queue
# a special flag for killing our threads safely
killFlag = False

def startThreads(keys, job):

    threads = []
    # for each api key, start a new thread
    logging.info("Starting {0} threads".format(len(keys)))
    for key in keys:
        t = ApiThread(key)
        t.daemon = False
        t.start()
        threads.append(t)

    # block until threads are finished
    for t in threads:
        t.join()


class ApiThread(threading.Thread):
    def __init__(self, apiKey):
        threading.Thread.__init__(self)
        self.key = apiKey

    def run(self):
        while True:
            if killFlag: break
            # make sure we have an active mysql connection
            #if not conn:
            #    getMySqlConnection
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

