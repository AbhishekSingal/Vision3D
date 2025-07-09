from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout,QWidget,QPushButton,QTableWidget, QTableWidgetItem,
    QHeaderView,QSizePolicy
)
from PyQt5.QtCore import Qt

from Utils.LayoutUtils import GetBoxWidget
from Components.ScrollView import ScrollView
import Styles.styles as styles
import Styles.colors as cl

class MultiplePointsDialog(QDialog):
    def __init__(self, parent=None, title="Add Multiple Points",points=0):
        super().__init__(parent)
        self.setWindowTitle(title)
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")
        self.points = points

        layout = QVBoxLayout()
        layout.setContentsMargins(15,15,15,15)
        layout.setSpacing(0)

        self.table = QTableWidget(points, 3)  # rows = points, columns = 4
        self.table.setTabKeyNavigation(True)
        self.table.setHorizontalHeaderLabels(["X Coordinate", "Y Coordinate", "Z Coordinate"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Maximum)
        self.table.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.table.setVerticalHeaderLabels([f"Point {i+1}" for i in range(points)])
        self.table.setStyleSheet(styles.table_style1+styles.scrollbar_style)
        self.table.horizontalHeader().setStyleSheet(f"""
            QHeaderView::section {{
                background-color: {cl.SYS_BD1};
                color: {cl.SYS_FG1};
                font-weight: bold;
                padding: 4px;
                border: 1px solid {cl.SYS_BD3};
                border-left:none;
                border-top:none;
            }}
        """)
        self.table.verticalHeader().setStyleSheet(f"""
            QHeaderView::section {{
                background-color: {cl.SYS_BD1};
                color: {cl.SYS_FG1};
                font-weight: 400;
                padding: 4px;
                border: 1px solid {cl.SYS_BD3};
                border-top:none;
                border-left:none;
            }}
        """)

        self.table.setStyleSheet(self.table.styleSheet()+f"""
            QTableCornerButton::section {{
                background-color: {cl.SYS_BD1};
                border: 1px solid {cl.SYS_BD3};
                border-top:none;
                border-left:none;
            }}
        """)
        

        self.ok_btn = QPushButton("Add Points")
        self.cancel_btn = QPushButton("Cancel")

        self.ok_btn.setStyleSheet(styles.button_style5)
        self.cancel_btn.setStyleSheet(styles.button_style6)

        # self.ok_btn.setFixedWidth(120)
        self.ok_btn.setFixedHeight(30)
        # self.ok_btn.setShortcut(Qt.Key_Return)

        # self.cancel_btn.setFixedWidth(120)
        self.cancel_btn.setFixedHeight(30)
        self.cancel_btn.setShortcut(Qt.Key_Escape)

        
        bw = GetBoxWidget([1,(self.cancel_btn,1),"5",(self.ok_btn,1)],Qt.Horizontal)
        layout.addWidget(self.table,0)
        layout.addSpacing(15)
        layout.addWidget(bw,0)

        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.setLayout(layout)

        self.setFixedWidth(400)
        if points == 2:
            self.setFixedHeight(170)
        elif points == 3:
            self.setFixedHeight(200)
        elif points >= 4:
            self.setFixedHeight(230)


    

    def getInput(self):
        coords = []
        result = self.exec_()

        if result != QDialog.Accepted:
            return [] , QDialog.Rejected

        for r in range(0,self.points):
            coord = []
            for c in range(0,3):
                val = self.table.item(r,c).text()
                coord.append(float(val))
            coords.append(coord)

        return coords , (result == QDialog.Accepted)


# class MultiplePointsDialog(QDialog):
#     def __init__(self, parent=None, title="Add Multiple Points",points=0):
#         super().__init__(parent)
#         self.setWindowTitle(title)
#         self.setModal(True)
#         self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
#         self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

#         layout = QVBoxLayout()
#         layout.setContentsMargins(15,15,15,15)
#         layout.setSpacing(0)

#         self.inputs = []

#         self.ok_btn = QPushButton("ok")
#         self.cancel_btn = QPushButton("cancel")

#         self.ok_btn.setStyleSheet(styles.button_style3)
#         self.cancel_btn.setStyleSheet(styles.button_style4)

#         self.ok_btn.setFixedWidth(120)
#         self.ok_btn.setFixedHeight(30)
#         self.ok_btn.setShortcut(Qt.Key_Return)

#         self.cancel_btn.setFixedWidth(120)
#         self.cancel_btn.setFixedHeight(30)
#         self.cancel_btn.setShortcut(Qt.Key_Escape)

#         points_widget = QWidget()
#         points_layout = QVBoxLayout()
#         points_layout.setContentsMargins(0,0,0,0)
#         points_layout.setSpacing(0)
#         points_widget.setLayout(points_layout)

#         scrollView = ScrollView(points_widget)
#         bw = GetBoxWidget([1,(self.cancel_btn,0),"10",(self.ok_btn,0)],Qt.Horizontal)



#         for p in range(0,points):
#             w = QWidget()
#             w.setStyleSheet(f"border:none;outline:none;background-color:{cl.SYS_BG2}")
#             l = QHBoxLayout()
#             l.setContentsMargins(5,5,5,5)
#             l.setSpacing(0)

#             point = QLabel(f"Point{p+1}")
#             point.setStyleSheet(styles.text_style3)
#             l.addWidget(point,0,Qt.AlignVCenter)
#             l.addSpacing(50)

#             for i in [(1,"x :"),(2,"y :"),(3,"z :")]:
#                 c_l = QLabel(i[1])
#                 c_l.setStyleSheet(styles.text_style3+f"QLabel{{color:{cl.SYS_FG2}}}")
#                 input_ = QLineEdit()
#                 input_.setPlaceholderText("Enter Decimal")
#                 input_.setStyleSheet(styles.input_style4)
#                 l.addWidget(c_l,0,Qt.AlignVCenter)
#                 l.addWidget(input_,1,Qt.AlignVCenter)
#                 self.inputs.append(input_)
#                 l.addSpacing(15)

#             w.setLayout(l)
#             points_layout.addWidget(w)
                



#         layout.addWidget(scrollView,1)
#         layout.addSpacing(15)
#         layout.addWidget(bw,0)

#         self.ok_btn.clicked.connect(self.accept)
#         self.cancel_btn.clicked.connect(self.reject)
#         self.setLayout(layout)

#         self.setFixedWidth(500)
#         self.setMaximumHeight(300)

#     def getInput(self):
#         coords = []
#         result = self.exec_()
#         if result != QDialog.Accepted:
#             return [] , QDialog.Rejected
#         for i in range(0, len(self.inputs), 3):
#             x = float(self.inputs[i].text())
#             y = float(self.inputs[i + 1].text())
#             z = float(self.inputs[i + 2].text())
#             coords.append([x, y, z])
        
#         return coords , (result == QDialog.Accepted)
    
    


