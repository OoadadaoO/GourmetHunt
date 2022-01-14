import csv

def filenameEncode(name):
    uniName = str(name.encode('unicode_escape'))
    uniName = uniName.replace("'", '')
    uniName = uniName.replace('\\', '')
    return uniName

def restaurantSet(user):
    restaurants = set()
    uniUser = filenameEncode(user)
    with open (f'./favorite/csv/{uniUser}.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            if row != []:
                temp = eval(row[0])
                restaurants.add(temp[0][0])
    return restaurants

def storage(user, restaurant, label):
    uniUser = filenameEncode(user)
    with open (f'./favorite/csv/{uniUser}.csv','a') as csvfile:
        writer = csv.writer(csvfile)
        if label.isspace():
            labelList = label.split(', ')
        else:
            labelList = label.split(',')
        table = [[
            [restaurant, labelList]
        ]]
        writer.writerow(table)

def tidy(user = 'visitor'):
    uniUser = filenameEncode(user)
    with open (f'./favorite/csv/{uniUser}.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        kinds = set()
        for row in reader:
            if row != []:
                temp = eval(row[0])
                kindsList = temp[0][1]
                for i in kindsList:
                    kinds.add(i)
        kindsAll = list(kinds)
        kindsAll.insert(0, '全部')
        return kindsAll

def resShow(user, choose):
    uniUser = filenameEncode(user)
    with open (f'./favorite/csv/{uniUser}.csv','r') as csvfile:
        reader = csv.reader(csvfile)
        originList = []
        newList = []
        for row in reader:
            if row != []:
                temp = eval(row[0])
                originList.append(temp[0])
        restaurantAll = restaurantSet(user)
        for i in restaurantAll:
            kindsSet = set()
            for j in originList:
                if i == j[0]:
                    for k in j[1]:
                        kindsSet.add(k)
            newList.append([i, list(kindsSet)])
        if choose == '全部':
            return newList
        restaurants = []
        for i in range(len(newList)):
            if choose in newList[i][1]:
                restaurants.append(newList[i])
        return restaurants