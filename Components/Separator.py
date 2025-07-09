from PyQt5.QtWidgets import QFrame,QWidget,QLabel,QHBoxLayout
from PyQt5.QtCore import Qt
import Styles.colors as cl

class SeparatorLine(QFrame):
    def __init__(self, color=f"{cl.SYS_SEP1}", orientation="H", length=-1, thickness=1, parent=None):
        super().__init__(parent)

        # Orientation: HLine or VLine
        if orientation.upper() == "H":
            self.setFrameShape(QFrame.HLine)
            self.setFixedHeight(thickness)
            if length != -1:
                self.setFixedWidth(length)
        elif orientation.upper() == "V":
            self.setFrameShape(QFrame.VLine)
            self.setFixedWidth(thickness)
            if length != -1:
                self.setFixedHeight(length)
        else:
            raise ValueError("Orientation must be 'H' or 'V'")

        self.setFrameShadow(QFrame.Plain)
        self.setStyleSheet(f"background-color: {color}; border: none;")

class LabeledHorizontalLine(QWidget):
    def __init__(self,label="",color=None,font_size=10,thickness = 1):
        super().__init__()
        if color is None:
            color = cl.SYS_SEP1
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        l1 = SeparatorLine(color=color,thickness=thickness)
        l2 = SeparatorLine(color=color,thickness=thickness)

        text = QLabel(label)
        text.setStyleSheet(f"color:{color};font-size:{font_size}px")

        layout.addWidget(l1,1,Qt.AlignVCenter)
        layout.addSpacing(5)
        layout.addWidget(text,0,Qt.AlignVCenter)
        layout.addSpacing(5)
        layout.addWidget(l2,1,Qt.AlignVCenter)

        self.setLayout(layout)
    
 

