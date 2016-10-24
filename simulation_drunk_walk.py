import random, math, pylab
def drunkerwalk(point, start, foot):
    n = 0
    now = start
    dist = 1
    distance = []
    distance.append(getdistance(point, start))
    time = [0]
    time1 = []
    while n != foot:
        n += 1
        now = walk(now, dist)
        distance.append(getdistance(point,now))
        time.append(n)
    for i in time:
        time1.append(i*10)
    return distance    

def walk(now, dist):
    footdistance = {'East':(dist,0), 'South':(0,-dist), 'West':(-dist,0), 'North':(0,dist)}
    direction = random.choice(['East', 'South', 'West', 'North'])
    now = (now[0] + footdistance[direction][0], now[1] + footdistance[direction][1])
    return now

def getdistance(point,now):
    return math.sqrt((now[0] - point[0])**2 + (now[1] - point[1])**2)


def average(maxTime, numTrials):
    averagenum = [0] * (numTrials + 1)
    for i in range(maxTime):
        print(i)
        distance = drunkerwalk((0,0), (0,0), numTrials)
        for j in range(len(distance)):
            averagenum[j] += (distance[j] / maxTime)
    pylab.plot(averagenum)
    pylab.xlabel('foot')
    pylab.ylabel('average distance from point')
    pylab.title('average drunker walk test %d time every time walk %d'%(maxTime, numTrials))
    pylab.grid(True)
    pylab.savefig("test3.png")
    pylab.show()
    
average(100,10000)
