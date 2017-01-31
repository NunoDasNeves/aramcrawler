from crawler import database

# tasks are the top-level of this program schema
# each api query type 


# static data tasks
def getStaticData():
    # what api calls do we need
    getChampData()
    getItemData()
    # what tables do we need
    # - Champions
    # - Items


# crawling tasks
# start with 1 getGames task per api key
def getGames(summonerId): # returns 0-10 ARAMs, 5-40 summoners
    # get games, put a getMatchDetail in the queue for each ARAM we got
    # if no arams, put another getGames in the queue for each api key
    
    # - MatchDetails
    # - PlayerStats
    # - Summoners
def getMatchDetail(matchId) # gets details of 1 ARAM
    # get match details
    # if queue is empty, put a getGames in the queue for each api key
    # - MatchDetails
    # - PlayerStats
def setupTables():

MatchDetails:
matchId PRIMARY KEY BIGINT UNSIGNED
mapId TINYINT UNSIGNED
matchCreation BIGINT UNSIGNED
matchDuration INT UNSIGNED
matchMode VARCHAR(24) ARAM
matchType VARCHAR(24) MATCHED_GAME
matchVersion VARCHAR(24)
platformId VARCHAR(8)
queueType VARCHAR(24) ARAM_5x5
region VARCHAR(4)
season VARCHAR(24)
firstBlood TINYINT UNSIGNED
firstInhibitor TINYINT UNSIGNED
firstTower TINYINT UNSIGNED
team1inhibitorKills INT UNSIGNED
team2inhibitorKills INT UNSIGNED
team1towerKills TINYINT UNSIGNED
team2towerKills TINYINT UNSIGNED
winner TINYINT UNSIGNED

Participants
id PRIMARY KEY BIGINT UNSIGNED
matchId KEY BIGINT UNSIGNED
participantId KEY TINYINT UNSIGNED
summonerId KEY BIGINT UNSIGNED
championId INT UNSIGNED
highestAchievedSeasonTier VARCHAR(24)
spell1Id TINYINT UNSIGNED
spell2Id TINYINT UNSIGNED
teamId TINYINT UNSIGNED
assists INT UNSIGNED
champLevel TINYINT UNSIGNED
deaths INT UNSIGNED
doubleKills INT UNSIGNED
firstBloodAssist BIT(1)
firstBloodKill BIT(1)
firstInhibitorAssist BIT(1)
firstInhibitorKill BIT(1)
firstTowerAssist BIT(1)
firstTowerKill BIT(1)
goldEarned INT UNSIGNED
goldSpent INT UNSIGNED
inhibitorKills INT UNSIGNED
item0 INT UNSIGNED
item1 INT UNSIGNED
item2 INT UNSIGNED
item3 INT UNSIGNED
item4 INT UNSIGNED
item5 INT UNSIGNED
item6 INT UNSIGNED
killingSprees INT UNSIGNED
kills INT UNSIGNED
largestCriticalStrike INT UNSIGNED
largestKillingSpree INT UNSIGNED
largestMultiKill INT UNSIGNED
magicDamageDealt INT UNSIGNED
magicDamageDealtToChampions INT UNSIGNED
magicDamageTaken INT UNSIGNED
minionsKilled INT UNSIGNED
pentaKills INT UNSIGNED
physicalDamageDealt INT UNSIGNED
physicalDamageDealtToChampions INT UNSIGNED
physicalDamageTaken INT UNSIGNED
quadraKills INT UNSIGNED
totalDamageDealt INT UNSIGNED
totalDamageDealtToChampions INT UNSIGNED
totalDamageTaken INT UNSIGNED
totalHeal INT UNSIGNED
totalTimeCrowdControlDealt INT UNSIGNED
totalUnitsHealed INT UNSIGNED
towerKills TINYINT UNSIGNED
tripleKills INT UNSIGNED
trueDamageDealt INT UNSIGNED
trueDamageDealtToChampions INT UNSIGNED
trueDamageTaken INT UNSIGNED
unrealKills INT UNSIGNED
winner TINYINT UNSIGNED

Summoners
summonerId PRIMARY KEY BIGINT UNSIGNED
name VARCHAR(256)
lastQueried BIGINT UNSIGNED
profileIconId INT UNSIGNED
summonerLevel TINYINT UNSIGNED

Champions
championId PRIMARY KEY TINYINT UNSIGNED
name KEY VARCHAR(64) key
t..

Items
.


