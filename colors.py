from PyQt5.Qt import QColor
from colour import Color


def getRange(color1, color2, steps):
    colors = list(Color(color1.name()).range_to(Color(color2.name()), steps))
    qColors = []
    for color in colors:
        qColors.append(QColor(color.hex))
    return qColors
