from crawler import database
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
    pass

# setup-tables tasks
def setupTables():
    pass
