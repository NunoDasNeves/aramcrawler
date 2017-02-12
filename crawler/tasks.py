from crawler import database
from crawler.schema.match import SCHEMA as CRAWLER_SCHEMA
from crawler.schema.static import SCHEMA as STATIC_SCHEMA
import config
import logging
import queue
import urllib.request, json

# ------ CACHING ------
# How many seconds we keep stuff
CACHE_TIMEOUT = 3600*24*1
# queue for which matchId to query next! whee
matchIds = queue.Queue()
# We can throw away matchIds whos summoners we've already queried
# matchid:{summonerid1,summonerid2,summonerid3}
matchIdCache = {}
# Summonerids, ordered by whether the summoner was in an ARAM
summonerIds = queue.PriorityQueue()
# We can throw away summonerIds once they're CACHE_TIMEOUT old (??)
summonerIdCache = {}
# ---------------------
NUM_THREADS = 0

# static-data tasks
def getChampData():
    # - Champions
    pass
def getItemData():
    # - Items
    pass

def getGames(apiKey, conn): # returns 0-10 ARAMs, 5-40 summoners
    """
    Gets games from a summoner's history (not full game information)
    Cache summoner names and matchIds for later queries
    """
    ENDPOINT = 'game-v1.3'
    # TODO: get summonerId from cache>table>initial
    summonerId = summonerIds.get()
    summonerIds.task_done()
    # get the data from the API
    data = queryApi(ENDPOINT, apiKey, summonerId)
    noNewArams = 0
    noArams = 0
    for game in data['games']:
        if game['gameMode'] == 'ARAM':
            noArams += 1
            gameId = game['gameId']
            matchIds.put(gameId)
            queries = processData(ENDPOINT, game, "INSERT", CRAWLER_SCHEMA)
            #database.updateTable(queries, conn)

        # - MatchDetails
        # - PlayerStats
        # - Summoners

    # If there are arams to query, add tasks for them!
    if noArams > 0:
        return [getMatchDetail]*noArams
    # Otherwise, add getGames if we don't have enough matches left for our threads
    diff = NUM_THREADS - matchIds.qsize()
    if diff > 0:
        return [getGames]*diff
    return []

def getMatchDetail(apiKey, conn):
    """ Gets details of 1 ARAM """
    ENDPOINT = 'match-v2.2'
    # get match details
    # if queue is empty, put a getGames in the queue for each api key
    # - MatchDetails
    # - PlayerStats
    # TODO: get matchId from cache>database>hardcoded
     # CACHE CHECK. basically we need to check if the match has been queried already
    # if game not in cache AND not in database, then we can query it
    gameId = game['gameId']
    if gameId in matchIdCache:
        matchIdCache[gameId].insert(data['summonerId'])
        # remove matchId from cache if all summoners in that game have been queried
        if len(matchIdCache[gameId]) == 10:
            del matchIdCache[gameId]
    # if the match hasn't been populated yet, there will be no participants
    rows = database.getRows('Participants', gameId)
    if len(rows) > 0:
        pass
    # so if the match doesn't exist, we're gonna put it in our queue of matches to query
    data = queryApi(ENDPOINT, apiKey, matchId)
    queries = processData(ENDPOINT, data, "UPDATE", CRAWLER_SCHEMA)
    #database.updateTable(queries, conn)

    # add getGames if we don't have enough matches left for our threads
    diff = NUM_THREADS - matchIds.qsize()
    if diff > 0:
        return [getGames]*diff
    return []

def processData(endpoint, data, sqlCommand, schema):
    """ Maps an api response to an array of SQL database queries """
    queries = []
    # make a new sql query for each table
    for tableName, fields in schema.items():
        #logging.info("doing table: " + tableName)
        # check each field to see if there's a function mapped to this endpoint
        rows = []
        values = []
        for fieldName, field in fields.items():
            #logging.info("   doing field: " + fieldName)
            if endpoint in field.keys():
                # execute said function, giving it the api data
                fSig = field[endpoint]
                fSig.kwargs['d'] = data
                values.append(str(fSig.function(**fSig.kwargs)))
                rows.append(fieldName)
        sql = sqlCommand+" `"+tableName+"` (`"+'`,`'.join(rows)+'`) VALUES ('+','.join(values)+')'
        queries.append(sql)
    logging.info(queries)
    return queries

def queryApi(endpoint, key, params):
    """ Queries the remote API and returns a dict with the data """
    # first create the right url
    prts = endpoint.split('-')
    # match-v2.2, params -> v2.2/match/params
    ext = '/'.join([prts[1],prts[0],str(params)])
    url = config.apiUrl+ext+'?api_key='+key
    logging.info("Querying: "+url)
    # do the query, convery from json to dict
    data = json.loads(urllib.request.urlopen(url, None).read())
    logging.info("Got data!")
    #logging.info("**************** data ****************\n"+str(data)+"\n***************************")
    return data

# setup-tables tasks
def setupTables():
    pass
