import logging
import json
from flask import request, jsonify
from codeitsuisse import app
from collections import deque
logger = logging.getLogger(__name__)
@app.route('/stock-hunter', methods=['POST'])
def evaluateStock():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    result = []
    for testcase in data:
        result.append(implement(testcase["entryPoint"]["first"],testcase["entryPoint"]["second"],testcase["targetPoint"]["first"],testcase["targetPoint"]["second"],testcase["gridDepth"],testcase["gridKey"],testcase["horizontalStepper"],testcase["verticalStepper"]))
    
    logging.info("My result :{}".format(result))
    return json.dumps(result)

def implement(sx,sy,ex,ey,a,b,c,d):
    w, h = max(sy,ey) + 3, max(sx,ex) + 3
    cost = [[0 for x in range(w)] for y in range(h)] 
    for i in range(h):
        for j in range(w):
            if (i == 0 and j == 0):
                cost[i][j] = a % b
                #cost[i][j] = (cost[i][j]) % 3
            elif (i == 0):
                cost[i][j] = (j * c + a) % b
                #cost[i][j] = (cost[i][j]) % 3
            elif (j == 0):
                cost[i][j] = (i * d + a) % b
                #cost[i][j] = (cost[i][j]) % 3
            else:
                cost[i][j] = (cost[i-1][j] * cost[i][j-1] + a) % b
            #cost[i][j] = 3 - cost[i][j]  
            #       
    for i in range(h):
        for j in range(w):
            cost[i][j] = (cost[i][j]) % 3
            cost[i][j] = 3 - cost[i][j]                           
    
    n = abs(sx-ex) + 1
    m = abs(sy-ey) + 1
    print(n,m)
    output = [["" for x in range(m)] for y in range(n)]    

    key = 0
    for i in range(h):
        for j in range(w):
            if (i == min(sx,ex) and j == min(sy,ey)):
                for ii in range(n):
                    for jj in range(m):
                        output[ii][jj] = chn(cost[i+ii][j+jj])
                key = 1
            if (key == 1):
                break
        if (key == 1):
            break

    answer = {}
    answer["gridMap"] = output
    answer["minimumCost"] = 0
    return answer

def chn(x):
    if (x == 3):
        return "L"
    elif (x == 2):
        return "M"
    elif (x == 1):
        return "S"
