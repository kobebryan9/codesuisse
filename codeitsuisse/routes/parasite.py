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
                if grid1[tmx][tmy] > grid1[xx][yy] + 1 and (grid[tmx][tmy] == 1 or grid[tmx][tmy] == 2):
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



    return answer

def check(x, y, n, m):
    if x < 0 or x >= n or y < 0 or y >= m:
        return 0
    else:
        return 1

