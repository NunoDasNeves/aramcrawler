from crawler import database
from crawler.schema import DATA_MAP
import config
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
def getMatchDetail(matchId, apiKey) # gets details of 1 ARAM
    ENDPOINT = 'match-v2.2'
    # get match details
    # if queue is empty, put a getGames in the queue for each api key
    # - MatchDetails
    # - PlayerStats
    data = queryApi(ENDPOINT, apiKeyi, matchId)
    processData(endpoint, data)

def processData(endpoint):
    queries = []
    # make a new sql query for each table
    for table in DATA_MAP:
            sql = ""
            # check each field to see if there's a function mapped to this endpoint
            for field in table:
                if endpoint in field:
                    # execute said function, giving it the api data
                    fSig = field[endpoint]
                    fSig['d'] = data
                    sql.append(fSig.function(**fSig.args, **fSig.kwargs))

            queries.append(sql)
            logging.info("SQL: "+sql)

    database.updateTable(queries)

def queryApi(endpoint, key, params):
    import urllib, json
    prts = endpoint.split('-')
    # match-v2.2, params -> v2.2/match/params
    ext = '/'.join([prts[1],prts[0],str(params)])
    data = urllib.request.urlopen(config.apiUrl+ext+'?api_key='+key, None)
    logging.info("**************** data ****************\n")
    return json.loads(data)

# setup-tables tasks
def setupTables():
    pass
