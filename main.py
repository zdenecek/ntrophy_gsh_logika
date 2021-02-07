from PyQt5.Qt import QApplication
import sys
import locale

# custom
import file as f
import draw as d
import mapClasses as c

# data
from layers import layers as files
from layersCustom import layers as customFiles

path = "c:\\Users\\zdnek\\ME\\ntrophy11\\log2\\csv2dot\\"

locale.setlocale(locale.LC_ALL, "")


def run():
    app = QApplication(sys.argv)
    map = d.Map(1, 800)

    for file in customFiles:
        print(f"adding custom {file[1]}")
        layer = c.getLayer(file[5], file[3], file[1], file[2], file[4])
        layer.group = file[0]
        map.addLayer(layer)

    for file in files:
        print(f"opening {file[1]}")
        data = f.openCSV(folder=path, filename=f"{file[1]}.csv")
        layer = c.getLayer(data, file[3], file[1], file[2], file[4])
        layer.group = file[0]
        map.addLayer(layer)

    map.show()
    sys.exit(app.exec_())


run()
