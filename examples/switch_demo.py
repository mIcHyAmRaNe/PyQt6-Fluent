from PyQt6.QtWidgets import QApplication, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt

from pyqt_fluent import Switch, ThemeManager


app = QApplication([])
w = QWidget()
w.setWindowTitle("Switch Demo")
w.resize(300, 200)

layout = QVBoxLayout(w)
layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

layout.addWidget(QLabel("Toggle switch:"))
switch = Switch()
layout.addWidget(switch)

layout.addWidget(QLabel("Another one:"))
switch2 = Switch()
switch2.setChecked(True)
layout.addWidget(switch2)

ThemeManager.instance().register_observer(w)
w.show()
app.exec()
