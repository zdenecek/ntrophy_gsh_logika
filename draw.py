from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QFont
from PyQt5.QtCore import Qt, QRectF


class Map(QWidget):

    def __init__(self, scale, dim):
        super().__init__()

        self.scale = scale
        self.dim = dim * self.scale

        self.pointMagnification = 3

        self.setGeometry(100, 40, self.dim + 300, self.dim+200)
        self.setWindowTitle('Map')
        self.layers = []

        # self.mouseReleaseEvent = self.clicked

        self.autoFillBackground = False

    def mousePressEvent(self, event):
        print(f"[{event.x()},{event.y()}]")
        if event.x() < self.labelMaxX and event.x() > self.labelMinX:
            y = event.y()
            for layer in self.layers:
                if y < layer.labelMaxY and y > layer.labelMinY:
                    print("hiding layer " + layer.getName() + f" hidden={not layer.hidden}")
                    layer.hidden = not layer.hidden
                    self.repaint()

    def addLayer(self, layer):
        self.layers.append(layer)
        self.layers.sort(key=lambda x: x.type, reverse=False)
        s = self.scale

        # values for point layers
        ofset = self.pointMagnification
        pd = 2*ofset + s  # point dimension
        #
        layer.rectangles = []

        for data in layer.paintData:
            points = data["points"]
            rectangles = []
            for point in points:
                if layer.type in [3, 4, 5]:
                    rectangles.append(QRectF(point.x()*s - ofset, point.y()*s - ofset, pd, pd))
                else:
                    rectangles.append(QRectF(point.x()*s, point.y()*s, s, s))
            layer.rectangles.append({"color": data["color"], "rectangles": rectangles})

    def paintEvent(self, e):
        self.draw()
        pass

    def draw(self):
        print("draw called, layer count " + str(len(self.layers)))
        painter = QPainter()
        painter.begin(self)

        for layer in self.layers:
            print(f"drawing layer {layer.getName()}, is binary {layer.isBinary}")
            self.drawLayer(painter, layer)

        self.drawLabels(painter)
        painter.end()

    def drawLabels(self, painter):
        fontsize = 8
        y = 3 + fontsize
        height = fontsize + 2

        self.labelMinX = x = self.dim + self.scale + 5
        self.labelMaxX = x + height

        offset = (height - fontsize)/2
        rect = height - 2*offset

        painter.setPen(Qt.darkGray)
        font = QFont("Helvetica", fontsize, 1, False)
        painter.setFont(font)

        for i in range(len(self.layers)):
            self.layers[i].labelMinY = y + offset
            self.layers[i].labelMaxY = y + offset + rect
            painter.setBrush(self.layers[i].color)
            font.setStrikeOut(self.layers[i].hidden)
            font.setBold(not self.layers[i].hidden)
            painter.setFont(font)
            painter.drawRect(x, y + offset, rect, rect)
            painter.drawText(x + height, y + height - offset, self.layers[i].getName())
            y += height

    def drawLayer(self, painter, layer):

        if layer.hidden:
            return

        def setPainter(painter, layerType, color, opacity):
            color.setAlpha(opacity)
            if layer.type == 3:
                painter.setBrush(color)
                painter.setPen(Qt.transparent)

            elif layer.type == 2:
                painter.setBrush(Qt.transparent)
                painter.setPen(color)
            else:
                # painter.setCompositionMode(QPainter.CompositionMode_Overlay)
                if layer.type == 1:
                    pass
                    # color.setAlpha(180)
                painter.setBrush(color)
                painter.setPen(Qt.transparent)

        for data in layer.rectangles:
            setPainter(painter, layer.type, data["color"], layer.opacity)
            painter.drawRects(data["rectangles"])
