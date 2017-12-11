from PatternStore import addPattern

def formDictionary(curs, dictFixed, fixed, variable):
    for row in curs:

        agg = row[0]  # ALWAYS the 0th index value

        f = ""
        if len(fixed) > 1:
            i = 1
            while i <= len(fixed):
                f = f + ":" + str(row[i])
                i = i + 1
        else:
            f = row[1]

        v = ""
        if len(variable) > 1:
            i = len(fixed) + 1
            while i <= len(fixed) + len(variable):
                v = v + ":" + str(row[i])
                i = i + 1
        else:
            v = row[len(fixed) + 1]

        if f not in dictFixed:
            dictFixed[f] = {}

        dictFixed[f][v] = float(agg)

        # print(dictFixed)


def formDictionary2(curs, dictFixed):
    for row in curs:
        fixed = row[0]
        agg = row[1]

        if fixed not in dictFixed:
            dictFixed[fixed] = {}

        dictFixed[fixed] = float(agg)


def formQuery(fixed, variable, value, tableName):
    vStr = ','.join(map(str, variable))
    fStr = ','.join(map(str, fixed))

    query = "SELECT stddev_pop(" + value + ")/ avg(" + value + ")," + fStr + ", " + vStr + "  FROM " + tableName + \
            " where ticker in ('AAPL') GROUP BY " + fStr + ", " + vStr + " ORDER BY " + vStr

    # print('Query::', query)

    return query


def formQuery2(fixed, value, tableName):
    query = "SELECT " + fixed + ", stddev_pop(" + value + ")/ avg(" + value + ") FROM " + tableName + " where ticker in ('AAPL')" + \
            " GROUP BY " + fixed + " ORDER BY " + fixed
    return query


def findConstants(dictFixed, fixed, variable, value):
    Cat_falseCount = 0
    Cat_trueCount = 0

    for fixedVar, plotData in dictFixed.items():
        trueCount = 0
        falseCount = 0
        for key in plotData:

            if plotData[key] < .15 and plotData[key] != 0:
                trueCount = trueCount + 1
                # addPattern(fixed, fixedVar, variable, plotData[key], 'stddev', value, 'constant', plotData[key] )
                addPattern(fixed, fixedVar, variable, 'stddev1', value,
                           'constant', plotData[key])

            else:
                falseCount = falseCount + 1

        if falseCount == 0 or (trueCount / (falseCount + trueCount) > 0.75):

            Cat_trueCount = Cat_trueCount + 1
            # addPattern(fixed, fixedVar, variable, None, 'stddev', value, 'constant', trueCount * 100 /(falseCount+trueCount)  )
            addPattern(fixed, fixedVar, variable, 'stddev1', value, 'constant',
                       trueCount * 100 / (falseCount + trueCount))

        else:
            Cat_falseCount = Cat_falseCount + 1

    if Cat_falseCount == 0 or (
            Cat_trueCount / (Cat_trueCount + Cat_falseCount) > 0.75):
        # addPattern(fixed, None, variable, None, 'stddev', value, "constant", (Cat_trueCount * 100 / (Cat_trueCount+Cat_falseCount)))
        addPattern(fixed, None, variable, 'stddev1', value, 'constant',
                   (Cat_trueCount * 100 / (Cat_trueCount + Cat_falseCount)))


def findConstants2(dictFixed, fixed, value):
    Cat_falseCount = 0
    Cat_trueCount = 0

    for fixedVar, stddeviation in dictFixed.items():

        if (stddeviation < 0.15):
            Cat_trueCount = Cat_trueCount + 1
            # addPattern(fixed, fixedVar, None, None, 'stddev', value, 'constant', stddeviation )
            addPattern(fixed, fixedVar, None, 'stddev', value, 'constant',
                       stddeviation)

        else:
            Cat_falseCount = Cat_falseCount + 1

    if Cat_falseCount == 0 or (
            Cat_trueCount / (Cat_falseCount + Cat_trueCount) > 0.75):
        # addPattern(fixed, None, None, None, 'stddev', value, "constant", (Cat_trueCount * 100 / (Cat_trueCount+Cat_falseCount)))
        addPattern(fixed, None, None, 'stddev', value, 'constant',
                   (Cat_trueCount * 100 / (Cat_trueCount + Cat_falseCount)))
