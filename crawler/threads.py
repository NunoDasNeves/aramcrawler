import logging, time
import threading, queue
from crawler import database, tasks

# TODO: implement a cache
# from crawler import cache

VERSION = 0.1
# 500 requests every 10 mins = 1 request per 1.2 seconds
API_WAIT = 1.21
# our queue of tasks to do
taskList = queue.Queue()
# a special flag for killing our threads safely
killFlag = False

def startThreads(keys, job):
    # put tasks in the queue
    if job == "crawl-games":
        logging.info("Starting ARAM crawler v{0}".format(VERSION))
    elif job == "get-static":
        logging.info("Getting static champions and items data")
        # TODO: remove, testing only
        taskList.put(tasks.getMatchDetail)
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
        logging.info("Thread {} starting".format(self.ident))
        conn = None
        while True:
            if killFlag: break
            startTime = time.time()
            try:
                # make sure we have an active mysql connection
                if conn is None:
                    logging.info("In the thread; no database connection, making one now")
                    conn = database.getConnection()
                # Here is where we do things
                # --------------------------
                if conn is not None:
                    logging.info("In the thread making one query")
                    theTask = taskList.get()
                    taskList.task_done()
                    theTask(self.apiKey, conn)
                # --------------------------
            except:

                logging.error("Oh no! something went wrong. Getting next task...")

            waitPeriod = API_WAIT-(time.time()-startTime)
            if waitPeriod > 0:
                logging.info("Waiting {0}".format(waitPeriod))
                time.sleep(waitPeriod)

        if cnn is not None:
            conn.close()
        logging.info("Thread {} dying".format(self.ident))

