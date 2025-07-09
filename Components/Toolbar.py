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

from Utils.IconUtils import GetIconLabel
from Utils.LabelInput import GetLabelCombo


class Toolbar(QWidget):
    def __init__(self):
        super().__init__()
        self.setup_ui()
    
    def setup_ui(self):
        self.setAttribute(Qt.WA_StyledBackground, True)
        layout = QHBoxLayout()
        layout.setContentsMargins(0,0,0,0)
        layout.setSpacing(0)

        #Logo
        self.logo = QLabel()
        self.logo.setPixmap(QPixmap("assets/sppl-logo-white.png"))
        self.logo.setFixedSize(50, 50)
        self.logo.setStyleSheet("margin:5px")
        self.logo.setScaledContents(True)

        self.logoLabel1 = QLabel("Sanrachna Prahari Pvt Ltd India\nAn IIT Delhi Company")
        self.logoLabel1.setStyleSheet("QLabel{color:white;font-size:12px;font-weight:600;}")
 

        #Toolbar Buttons
        self.addSensorBtn = VerticalIconTextButton("assets/addicon100.png","Add Sensor",size=35)
        self.systemSettingsBtn = VerticalIconTextButton("assets/settingsicon100.png","Settings",size=35)
        self.devicesBtn = VerticalIconTextButton("assets/hardwareicon100.png","Devices")
        self.recordingsBtn = VerticalIconTextButton("assets/recordsicon100.png","Records")
        self.infoBtn = VerticalIconTextButton("assets/infoicon100.png","Site Info")
        self.systemBtn = VerticalIconTextButton("assets/systemicon100.png","System")
        self.accountBtn = VerticalIconTextButton("assets/accounticon100.png","Account",size=35)
        
        self.layoutBtn = VerticalIconTextButton("assets/layouticon100.png","Layout",size=35)
        self.panelsBtn = VerticalIconTextButton("assets/viewicon100.png","Panels",size=35)

        #Separators
        line1 = SeparatorLine(color=f"{cl.SYS_SEP1}", orientation="V", length=60, thickness=1)
        line2 = SeparatorLine(color=f"{cl.SYS_SEP1}", orientation="V", length=60, thickness=1)
        line3 = SeparatorLine(color=f"{cl.SYS_SEP1}", orientation="V", length=60, thickness=1)


        #Sensor Ribbon
        sensorComboPanel = QWidget()
        sensorComboPanel_layout = QVBoxLayout()
        sensorComboPanel_layout.setContentsMargins(0,0,0,0)
        sensorComboPanel_layout.setSpacing(2)

        sensor_l , self.sensor_i = GetLabelCombo(" Current Sensor :",["S20001","S30187","S00010"],label_style=f"color:{cl.SYS_FG1};font-size:10px")
        self.sensor_i.setFixedWidth(120)
        self.sensor_settings_icon = GetIconLabel("Sensor Settings","assets/settingsicon100.png",20,label_style=styles.text_style3)

        sensorComboPanel_layout.addWidget(sensor_l)
        sensorComboPanel_layout.addWidget(self.sensor_i)
        sensorComboPanel_layout.addSpacing(5)
        sensorComboPanel_layout.addWidget(self.sensor_settings_icon)

        sensorComboPanel.setLayout(sensorComboPanel_layout)


        #Layout Ribbon
        layoutOptionsPanel = QWidget()
        layoutOptionsPanel_layout = QVBoxLayout()
        layoutOptionsPanel_layout.setContentsMargins(0,0,0,0)
        layoutOptionsPanel_layout.setSpacing(1)

        self.minimalicon = GetIconLabel("Minimal Layout","assets/squaresicon100.png",size=20,label_style=f"color:{cl.SYS_FG1};font-size:12px")
        self.complexicon = GetIconLabel("Complex Layout","assets/complexicon100.png",size=20,label_style=f"color:{cl.SYS_FG1};font-size:12px")

        layoutOptionsPanel_layout.addStretch(1)
        layoutOptionsPanel_layout.addWidget(self.minimalicon,0)
        layoutOptionsPanel_layout.addSpacing(10)
        layoutOptionsPanel_layout.addWidget(self.complexicon,0)
        layoutOptionsPanel_layout.addStretch(1)

        layoutOptionsPanel.setLayout(layoutOptionsPanel_layout)


        #Tools Ribbon
        toolsPanel = QWidget()
        toolsPanel_layout = QVBoxLayout()
        toolsPanel_layout.setContentsMargins(0,0,0,0)
        toolsPanel_layout.setSpacing(1)

        self.saIcon = GetIconLabel("Signal Analysis","assets/signalicon100.png",20,label_style=f"color:{cl.SYS_FG1};font-size:12px")
        self.shmIcon = GetIconLabel("SHM Analysis","assets/buildingicon100.png",20,label_style=f"color:{cl.SYS_FG1};font-size:12px")

        toolsPanel_layout.addStretch(1)
        toolsPanel_layout.addWidget(self.saIcon,0)
        toolsPanel_layout.addSpacing(10)
        toolsPanel_layout.addWidget(self.shmIcon,0)
        toolsPanel_layout.addStretch(1)

        toolsPanel.setLayout(toolsPanel_layout)


        #Accounts Ribbon
        accountsPanel = QWidget()
        accountsPanel_layout = QVBoxLayout()
        accountsPanel_layout.setContentsMargins(0,0,0,0)
        accountsPanel_layout.setSpacing(2)

        self.closeIcon = GetIconLabel("Close","assets/closeicon100.png",20,label_style=f"color:{cl.SYS_FG1};font-size:12px")
        self.logIcon = GetIconLabel("Logs","assets/logicon100.png",20,label_style=f"color:{cl.SYS_FG1};font-size:12px")

        accountsPanel_layout.addStretch(1)
        accountsPanel_layout.addWidget(self.closeIcon,0)
        accountsPanel_layout.addSpacing(10)
        accountsPanel_layout.addWidget(self.logIcon,0)
        accountsPanel_layout.addStretch(1)

        accountsPanel.setLayout(accountsPanel_layout)


        #Setting Hover and Cursor
        labels = [self.sensor_settings_icon,self.minimalicon,self.complexicon,self.saIcon,self.shmIcon,self.closeIcon,self.logIcon]
        for l in labels:
            l.setCursor(Qt.PointingHandCursor)
            l.setStyleSheet(f"""QWidget:hover{{border:1px solid {cl.SYS_FG2}}}
                            QLabel:hover{{border:none}}""")

        #Adding to Layout
        layout.addSpacing(10)
        layout.addWidget(self.logo,0,Qt.AlignVCenter)
        layout.addSpacing(10)
        layout.addWidget(self.logoLabel1,0,Qt.AlignVCenter)
        layout.addStretch(1)

        layout.addWidget(self.addSensorBtn,0,Qt.AlignVCenter)
        layout.addWidget(self.devicesBtn,0,Qt.AlignVCenter)
        layout.addWidget(sensorComboPanel,0,Qt.AlignVCenter)
        layout.addWidget(self.recordingsBtn,0,Qt.AlignVCenter)

        layout.addWidget(line1,Qt.AlignVCenter)

        layout.addWidget(self.layoutBtn,Qt.AlignVCenter)
        layout.addWidget(layoutOptionsPanel)
        layout.addWidget(self.panelsBtn,Qt.AlignVCenter)

        layout.addWidget(line2,Qt.AlignVCenter)


        layout.addWidget(self.systemSettingsBtn)
        layout.addWidget(self.systemBtn)
        layout.addWidget(self.infoBtn)
        layout.addWidget(toolsPanel)
        layout.addSpacing(20)

        layout.addWidget(line3,Qt.AlignVCenter)

        layout.addSpacing(20)
        layout.addWidget(accountsPanel)
        layout.addWidget(self.accountBtn)

        
        self.setLayout(layout)
        self.setFixedHeight(90)
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")  