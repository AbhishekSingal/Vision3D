from PyQt5.QtWidgets import QWidget , QVBoxLayout , QLabel 
from PyQt5.QtCore import pyqtSignal , Qt
from PyQt5.QtGui import QCursor , QPixmap,QIcon

import Styles.colors as cl

class VerticalIconTextButton(QWidget):
    clicked = pyqtSignal()

    def __init__(self, icon_path, text, parent=None,size = 30,hover_bg = cl.SYS_BG3,font_size=12,width=80,height=60):
        super().__init__(parent)
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setCursor(QCursor(Qt.PointingHandCursor))

        layout = QVBoxLayout(self)
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(4)

        self.size = size

        # Icon
        # self.icon_label = QLabel()
        # pixmap = QPixmap(icon_path).scaled(30, 30, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        # self.icon_label.setPixmap(pixmap)
        # self.icon_label.setAlignment(Qt.AlignCenter)

        self.icon_label = QLabel()
        icon = QIcon(icon_path)
        pixmap = icon.pixmap(size, size)  # uses system-aware scaling
        self.icon_label.setPixmap(pixmap)
        self.icon_label.setAlignment(Qt.AlignCenter)

        # Text
        self.text_label = QLabel(text)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet(f"""
            color: {cl.SYS_FG1};
            font-size: {font_size}px;
            font-weight: 500;
        """)

        # Add to layout
        layout.addWidget(self.icon_label,1)
        layout.addWidget(self.text_label,0)

        # Base style
        self.setStyleSheet(f"""
            QWidget {{
                background-color: transparent;
                border: none;
                margin-top:5px;
            }}
            QWidget:hover {{
                background-color: {hover_bg}
            }}
        """)

        self.setFixedSize(width, height)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.clicked.emit()

    def updateIconText(self, icon_path, text):
        icon = QIcon(icon_path)
        pixmap = icon.pixmap(self.size)  # preserve current icon size
        self.icon_label.setPixmap(pixmap)
        self.text_label.setText(text)