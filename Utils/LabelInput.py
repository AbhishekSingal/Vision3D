from PyQt5.QtWidgets import (
    QLabel,QLineEdit
)
from qfluentwidgets import ComboBox
import Styles.styles as styles

from Utils.IconUtils import GetIconLabel

def GetLabelLineEdit(label_text,placeholder_text,label_style = styles.text_style3 , input_style = styles.input_style2 , input_height = 24):
    label = QLabel(label_text)
    label.setStyleSheet(label_style)

    input = QLineEdit()
    input.setPlaceholderText(placeholder_text)
    input.setStyleSheet(input_style)
    input.setFixedHeight(input_height)

    return label,input

def GetIconLabelLineEdit(label_text,icon_path,icon_size,placeholder_text,label_style = styles.text_style3 , input_style = styles.input_style2 , input_height = 24):
    label = GetIconLabel(label_text,icon_path,icon_size,label_style)

    input = QLineEdit()
    input.setPlaceholderText(placeholder_text)
    input.setStyleSheet(input_style)
    input.setFixedHeight(input_height)

    return label,input

def GetLabelCombo(label_text,combo_items,label_style=styles.text_style3,combo_height = 25):
    label = QLabel(label_text)
    label.setStyleSheet(label_style)
    combo = ComboBox()
    combo.addItems(combo_items)
    dfont = combo.font()
    dfont.setPixelSize(11)
    combo.setFont(dfont)
    combo.setFixedHeight(combo_height)

    return label,combo

def GetIconLabelCombo(label_text,icon_path,icon_size,combo_items,label_style=styles.text_style3,combo_height = 25):
    label = GetIconLabel(label_text,icon_path,icon_size,label_style)
    combo = ComboBox()
    combo.addItems(combo_items)
    dfont = combo.font()
    dfont.setPixelSize(11)
    combo.setFont(dfont)
    combo.setFixedHeight(combo_height)

    return label,combo