from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QDialogButtonBox,QWidget,QPushButton
)
from PyQt5.QtCore import Qt

from Components.Collan import getCollan
from Utils.LayoutUtils import GetBoxWidget
from Utils.LabelInput import GetLabelLineEdit
import Styles.styles as styles
import Styles.colors as cl

class InputDialog(QDialog):
    def __init__(self, parent=None, title="",prompt = "",placeholder="",ok_text="OK",cancel_text="Cancel"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

        layout = QVBoxLayout()
        layout.setContentsMargins(15,15,15,15)
        layout.setSpacing(0)
        self.l,self.i = GetLabelLineEdit(prompt,placeholder,styles.text_style3,input_style=styles.input_style4,input_height=30)

        w1 = QWidget()
        l1 = QVBoxLayout()
        l1.setContentsMargins(0,0,0,0)
        l1.setSpacing(0)

        l1.addWidget(self.l,0)
        l1.addSpacing(2)
        l1.addWidget(self.i,1)

        w1.setLayout(l1)


        w2 = QWidget()
        l2 = QHBoxLayout()
        l2.setContentsMargins(0,0,0,0)
        l2.setSpacing(5)

        self.ok_btn = QPushButton(ok_text)
        self.cancel_btn = QPushButton(cancel_text)

        self.ok_btn.setStyleSheet(styles.button_style5)
        self.cancel_btn.setStyleSheet(styles.button_style6)

        self.ok_btn.setFixedWidth(130)
        self.ok_btn.setFixedHeight(30)
        self.ok_btn.setShortcut(Qt.Key_Return)

        self.cancel_btn.setFixedWidth(130)
        self.cancel_btn.setFixedHeight(30)
        self.cancel_btn.setShortcut(Qt.Key_Escape)

        l2.addWidget(self.cancel_btn)
        l2.addWidget(self.ok_btn)

        w2.setLayout(l2)

        layout.addWidget(w1)
        layout.addSpacing(10)
        layout.addWidget(w2)


        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.setLayout(layout)

        self.setFixedSize(295,130)

    def getInput(self):
        result = self.exec_()
        if result != QDialog.Accepted:
            return 0 , QDialog.Rejected
        text = self.i.text().strip()
        return text or "", (result == QDialog.Accepted)

class TwoInputDialog(QDialog):
    def __init__(self, parent=None, title="",prompt1 = "",placeholder1="",prompt2 = "",placeholder2="",ok_text="OK",cancel_text="Cancel"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

        layout = QVBoxLayout()
        layout.setContentsMargins(15,15,15,15)
        layout.setSpacing(0)
        self.l1,self.i1 = GetLabelLineEdit(prompt1,placeholder1,styles.text_style3,input_style=styles.input_style4,input_height=30)
        self.l2,self.i2 = GetLabelLineEdit(prompt2,placeholder2,styles.text_style3,input_style=styles.input_style4,input_height=30)

        self.ok_btn = QPushButton(ok_text)
        self.cancel_btn = QPushButton(cancel_text)

        self.ok_btn.setStyleSheet(styles.button_style5)
        self.cancel_btn.setStyleSheet(styles.button_style6)

        self.ok_btn.setFixedWidth(130)
        self.ok_btn.setFixedHeight(30)
        self.ok_btn.setShortcut(Qt.Key_Return)

        self.cancel_btn.setFixedWidth(130)
        self.cancel_btn.setFixedHeight(30)
        self.cancel_btn.setShortcut(Qt.Key_Escape)

        w1 = GetBoxWidget([(self.l1,1),"5",(getCollan(),0),"5",(self.i1,4)],Qt.Horizontal)
        w2 = GetBoxWidget([(self.l2,1),"5",(getCollan(),0),"5",(self.i2,4)],Qt.Horizontal)
        bw = GetBoxWidget([1,(self.cancel_btn,0),"5",(self.ok_btn,0)],Qt.Horizontal)

        layout.addWidget(w1)
        layout.addSpacing(5)
        layout.addWidget(w2)
        layout.addSpacing(10)
        layout.addWidget(bw)



        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.setLayout(layout)

        self.setFixedSize(295,160)

    def getInput(self):
        result = self.exec_()
        if result != QDialog.Accepted:
            return (0,0) , QDialog.Rejected
        text = self.i1.text().strip()
        return (self.i1.text(),self.i2.text()), (result == QDialog.Accepted)
