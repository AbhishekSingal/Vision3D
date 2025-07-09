from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit,QWidget,QPushButton,QCheckBox
)
from PyQt5.QtCore import Qt

from Components.Collan import getCollan
from Utils.LayoutUtils import GetBoxWidget
from Utils.LabelInput import GetLabelLineEdit
import Styles.styles as styles
import Styles.colors as cl


class SurfaceCopyDialog(QDialog):
    def __init__(self, parent=None, title="Create Surface Copies",ok_text="Create",cancel_text="Cancel"):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

        layout = QVBoxLayout()
        layout.setContentsMargins(15,15,15,15)
        layout.setSpacing(0)
        self.l1,self.i1 = GetLabelLineEdit("Copies","Enter Integer",styles.text_style3,input_style=styles.input_style4,input_height=30)
        self.l2,self.i2 = GetLabelLineEdit("Distance","Enter Decimal",styles.text_style3,input_style=styles.input_style4,input_height=30)

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

        self.lineChbx = QCheckBox("Connect with Lines")
        self.lineChbx.setStyleSheet(styles.checkbox_style1)
        self.lineChbx.setChecked(False)

        self.borderChbx = QCheckBox("Draw Border Lines")
        self.borderChbx.setStyleSheet(styles.checkbox_style1)
        self.borderChbx.setChecked(False)

        self.surfaceChbx = QCheckBox("Draw Surfaces")
        self.surfaceChbx.setStyleSheet(styles.checkbox_style1)
        self.surfaceChbx.setChecked(False)

        w1 = GetBoxWidget([(self.l1,1),"5",(getCollan(),0),"5",(self.i1,4)],Qt.Horizontal)
        w2 = GetBoxWidget([(self.l2,1),"5",(getCollan(),0),"5",(self.i2,4)],Qt.Horizontal)
        bw = GetBoxWidget([1,(self.cancel_btn,0),"5",(self.ok_btn,0)],Qt.Horizontal)

        layout.addWidget(w1)
        layout.addSpacing(5)
        layout.addWidget(w2)
        layout.addSpacing(10)
        layout.addWidget(self.lineChbx)
        layout.addSpacing(5)
        layout.addWidget(self.borderChbx)
        layout.addSpacing(5)
        layout.addWidget(self.surfaceChbx)
        layout.addSpacing(15)
        layout.addWidget(bw)



        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.setLayout(layout)

        self.setFixedSize(295,210)

    def getInput(self):
        result = self.exec_()
        if result != QDialog.Accepted:
            return (0,0) , QDialog.Rejected
        text = self.i1.text().strip()
        return (self.i1.text(),self.i2.text(),self.lineChbx.isChecked(),self.borderChbx.isChecked(),self.surfaceChbx.isChecked()), (result == QDialog.Accepted)
