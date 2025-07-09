from PyQt5.QtWidgets import(QLabel ,QWidget , QHBoxLayout)

from PyQt5.QtGui import QPixmap,QIcon,QMovie
from PyQt5.QtCore import Qt,QSize

import Styles.styles as styles
import Styles.colors as cl

def GetIcon(path:str,size:float):
    icon_label = QLabel()
    icon_ = QIcon(path)
    pixmap = icon_.pixmap(size,size)
    # pixmap = QPixmap(path).scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    icon_label.setPixmap(pixmap)
    icon_label.setAlignment(Qt.AlignCenter)
    icon_label.setStyleSheet(f"QLabel{{border:none;outline:none}}QLabel:hover{{background-color:{cl.SYS_BD4}}}")
    icon_label.setCursor(Qt.PointingHandCursor)

    return icon_label

def GetIconLabel(label_widget:str,path:str,size,label_style = styles.text_style1):
    widget = QWidget()
    widget.setAttribute(Qt.WA_StyledBackground, True)
    layout = QHBoxLayout()

    layout.setContentsMargins(2,2,2,2)
    layout.setSpacing(2)

    label_widget = QLabel(label_widget)
    label_widget.setStyleSheet(label_style)

    icon_widget = GetIcon(path,size)

    layout.addWidget(icon_widget,0,Qt.AlignVCenter)
    layout.addWidget(label_widget,0,Qt.AlignVCenter)
    
    layout.addStretch(1)

    widget.setLayout(layout)

    widget.setStyleSheet("border:none;outline:none")

    return widget


def GetGIF(gif_path:str,size):
    spinner = QLabel()
    movie = QMovie(gif_path)
    movie.setScaledSize(QSize(size,size))  
    spinner.setMovie(movie)
    spinner.setAlignment(Qt.AlignCenter)
    movie.start()

    return spinner

def GetGIFLabel(label_widget:str,path:str,size,label_style = styles.text_style1):
    widget = QWidget()
    widget.setAttribute(Qt.WA_StyledBackground, True)
    layout = QHBoxLayout()

    layout.setContentsMargins(2,2,2,2)
    layout.setSpacing(2)

    label_widget = QLabel(label_widget)
    label_widget.setStyleSheet(label_style)

    icon_widget = GetGIF(path,size)

    layout.addWidget(icon_widget,0,Qt.AlignVCenter)
    layout.addWidget(label_widget,0,Qt.AlignVCenter)
    
    layout.addStretch(1)

    widget.setLayout(layout)

    widget.setStyleSheet("border:none;outline:none")

    return widget