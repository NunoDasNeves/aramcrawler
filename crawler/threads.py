import logging, time
import threading, queue
from crawler import database, tasks

# TODO: implement a cache
# from crawler import cache

VERSION = 0.1
# 500 requests every 10 mins = 1 request per 1.2 seconds
API_WAIT = 1.21
# how many API_WAIT's to wait if there are no tasks to do
TIMEOUT = 3
# our queue of tasks to do
taskList = queue.Queue()
# a special flag for killing our threads safely
killFlag = False

def startThreads(keys, job):
    # put tasks in the queue
    if job == "crawl-games":
        logging.info("Starting ARAM crawler v{0}".format(VERSION))
        taskList.put(tasks.getMatchDetail)
    elif job == "get-static":
        logging.info("Getting static champions and items data")
    else:
        return

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

    logging.info("ARAM CRAWLER DYING")


class ApiThread(threading.Thread):
    def __init__(self, apiKey):
        threading.Thread.__init__(self)
        self.apiKey = apiKey

    def run(self):
        logging.info("[{}] Starting".format(self.ident))
        conn = 1
        timeout = 0
        while True:
            if killFlag: break
            startTime = time.time()
            # make sure we have an active mysql connection
            #if conn is None:
            #    logging.info("In the thread; no database connection, making one now")
            #    conn = database.getConnection()
            # Here is where we do things
            # -------------------------- #
            if conn is not None:
                try:
                    logging.info("[{}] Checking task list".format(self.ident))
                    theTask = taskList.get(block=True, timeout=TIMEOUT)
                    taskList.task_done()
                    logging.info("[{}] Starting task: {}".format(self.ident, str(theTask)))
                    theTask(self.apiKey, conn)
                except queue.Empty:
                    logging.info("[{}] No tasks found after {} seconds".format(self.ident, TIMEOUT))
                    break
            # -------------------------- #
            waitPeriod = API_WAIT-(time.time()-startTime)
            if waitPeriod > 0:
                logging.info("[{}] Waiting {}".format(self.ident, waitPeriod))
                time.sleep(waitPeriod)

        #if conn is not None:
        #    conn.close()
        logging.info("[{}] Dying".format(self.ident))

