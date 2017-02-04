# endpoints
GAME = 'game-v1.3'
MATCH = 'match-v2.2'

class FuncSig:
    def __init__(self, f, kwargs):
        self.function = f
        self.kwargs = kwargs

# recursive function for reading nested dictionary objects via an array
# eg with d = {'a':{'b':1}}, d['a']['b'] can be read with rDBA(d,[a,b])
def readDictByArray(d, a):
    if len(a) == 0:
        return None
    if len(a) == 1:
        return d[a[0]]
    return readDictByArray(d[a[0]], a[1:])


def getWinner(d, endpoint):
    if endpoint == GAME:
        won = d['stats']['win']
        team = d['stats']['team']/100
    elif endpoint == MATCH:
        won = d['participants'][0]['stats']['winner']
        team = d['participants'][0]['teamId']/100
    else:
        return None
    # return the appropriate team id based on whether participant  won/lost
    if won:
        return team
    else:
        return 1 if team == 2 else 2
