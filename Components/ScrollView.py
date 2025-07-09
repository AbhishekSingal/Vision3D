from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout,
    QSplitter, QComboBox
)
from PyQt5.QtChart import QChart, QChartView, QLineSeries
from PyQt5.QtGui import QPixmap, QPainter, QColor
from PyQt5.QtCore import Qt, QPointF

# ──────────────── Project Imports ────────────────
from Components.Separator import SeparatorLine
from Components.VerticalIconTextButton import VerticalIconTextButton
import Styles.styles as styles
import Styles.colors as cl


from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea
from PyQt5.QtCore import Qt

class ScrollView(QWidget):
    def __init__(self,widget:QWidget,bg=cl.SYS_BG3):
        super().__init__()
        self.widget = widget
        self.bg = bg
        self.setup_ui()

    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        self.setStyleSheet(styles.panel_style1)  # External style

        layout = QVBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        # Scroll Area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setStyleSheet(styles.scrollbar_style)

        # Container inside the scroll area
        self.scroll_content = QWidget()
        self.scroll_content.setStyleSheet(f"background-color:{self.bg}")

        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.scroll_layout.setContentsMargins(1,1,1,1)
        self.scroll_layout.setSpacing(0)

        self.scroll_layout.addWidget(self.widget)

        self.scroll_content.setLayout(self.scroll_layout)

        scroll_area.setWidget(self.scroll_content)

        layout.addWidget(scroll_area,1)


        self.setLayout(layout)

