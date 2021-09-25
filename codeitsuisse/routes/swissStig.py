import logging
import json

from flask import request, jsonify

from codeitsuisse import app

logger = logging.getLogger(__name__)

@app.route('/swissStig', methods=['POST'])
def evaluateswissStig():
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))

    result = []
    for testcase in data:
        result.append(implement(testcase["questions"], testcase["coefficients"], testcase["maxRating"]))

    logging.info("My result :{}".format(result))
    return json.dumps(result)

def implement(questions, coefficients, maxRating):
    Q = len(questions)
    mx = []
    mn = []
    correct = 0
    for i in range(Q + 1):
        mx.append(-1)
        mn.append(1e9)
    for i in reversed(range(Q)):
        mn[i] = min(mn[i + 1], questions[i]["from"])
        mx[i] = max(mx[i + 1], questions[i]["to"])
    for i in range(Q - 1):
        if (mn[i + 1] >= questions[i]["from"] and mx[i + 1] <= questions[i]["to"]):
            questions[i]["here"] = 1
            correct += 1
        else:
            questions[i]["here"] = 0
    total = 0
    if (correct == 0):
        questions.sort()
        total = 0
        last = 0
        for (i in range(Q - 1)):
            if (questions[i]["from"] > last):
                total += questions[i]["from"] - last - 1
                last = questions[i]["to"]
            else:
                last = max(last, questions[i]["to"])
        total += maxRating - last
    else:
        pl = 0
        last = 0
        end = 0
        for i in range(Q - 1):
            if (questions[i]["here"] == 1):
                pl = i
                last = questions[i]["from"] - 1
                end = questions[i]["to"]
                break
        remain = []
        for i in range(i + 1, Q - 1):
            remain.append(questions[i])
        remain.sort()
        for q in remain:
            if (q["from"] > last):
                total += q["from"] - last - 1
                last = q["to"]
            else:
                last = max(last, q["to"])
        total += end - last
    result = []
    result["p"] = 1
    result["q"] = total
    return result
