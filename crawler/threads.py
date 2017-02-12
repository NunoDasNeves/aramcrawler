import logging, time
import threading, queue
from crawler import database, tasks
import signal

VERSION = 0.1
# 500 requests every 10 mins = 1 request per 1.2 seconds
API_WAIT = 1.21
# how many seconds to wait if there are no tasks to do
TIMEOUT = 60
# our queue of tasks to do
taskList = queue.Queue()
# a special flag for killing our threads safely
killFlag = False

def killThreads(signum, frame):
    logging.info("SIGINT or SIGTERM detected, quitting...")
    global killFlag
    killFlag = True

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
        tasks.NUM_THREADS += 1

    # set up signal handlers
    signal.signal(signal.SIGINT, killThreads)
    signal.signal(signal.SIGTERM, killThreads)

    # block until threads are finished
    for t in threads:
        t.join()
    logging.info("ARAM CRAWLER QUITTING")


class ApiThread(threading.Thread):
    def __init__(self, apiKey):
        threading.Thread.__init__(self)
        self.apiKey = apiKey

    def run(self):
        logging.info("[{}] Starting".format(self.ident))
        conn = database.getConnection()
        timeout = 0
        while True:
            logging.info('[{}] killFlag: {}'.format(self.ident, killFlag))
            # get the current time so we can time our API calls
            startTime = time.time()

            # get and execute the next task
            try:
                logging.info("[{}] Checking task list".format(self.ident))
                theTask = taskList.get(block=True, timeout=TIMEOUT)
                taskList.task_done()
                # if the killFlag is set, only do getMatchDetails then finish
                # this is because getMatchDetail will finish populating db rows
                if killFlag and theTask != tasks.getMatchDetail:
                    continue
                logging.info("[{}] Starting task: {}".format(self.ident, str(theTask)))
                # theTask will return an array of newTasks to add to the list
                newTasks = theTask(self.apiKey, conn)
                for t in newTasks:
                    taskList.put(t)
            except queue.Empty:
                logging.info("[{}] No tasks found after {} seconds".format(self.ident, TIMEOUT))
                break

            # wait the difference between the time we took to run and API_WAIT
            waitPeriod = API_WAIT-(time.time()-startTime)
            if waitPeriod > 0:
                logging.info("[{}] Waiting {}".format(self.ident, waitPeriod))
                time.sleep(waitPeriod)

        conn.close()
        logging.info("[{}] Dying".format(self.ident))

