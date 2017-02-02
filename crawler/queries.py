from crawler import database
from crawler import schema
# tasks are the top-level of this program
# each api query type 

# static-data tasks
def getChampData():
    # - Champions
    pass
def getItemData():
    # - Items
    pass

# crawl-games tasks
# start with 1 getGames task per api key
def getGames(summonerId): # returns 0-10 ARAMs, 5-40 summoners
    # get games, put a getMatchDetail in the queue for each ARAM we got
    # if no arams, put another getGames in the queue for each api key
    pass
    # - MatchDetails
    # - PlayerStats
    # - Summoners
def getMatchDetail(matchId) # gets details of 1 ARAM
    # get match details
    # if queue is empty, put a getGames in the queue for each api key
    # - MatchDetails
    # - PlayerStats
    logging.info("SQL is: "+sql)
    pass

def doApiCall(endpoint, key):
    #data = json.loads(data)
    return {}

def queryApi(endpoint, key):
    data = doApiCall(endpoint,key)
    for table in dataMap:
        sql = ""
        for field in table:
            if endpoint in field:
                fSig = field[endpoint]
                fSig['d'] = data
                sql.append(fSig.function(**fSig.args, **fSig.kwargs))


# setup-tables tasks
def setupTables():
    pass
