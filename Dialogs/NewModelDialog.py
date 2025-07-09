from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QDialogButtonBox,QWidget,QPushButton,QFileDialog
)
from PyQt5.QtCore import Qt

from Utils.LayoutUtils import GetBoxWidget
from Utils.IconUtils import GetIconLabel
from Utils.LabelInput import GetLabelLineEdit
import Styles.styles as styles
import Styles.colors as cl

class NewModelDialog(QDialog):
    def __init__(self, parent=None, title=""):
        super().__init__(parent)
        self.setWindowTitle("Create New File")
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

        layout = QVBoxLayout()
        layout.setContentsMargins(15,15,15,15)
        layout.setSpacing(0)


        self.file_l = QLabel("File Name")
        self.file_l.setStyleSheet(styles.text_style3+"QLabel{font-size:12px}")
        self.file_l.setFixedWidth(60)

        self.file_i = QLineEdit()
        self.file_i.setPlaceholderText("Type File Name")
        self.file_i.setStyleSheet(styles.input_style4)
        self.file_i.setFixedHeight(30)

        self.folder_l = QLabel("Location")
        self.folder_l.setStyleSheet(styles.text_style3+"QLabel{font-size:12px}")
        self.folder_l.setFixedWidth(60)

        self.folder_i = QLineEdit()
        self.folder_i.setPlaceholderText("Select or Type Folder Path")
        self.folder_i.setStyleSheet(styles.input_style4)
        self.folder_i.setFixedHeight(30)

        self.folder_btn = QPushButton("Select")
        self.folder_btn.setFixedHeight(30)
        self.folder_btn.setFixedWidth(60)
        self.folder_btn.setStyleSheet(styles.button_style6)
        self.folder_btn.clicked.connect(self.selectFolder)

        self.ok_btn = QPushButton("Create File")
        self.cancel_btn = QPushButton("Cancel")

        self.ok_btn.setStyleSheet(styles.button_style5)
        self.cancel_btn.setStyleSheet(styles.button_style6)

        self.ok_btn.setFixedWidth(130)
        self.ok_btn.setFixedHeight(30)
        self.ok_btn.setShortcut(Qt.Key_Return)

        self.cancel_btn.setFixedWidth(130)
        self.cancel_btn.setFixedHeight(30)
        self.cancel_btn.setShortcut(Qt.Key_Escape)

        collan1 = QLabel(":")
        collan2 = QLabel(":")

        collan1.setStyleSheet(styles.text_style3)
        collan2.setStyleSheet(styles.text_style3)



        fileW = GetBoxWidget([
            (self.file_l,0),
            (collan1,0),
            "5",
            (self.file_i,1)
        ],Qt.Horizontal)

        folderW = GetBoxWidget([
            (self.folder_l,0),
            (collan2,0),
            "5",
            (self.folder_i,1),
            "5",
            (self.folder_btn,0)
        ],Qt.Horizontal)

        buttonW = GetBoxWidget([
            1,
            (self.cancel_btn,0),
            "5",
            (self.ok_btn,0)
        ],Qt.Horizontal)

        layout.addWidget(fileW,0)
        layout.addSpacing(10)
        layout.addWidget(folderW,0)
        layout.addSpacing(20)
        layout.addStretch(1)
        layout.addWidget(buttonW)



        self.ok_btn.clicked.connect(self.accept)
        self.cancel_btn.clicked.connect(self.reject)
        self.setLayout(layout)

        self.setFixedSize(550,150)
    
    def selectFolder(self,event=None):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.folder_i.setText(folder)

    def getInput(self):
        result = self.exec_()
        if result != QDialog.Accepted:
            return (None,None) , QDialog.Rejected
        
        return (self.file_i.text(),self.folder_i.text()),(result == QDialog.Accepted)
    

