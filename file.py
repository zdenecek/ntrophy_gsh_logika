import csv


def openCSV(folder, filename):

    path = folder + filename
    data = []

    with open(path, 'r') as file:
        spamreader = csv.reader(file, quoting=csv.QUOTE_NONNUMERIC, delimiter=',')
        for row in spamreader:
            row.pop()
            data.append(row)
    return data


def isBinary(layerData):
    for row in layerData:
        for cell in row:
            if cell > 1:
                return False
    return True


def isEmpty(layerData):
    for row in layerData:
        for cell in row:
            if cell != 0:
                return False
    return True


def printData(data):
    for row in data:
        tx = ""
        for cell in row:
            tx += str(cell) + ", "
