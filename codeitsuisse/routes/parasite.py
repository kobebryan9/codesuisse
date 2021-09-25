import logging
import json

from flask import request, jsonify

from codeitsuisse import app
from collections import deque

logger = logging.getLogger(__name__)

@app.route('/parasite', methods=['POST'])
def evaluateParasite():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    result = []
    for testcase in data:
        result.append(implement(testcase["room"],testcase["grid"],testcase["interestedIndividuals"]))
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def implement(room, grid, ind):
    dx = [0, 0, 1, -1, 1, 1, -1, -1]
    dy = [1, -1, 0 , 0, -1, 1, -1, 1]

    n = len(grid)
    m = len(grid[0])    
    big = n*m + 1
    grid1 = b = [x[:] for x in grid]
    grid2 = b = [x[:] for x in grid]    

    stx = 0
    sty = 0

    for i in range(n):
        for j in range(m):
            grid1[i][j] = big
            print(i,j,grid1[i][j],grid[i][j])
            if (grid[i][j] == 3):
                stx = i
                sty = j

    print(stx,sty)
    q = deque()
    q.append([stx,sty])
    a = 0
    grid1[stx][sty] = 0
    while (len(q) > 0):
        g = q.popleft()
        xx = g[0]
        yy = g[1]
        print(xx,yy)
        for i in range(4):
            tmx = xx + dx[i]
            tmy = yy + dy[i]
            if check(tmx,tmy,n,m) == 1:
                print("testing", tmx,tmy,grid1[tmx][tmy],grid1[xx][yy],grid[tmx][tmy] )
                if grid1[tmx][tmy] > grid1[xx][yy] + 1 and (grid[tmx][tmy] == 1):
                    grid1[tmx][tmy] = grid1[xx][yy] + 1
                    q.append([tmx,tmy])

    answer = {}
    answer["room"] = room
    answer["p1"] = {}
    answer["p2"] = 0
    answer["p3"] = 0
    answer["p4"] = 0

    for x in ind:
        nn = len(x)
        xx = 0
        yy = 0
        for i in range(nn):
            if (x[i] == ","):
                xx = int(x[0:i])
                yy = int(x[i+1:nn])

        if (grid1[xx][yy] != big and grid[xx][yy] != 3 and grid[xx][yy] != 2):
            answer["p1"][x] = grid1[xx][yy]
        else:
            answer["p1"][x] = -1
        #print(xx,yy)

    ans = 0
    for i in range(n):
        for j in range(m):
            if (grid[i][j] == 1):
                if (grid1[i][j] == big):
                    ans = big
                else:
                    ans = max(ans, grid1[i][j])

    if (ans == big):
        ans = -1
    answer["p2"] = ans   

    for i in range(n):
        for j in range(m):
            grid1[i][j] = big

    q = deque()
    q.append([stx,sty])
    a = 0
    grid1[stx][sty] = 0
    while (len(q) > 0):
        g = q.popleft()
        xx = g[0]
        yy = g[1]
        print(xx,yy)
        for i in range(8):
            tmx = xx + dx[i]
            tmy = yy + dy[i]
            if check(tmx,tmy,n,m) == 1:
                print("testing", tmx,tmy,grid1[tmx][tmy],grid1[xx][yy],grid[tmx][tmy] )
                if grid1[tmx][tmy] > grid1[xx][yy] + 1 and (grid[tmx][tmy] == 1):
                    grid1[tmx][tmy] = grid1[xx][yy] + 1
                    q.append([tmx,tmy])   

    ans = 0
    for i in range(n):
        for j in range(m):
            if (grid[i][j] == 1):
                if (grid1[i][j] == big):
                    ans = big
                else:
                    ans = max(ans, grid1[i][j])   
    
    if (ans == big):
        ans = -1
    answer["p3"] = ans       

    
    for i in range(n):
        for j in range(m):
            grid1[i][j] = -1
            if (grid[i][j] == 2):
                grid[i][j] = 0

    tot = 0

    for i in range(n):
        for j in range(m):
            if (grid[i][j] != 0):
                if (grid1[i][j] == -1):
                        q = deque()
                        q.append([i,j])
                        grid1[i][j] = tot
                        tot = tot + 1
                        while (len(q) > 0):
                            g = q.popleft()
                            xx = g[0]
                            yy = g[1]
                            for ii in range(4):
                                tmx = xx + dx[ii]
                                tmy = yy + dy[ii]
                                if check(tmx,tmy,n,m) == 1:
                                    print("testing", tmx,tmy,grid1[tmx][tmy],grid1[xx][yy],grid[tmx][tmy] )
                                    if grid1[tmx][tmy] != grid1[xx][yy] and (grid[tmx][tmy] != 0):
                                        grid1[tmx][tmy] = grid1[xx][yy]
                                        q.append([tmx,tmy])

    w, h = tot, tot
    cost = [[0 for x in range(w)] for y in range(h)] 
    for i in range(tot):
        for j in range(tot):
            cost[i][j] = big

    for i in range(n):
        for j in range(m):
            team = grid1[i][j]
            if (team == -1):
                continue
            if (cost[team][team] == big):
                print("team",i,j,team)
                cost[team][team] = 0
                q = deque()                
                for ii in range(n):
                    for jj in range(m):
                        grid2[ii][jj] = big
                        if (grid1[ii][jj] == team):
                            grid2[ii][jj] = 0
                            q.append([ii,jj])

                while (len(q) > 0):
                    g = q.popleft()
                    xx = g[0]
                    yy = g[1]
                    for ii in range(4):
                        tmx = xx + dx[ii]
                        tmy = yy + dy[ii]
                        if check(tmx,tmy,n,m) == 1:
                            #print("testing", tmx,tmy,grid2[tmx][tmy],grid1[xx][yy],grid[tmx][tmy] )
                            if grid2[tmx][tmy] > grid2[xx][yy] + 1 and (grid[tmx][tmy] == 0):
                                grid2[tmx][tmy] = grid2[xx][yy] + 1
                                q.append([tmx,tmy])
                            if grid2[tmx][tmy] > grid2[xx][yy] and (grid[tmx][tmy] != 0):
                                grid2[tmx][tmy] = grid2[xx][yy]
                                q.append([tmx,tmy])                            

                for ii in range(n):
                    for jj in range(m):
                        cost[team][grid1[ii][jj]] = min(cost[team][grid1[ii][jj]],grid2[ii][jj])


    dist = [0 for x in range(tot)]
    cur = [0 for x in range(tot)]
    for x in range(tot):
        dist[x] = cost[0][x]
        cur[x] = 0

    cur[0] = 1
    ans = 0

    for i in range(tot-1):
        mim = big
        id = 0
        for j in range(tot):
            if (id == 0) and j != 0 and dist[j] < mim and cur[j] == 0:
                mim = dist[j]
                id = j

        cur[id] = 1
        ans += mim
        for j in range(tot):
            if cur[j] == 0:
                dist[j] = min(dist[j],cost[id][j])

    answer["p4"] = ans
    return answer

def check(x, y, n, m):
    if x < 0 or x >= n or y < 0 or y >= m:
        return 0
    else:
        return 1

