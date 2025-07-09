#Qt Imports
from PyQt5.QtWidgets import (
    QWidget ,QVBoxLayout, QLabel
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

#Styles Import
import Styles.styles as styles
import Styles.colors as cl


class Logo(QWidget):
    def __init__(self):
        super().__init__()

        self.setup_ui()
    
    def setup_ui(self):
        header_layout = QVBoxLayout()
        header_layout.setContentsMargins(0,0,0,0)
        header_layout.setSpacing(0)

        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("assets/sppl-logo-white.png"))
        self.logo.setFixedSize(50, 50)
        self.logo.setStyleSheet("margin:5px")
        self.logo.setScaledContents(True)

        self.logoLabel1 = QLabel("SPPL India")
        self.logoLabel1.setStyleSheet(styles.text_style2+"QLabel{font-weight:600;font-size:10px}")

        self.logoLabel2 = QLabel("IIT Delhi")
        self.logoLabel2.setStyleSheet(styles.text_style2+f"QLabel{{font-weight:400;font-size:9px;color:{cl.SYS_FG3}}}")

        header_layout.addWidget(self.logo,0,Qt.AlignHCenter)
        header_layout.addWidget(self.logoLabel1,0,Qt.AlignHCenter)
        header_layout.addWidget(self.logoLabel2,0,Qt.AlignHCenter)
    
        self.setLayout(header_layout)