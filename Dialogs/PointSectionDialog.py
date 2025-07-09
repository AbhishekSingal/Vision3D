from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QDialogButtonBox,QWidget,QPushButton,QSlider
)
from PyQt5.QtCore import Qt

from fractions import Fraction

from Utils.LabelInput import GetLabelLineEdit
from Utils.LayoutUtils import GetBoxWidget
from Components.Collan import getCollan
import Styles.styles as styles
import Styles.colors as cl

class PointSectionDialog(QDialog):
    def __init__(self, parent=None, title="Insert Sectional Point",ok_text="Add Point",cancel_text="Cancel",p1=[0,0,0],p2=[0,0,0]):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

        layout = QVBoxLayout()
        layout.setContentsMargins(15,15,15,15)
        layout.setSpacing(0)

        p1_l,self.p1_i = GetLabelLineEdit(f"Point1 ({p1[0]},{p1[1]},{p1[2]})","Enter Factor",input_style=styles.input_style3)
        p2_l,self.p2_i = GetLabelLineEdit(f"Point2 ({p2[0]},{p2[1]},{p2[2]})","Enter Factor",input_style=styles.input_style3)

        self.p1_i.setText("1")
        self.p2_i.setText("1")
        self.p1_i.textChanged.connect(self.setSlider)
        self.p2_i.textChanged.connect(self.setSlider)

        p1_l.setFixedWidth(160)
        p2_l.setFixedWidth(160)

        p1_w = GetBoxWidget([(p1_l,0),(getCollan(),0),"10",(self.p1_i,0)],Qt.Horizontal)
        p2_w = GetBoxWidget([(p2_l,0),(getCollan(),0),"10",(self.p2_i,0)],Qt.Horizontal)


        p1_s = QLabel("Point1")
        p2_s = QLabel("Point2")
        p1_s.setStyleSheet(styles.text_style3)
        p2_s.setStyleSheet(styles.text_style3)

        self.slider = QSlider(Qt.Horizontal)
        self.slider.setRange(0,100)
        self.slider.setTickInterval(1)
        self.slider.setValue(50)
        self.slider.setTickPosition(QSlider.NoTicks)
        self.slider.valueChanged.connect(self.setInputs)

        sw = GetBoxWidget([(p1_s,0),(self.slider,1),(p2_s,0)],Qt.Horizontal)

 
        self.ok_btn = QPushButton(ok_text)
        self.cancel_btn = QPushButton(cancel_text)

        self.ok_btn.setStyleSheet(styles.button_style5)
        self.cancel_btn.setStyleSheet(styles.button_style6)

        self.ok_btn.setFixedWidth(130)
        self.ok_btn.setFixedHeight(30)

        self.cancel_btn.setFixedWidth(130)
        self.cancel_btn.setFixedHeight(30)
        self.cancel_btn.setShortcut(Qt.Key_Escape)

        bw = GetBoxWidget([1,(self.cancel_btn,0),"5",(self.ok_btn,0)],Qt.Horizontal)

        layout.addWidget(p1_w)
        layout.addSpacing(5)
        layout.addWidget(p2_w)
        layout.addSpacing(15)
        layout.addWidget(sw)
        layout.addSpacing(15)
        layout.addWidget(bw)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.setLayout(layout)

        self.setFixedWidth(295)
        self.setFixedHeight(180)


    def setSlider(self):
        try:
            r1 = float(self.p1_i.text())
            r2 = float(self.p2_i.text())
            if r1 + r2 == 0:
                return
            value = int(r1 * (100 / (r1 + r2)))

            self.slider.blockSignals(True)  # 🔒 Prevent signal recursion
            self.slider.setValue(value)
            self.slider.blockSignals(False)  # 🔓 Re-enable signals

        except ValueError:
            pass  # Optional: handle bad input

    def setInputs(self, value):
        r1 = value
        r2 = 100 - value

        if r2 == 0:
            self.p1_i.setText("1")
            self.p2_i.setText("0")
            return

        fract = Fraction(r1, r2)

        # Prevent recursive triggering
        self.p1_i.blockSignals(True)
        self.p2_i.blockSignals(True)
        self.p1_i.setText(str(fract.numerator))
        self.p2_i.setText(str(fract.denominator))
        self.p1_i.blockSignals(False)
        self.p2_i.blockSignals(False)




    def getInput(self):
        result = self.exec_()
        if result != QDialog.Accepted:
            return (0,0) , QDialog.Rejected
        
        return (float(self.p1_i.text()),float(self.p2_i.text())),(result == QDialog.Accepted)
