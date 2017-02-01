# recursive function for reading nested dictionary objects via an array
# eg with d = {'a':{'b':1}}, d['a']['b'] can be read with rDBA(d,[a,b])
def readDictByArray(d,a):
    if len(a) == 0:
        return None
    if len(a) == 1:
        return d[a[0]]
    return readDictByArray(d[a[0]], a[1:])

dataMap = {
    'MatchDetails':
    {
        'matchId':
        {
            'type':'PRIMARY KEY BIGINT UNSIGNED',
            'game-v1.3':(readDictByArray,["gameId"]),
            'match-v2.2':(readDictByArray,["matchId"])
        },'

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
        ',

        'winner':
        {
            'type':'TINYINT UNSIGNED',
            'type':'PRIMARY KEY BIGINT UNSIGNED',
            'game-v1.3':(lambda d,a:),
            'match-v2.2':(firstField,["matchId"])

        }
    },
'test':
'
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
'
}
