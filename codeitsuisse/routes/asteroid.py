import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/asteroid', methods=['POST'])
def evaluateAsteroid():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    result = []
    for test_cases in data:
        for testcase in test_cases:
            result.append(implement(testcase))

    logging.info("My result :{}".format(result))
    return json.dumps(result)

def calculate(count):
    if (count <= 6) return count
    elif (count >= 10) return 2 * count
    else return 1.5 * count

def implement(s):
    answer = {}
    answer["input"] = s
    len = s.length()
    origin = 0
    score = 0
    for i in range(len):
        tmpscore = 0
        p1 = i - 1
        p2 = i + 1
        last = s[i]
        if (p1 < 0 or p2 == len):
            tmpscore = 1
        elif (s[p1] != s[p2]):
            tmpscore = 1
        else:
            count = 0
            while (p1 - 1 >= 0 and s[p1 - 1] == s[p1]):
                count += 1
                p1 -= 1
            while (p2 + 1 < len and s[p2 + 1] == s[p2]):
                count += 1
                p2 += 1
            if (s[p1] == s[i]):
                count += 1
                tmpscore += calculate(count)
            else:
                tmpscore += calculate(count) + 1
            p1 -= 1
            p2 += 1
            while (p1 >= 0 and p2 < len):
                count = 0
                if (s[p1] != s[p2]):
                    break
                while (p1 - 1 >= 0 and s[p1 - 1] == s[p1]):
                    count += 1
                    p1 -= 1
                while (p2 + 1 < len and s[p2 + 1] == s[p2]):
                    count += 1
                    p2 += 1
                tmpscore += calculate(count)
        if (tmpscore > score):
            score = tmpscore
            origin = i
    answer["score"] = score
    answer["origin"] = origin
    return answer