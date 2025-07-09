from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QDialogButtonBox,QWidget,QPushButton
)
from PyQt5.QtCore import Qt

from Utils.LabelInput import GetLabelLineEdit
from Utils.LayoutUtils import GetBoxWidget
import Styles.styles as styles
import Styles.colors as cl

class EditPointDialog(QDialog):
    def __init__(self, parent=None, title="",initial = [0,0,0]):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

        layout = QVBoxLayout()
        layout.setContentsMargins(15,25,15,5)
        layout.setSpacing(0)
        
        self.xl,self.xi = GetLabelLineEdit("X Coordinate :","Enter Decimal",label_style=styles.text_style3,input_style=styles.input_style3)
        self.yl,self.yi = GetLabelLineEdit("Y Coordinate :","Enter Decimal",label_style=styles.text_style3,input_style=styles.input_style3)
        self.zl,self.zi = GetLabelLineEdit("Z Coordinate :","Enter Decimal",label_style=styles.text_style3,input_style=styles.input_style3)

        self.xi.setText(str(initial[0]))
        self.yi.setText(str(initial[1]))
        self.zi.setText(str(initial[2]))

        self.ok_btn = QPushButton("Update Point")
        self.ok_btn.setStyleSheet(styles.button_style5)
        self.ok_btn.setFixedHeight(30)
        self.ok_btn.setShortcut(Qt.Key_Return)

        self.cancel_btn = QPushButton("Cancel")
        self.cancel_btn.setStyleSheet(styles.button_style6)
        self.cancel_btn.setFixedHeight(30)
        self.cancel_btn.setShortcut(Qt.Key_Escape)

        widget = GetBoxWidget([
            (GetBoxWidget([(self.xl,0),(self.xi,1)],Qt.Horizontal,spacing=10),0),
            (GetBoxWidget([(self.yl,0),(self.yi,1)],Qt.Horizontal,spacing=10),0),
            (GetBoxWidget([(self.zl,0),(self.zi,1)],Qt.Horizontal,spacing=10),0),
        ],Qt.Vertical,align=False,spacing=10)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)

        layout.addWidget(widget)
        layout.addSpacing(10)
        layout.addWidget(GetBoxWidget([(self.cancel_btn,1),(self.ok_btn,1)],Qt.Horizontal,spacing=5),0)


        self.setLayout(layout)

        # self.setFixedSize(292,150)
        self.setFixedWidth(280)
        self.setFixedHeight(180)

    def getInput(self):
        result = self.exec_()
        if result != QDialog.Accepted:
            return [] , QDialog.Rejected
        x = float(self.xi.text())
        y = float(self.yi.text())
        z = float(self.zi.text())

        return [x,y,z] , (result == QDialog.Accepted)
        # text = self.i.text().strip()
        # return text or "", (result == QDialog.Accepted)
