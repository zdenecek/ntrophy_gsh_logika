from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QColor
import colors as c


def getLayer(data, colors, name, type, opacity):
    if type in [0, 4]:
        return NonBinLayer(data, colors, name, type, opacity)
    elif type == 5:
        return CustomLayer(data, colors, name, type, opacity)
    else:
        return BinLayer(data, colors, name, type, opacity)


class MapLayer:
    typeNames = {
        0: "non binary",
        1: "area",
        2: "line",
        3: "point",
        4: 'point binary',
        5: "custom"
        }

    def getName(self):
        return self.name

    def __init__(self, color, name, type, opacity):
        self.color = QColor(color)
        self.name = name
        self.type = type
        self.opacity = opacity
        self.hidden = True


class CustomLayer(MapLayer):

    def __init__(self, data, color, name, type, opacity):
        super().__init__(color, name, type, opacity)
        self.isBinary = True
        self.calculatePaintData(data)

    def calculatePaintData(self, data):
        dat = {}
        dat["color"] = self.color
        dat["points"] = []

        for p in data:
            print(f"appending [{p[0]}, {p[1]}]")
            dat["points"].append(QPoint(p[0], p[1]))

        self.paintData = [dat]


class BinLayer(MapLayer):

    def __init__(self, data, color, name, type, opacity):
        super().__init__(color, name, type, opacity)
        self.isBinary = True
        self.calculatePaintData(data)

    def calculatePaintData(self, data):
        columns = range(len(data[0]))

        dat = {}
        dat["color"] = self.color
        dat["points"] = []

        for row in range(len(data)):
            for col in columns:
                if data[row][col] > 0:
                    dat["points"].append(QPoint(col, row))

        self.paintData = [dat]


class NonBinLayer(MapLayer):
    def __init__(self, data, colors, name, type, opacity):
        super().__init__(colors[0], name, type, opacity)
        self.color2 = QColor(colors[1])
        self.color1 = self.color
        self.isBinary = False
        self.calculatePaintData(data)

    def calculatePaintData(self, data):
        columns = range(len(data[0]))

        min = max = None
        points = []

        for row in range(len(data)):
            for col in columns:
                value = data[row][col]
                if value != 0:
                    points.append({"value": value, "point": QPoint(col, row)})
                    if min:
                        if value < min:
                            min = value
                        elif value > max:
                            max = value
                    else:
                        min = value
                        max = value

        self.maximum = max
        self.minimum = min

        drawData = {}
        for point in points:
            if point["value"] not in drawData:
                drawData[point["value"]] = []
            drawData[point["value"]].append(point["point"])

        colors = c.getRange(self.color1, self.color2, int(max - min + 1))

        self.paintData = []
        for value in drawData:
            data = {}
            data["color"] = colors[int(value - min)]
            data["points"] = drawData[value]
            self.paintData.append(data)
