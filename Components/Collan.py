from PyQt5.QtWidgets import QLabel
import Styles.styles as styles

def getCollan(style = styles.text_style3):
    label = QLabel(":")
    label.setStyleSheet(style)
    return label