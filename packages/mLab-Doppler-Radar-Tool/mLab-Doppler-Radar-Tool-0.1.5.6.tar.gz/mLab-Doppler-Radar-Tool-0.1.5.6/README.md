##mLab Doppler Radar Tool: UART serial & data plot

[![Latest PyPI version](https://img.shields.io/badge/pypi-v0.1-green.svg)](https://pypi.org/project/qt-ledwidget/)
[![License: MIT](https://img.shields.io/dub/l/vibe-d.svg)](https://opensource.org/licenses/MIT)

*before you install mLab Doppler Radar Tool,
please check if you already install PyQt5 or not.*

for **Raspberry Pi**,please install PyQt5 as following.
In Raspbian Stretch Lite the following worked for:
```
$sudo apt-get update
$sudo apt-get install qt5-default pyqt5-dev pyqt5-dev-tools
``` 

for **Ubuntu** user, in linux terminal:
```
$sudo python3 -m pip install PyQt5
```
for **windows** user, in CMD terminal:
```
python -m pip install PyQt5
```

then copy, run our example code:
```
form mLab_DopplerRadar import MainWindow
from PyQt5 import QtCore, QtWidgets, QtGui
import sys

if __name__ == "__main__":
    print("system start)
    app = QtWidgets.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
```

like:
```
sudo python3 <your file location/name>
```