from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QDialogButtonBox,QWidget,QPushButton,QSizePolicy
)
from PyQt5.QtCore import Qt

from Components.ScrollView import ScrollView
from Utils.LabelInput import GetLabelLineEdit
from Utils.LayoutUtils import GetBoxWidget
from Utils.IconUtils import GetIcon
import Styles.styles as styles
import Styles.colors as cl

class MessageDialog(QDialog):
    INFO_DIALOG = ("Info","assets/infoicon100.png")
    WARNING_DIALOG = ("Warning","assets/warningicon100.png")
    ERROR_DIALOG = ("Error","assets/closeicon100.png")

    def __init__(self, parent=None,messageHeading="",message="",type=INFO_DIALOG):
        super().__init__(parent)
        self.setWindowTitle(type[0])
        self.setModal(True)
        self.setWindowFlag(Qt.WindowContextHelpButtonHint, False)
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

        layout = QVBoxLayout()
        layout.setContentsMargins(15,25,15,15)
        layout.setSpacing(0)

        icon = GetIcon(type[1],60)
        heading = QLabel(messageHeading)
        heading.setStyleSheet(styles.header_style1+"QLabel{font-size:14px}")
        message = QLabel(message)
        message.setWordWrap(True)
        message.setStyleSheet(styles.infotext_style2+"QLabel{font-size:11px}")

        widget = GetBoxWidget(
            [
                (GetBoxWidget([(icon,0),1],Qt.Vertical),0),
                (GetBoxWidget([
                    (heading,0),
                    "5",
                    (message,0)
                ],Qt.Vertical,align=False),1)
            ],Qt.Horizontal,spacing=10
        )

        self.ok_btn = QPushButton("OK")
        self.ok_btn.setStyleSheet(styles.button_style6)
        self.ok_btn.setFixedWidth(120)
        self.ok_btn.setFixedHeight(25)
        self.ok_btn.setShortcut(Qt.Key_Return)

        layout.addWidget(widget,1)
        layout.addSpacing(15)
        layout.addWidget(GetBoxWidget([1,(self.ok_btn,0)],Qt.Horizontal))


        self.ok_btn.clicked.connect(self.accept)
        self.setLayout(layout)

        self.setMinimumWidth(350)
        self.setMaximumHeight(200)


