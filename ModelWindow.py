# ──────────────── Qt Imports ────────────────
from PyQt5.QtWidgets import (
    QWidget, QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy,QMainWindow , QDockWidget , QPushButton ,  QCheckBox , QFileDialog  )
from PyQt5.QtGui import QPixmap, QColor , QGuiApplication,QDoubleValidator,QIcon
from PyQt5.QtCore import Qt, QPointF , QTimer,QEvent
from qfluentwidgets import ComboBox,TabBar

# ──────────────── System Imports ────────────────
import os
from pathlib import Path

# ──────────────── Project Imports ────────────────
from Graphics.Renderer import Renderer,Point,Line,Surface,Sensor
import Graphics.Math as Geometry

from Components.Separator import SeparatorLine , LabeledHorizontalLine
from Components.VerticalIconTextButton import VerticalIconTextButton
from Components.Logo import Logo
from Components.ScrollView import ScrollView
from Components.ColorPicker import ColorPickerButton

from Utils.IconUtils import GetIcon,GetIconLabel
from Utils.LayoutUtils import GetBoxWidget
from Utils.LabelInput import GetLabelLineEdit
from Utils.TooltipUtils import getTooltipHTML

from Dialogs.InputDialog import InputDialog
from Dialogs.SurfaceCopyDialog import SurfaceCopyDialog
from Dialogs.MultiplePointsDialog import MultiplePointsDialog
from Dialogs.MessageDialog import MessageDialog
from Dialogs.EditPointDialog import EditPointDialog
from Dialogs.NewModelDialog import NewModelDialog
from Dialogs.PointSectionDialog import PointSectionDialog

import Styles.styles as styles
import Styles.colors as cl


"""
Tools:
Draw Square/Rectangle
Draw Polygon
Draw Cube/Cuboid

Ribbon:
Mid Point/Section Formula  DONE
Insert Multiple Points Between Two Points DONE
Copy Points Above DONE
Padding REQ
Shift Points REQ
Distance b/w Selections REQ
Line Length REQ
Angle b/w Selections REQ
Intersections REQ
Normal of Plane REQ
Insert Point at distance along Vector

Units
"""

"""
File Managment
File Status (Saved/Unsaved)
"""


class ModelWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Vision3D")
        self.setStyleSheet(f"background-color:{cl.SYS_BG1}")

        self.filePath = None
        self.vibrating = False
        self.viewOnly = False

        self.currentFile = ""

        self.files = {}

        self.showMaximized()
        self.close()
        self.setup_ui()

    
    def setup_ui(self):
        self.createRibbon()

        #Toolbar Icons
        self.addpointTool = GetIcon("assets/anchoricon100.png",20)
        self.multiplepointsTool = GetIcon("assets/addpointsicon100.png",20)
        self.lineTool = GetIcon("assets/linetoolicon100.png",20)
        self.linePointTool = GetIcon("assets/linepointicon100.png",20)
        self.sensorTool = GetIcon("assets/addsensoricon100.png",20)
        self.borderTool = GetIcon("assets/bordertoolicon100.png",20)
        self.surfaceTool = GetIcon("assets/surfaceicon100.png",20)
        self.rectangleTool = GetIcon("assets/drawrectangleicon100.png",20)
        self.polygonTool = GetIcon("assets/drawpolygonicon100.png",20)
        self.cuboidTool = GetIcon("assets/drawcuboidicon100.png",20)

        #Toolbar Widget
        self.toolBar = GetBoxWidget(
            [
                1,
                (self.addpointTool,0),
                (self.multiplepointsTool,0),
                (self.lineTool,0),
                (self.linePointTool,0),
                (self.sensorTool,0),
                (self.borderTool,0),
                (self.surfaceTool,0),
                (self.rectangleTool,0),
                (self.polygonTool,0),
                (self.cuboidTool,0),
                2
            ],
            Qt.Vertical,
            spacing=15,
            align=False,
            contentMargins=(10,10,10,10)
        )


        #Renderer Panel
        self.rendererWidget = QWidget()
        self.rendererWidget.setStyleSheet(f"background-color:{cl.SYS_BG1};border:1px solid {cl.SYS_BD4}")
        self.renderer_layout = QVBoxLayout()
        self.renderer_layout.setContentsMargins(1,0,1,0)
        self.renderer_layout.setSpacing(0)

        self.renderer_tab = TabBar()
        self.renderer_tab.setFixedHeight(35)
        self.renderer_tab.setStyleSheet(f"border:none;border-bottom:1px solid {cl.SYS_BD4}")
        self.renderer_tab.setMovable(True)
        self.renderer_tab.setAddButtonVisible(False)
        self.renderer_tab.currentChanged.connect(self.tabChanged)
        self.renderer_tab.tabCloseRequested.connect(self.closeFile)

        self.renderer = Renderer()
        self.renderer_layout.addWidget(self.renderer_tab,0)
        self.renderer_layout.addWidget(self.renderer,1)
        self.rendererWidget.setLayout(self.renderer_layout)

        
        #QuickEdit Widget
        self.quickEditPanel = QWidget()
        self.quickEditPanel_layout = QHBoxLayout()
        self.quickEditPanel_layout.setContentsMargins(0,0,10,0)
        self.quickEditPanel_layout.setSpacing(5)
        self.quickEditPanel.setFixedHeight(50)

        self.statusIcon = GetIcon("assets/tickicon100.png",20)
        self.statusText = QLabel("Ready for Drawing")
        self.statusText.setStyleSheet(styles.text_style3)

        self.statusWidget = GetBoxWidget([(self.statusIcon,0),"5",(self.statusText,0)],Qt.Horizontal)

        x,self.xi = GetLabelLineEdit("x :","Enter Decimal",styles.text_style3+"QLabel{font-size:12px}",input_style=styles.input_style4,input_height=25)
        y,self.yi = GetLabelLineEdit("y :","Enter Decimal",styles.text_style3+"QLabel{font-size:12px}",input_style=styles.input_style4,input_height=25)
        z,self.zi = GetLabelLineEdit("z :","Enter Decimal",styles.text_style3+"QLabel{font-size:12px}",input_style=styles.input_style4,input_height=25)
        self.xyzValidator = QDoubleValidator()
        self.xyzValidator.setNotation(QDoubleValidator.StandardNotation)

        for i in [self.xi,self.yi,self.zi]:
            i.setFixedWidth(150)
            i.setValidator(self.xyzValidator)
            i.installEventFilter(self)


        self.addPointButton = QPushButton("Add Point")
        self.addPointButton.setStyleSheet(styles.button_style5)
        self.addPointButton.setFixedSize(120,25)

        self.quickEditPanel_layout.addWidget(self.statusWidget)
        self.quickEditPanel_layout.addStretch(1)


        self.quickEditPanel_layout.addWidget(x,0,Qt.AlignVCenter)
        self.quickEditPanel_layout.addWidget(self.xi,0,Qt.AlignVCenter)

        self.quickEditPanel_layout.addSpacing(10)

        self.quickEditPanel_layout.addWidget(y,0,Qt.AlignVCenter)
        self.quickEditPanel_layout.addWidget(self.yi,0,Qt.AlignVCenter)

        self.quickEditPanel_layout.addSpacing(10)

        self.quickEditPanel_layout.addWidget(z,0,Qt.AlignVCenter)
        self.quickEditPanel_layout.addWidget(self.zi,0,Qt.AlignVCenter)

        self.quickEditPanel_layout.addSpacing(10)

        self.quickEditPanel_layout.addWidget(self.addPointButton,0,Qt.AlignVCenter)
        

        self.quickEditPanel.setLayout(self.quickEditPanel_layout)




        #Model Settings Panel
        self.modelSettingPanel = QWidget()
        self.modelSettingPanel.setMinimumWidth(250)  
        self.modelSettingPanel.setStyleSheet(f"background-color:{cl.SYS_BG1};border: 1px solid {cl.SYS_BD4};border-top:none")  
        self.modelSettingsPanel_layout = QVBoxLayout()
        self.modelSettingsPanel_layout.setContentsMargins(15,10,15,10)
        self.modelSettingsPanel_layout.setSpacing(2)

        # === Objects ===
        self.objectsWidget = QWidget()
        self.objectsWidget.setStyleSheet("border:none;outline:none")
        self.objectsWidget_layout = QVBoxLayout()
        self.objectsWidget_layout.setContentsMargins(0, 0, 0, 0)
        self.objectsWidget_layout.setSpacing(0)
        self.objectsWidget.setLayout(self.objectsWidget_layout)
        pointsScrollView = ScrollView(self.objectsWidget)
        pointsScrollView.setStyleSheet("border:none")

        # === Customisations ===
        self.customisationsWidget = QWidget()
        self.customisationsWidget.setStyleSheet("border:none;outline:none")
        self.customisationsWidget_layout = QVBoxLayout()
        self.customisationsWidget_layout.setContentsMargins(10, 5, 5, 10)
        self.customisationsWidget_layout.setSpacing(2)
        self.customisationsWidget.setLayout(self.customisationsWidget_layout)
        self.setupCustomisations()
        lineScrollView = ScrollView(self.customisationsWidget)
        lineScrollView.setStyleSheet("border:none")

        # === Buttons ===
        self.reset_btn = QPushButton("Reset")
        self.update_btn = QPushButton("Update")

        self.reset_btn.setStyleSheet(styles.button_style4+"QPushButton{font-size:12px}")
        self.update_btn.setStyleSheet(styles.button_style3+"QPushButton{font-size:12px}")

        self.reset_btn.setFixedHeight(25)
        self.update_btn.setFixedHeight(25)
        bw = GetBoxWidget(
            [ (self.reset_btn,1) , "5" , (self.update_btn,1) ],
            Qt.Horizontal
        )

        self.objectsCombo = ComboBox()
        self.objectsCombo.addItems(["Points","Lines","Surfaces","Sensors"])
        self.objectsCombo.setFixedHeight(25)
        dfont = self.objectsCombo.font()
        dfont.setPixelSize(10)
        self.objectsCombo.setFont(dfont)
        self.selectAllBtn = GetIcon("assets/selectallicon100.png",20)
        self.deleteObjectsBtn = GetIcon("assets/deleteviewicon100.png",20)

        objectsHeader = GetBoxWidget(
            [
                (GetIconLabel("Objects :","assets/cubeicon100.png",20,styles.header_style4+"QLabel{font-size:13px;border:none}"),0),
                "10",
                (self.objectsCombo,1),
                "10",
                (self.selectAllBtn,0),
                "5",
                (self.deleteObjectsBtn,0)
            ],
            Qt.Horizontal
        )
        self.selectionText = QLabel("Total Points Selected : 0")
        self.selectionText.setStyleSheet(styles.text_style3+"QLabel{font-size:10px}")
        self.clearSelectionsBtn = GetIconLabel("Delete Selections","assets/cancelicon100.png",15,styles.text_style3+"QLabel{font-size:10px}")
        self.clearSelectionsBtn.setCursor(Qt.PointingHandCursor)
        objectFooter = GetBoxWidget([
            (self.selectionText,0),
            1,
            (self.clearSelectionsBtn,0)
        ],Qt.Horizontal)


        customisationsHeader = GetBoxWidget(
            [
                (GetIconLabel("Customisations :","assets/customizationsicon100.png",15,styles.header_style4+"QLabel{font-size:13px;border:none}"),0),
                1,
                (GetIconLabel("Import","assets/arrowdownicon100.png",15,styles.text_style3+"QLabel{font-size:11px;border:none}"),0),
                "5",
                (GetIconLabel("Export","assets/arrowupicon100.png",15,styles.text_style3+"QLabel{font-size:11px;border:none}"),0),
            ],
            Qt.Horizontal
        )
        # linesHeader = GetIconLabel("Customisations :","assets/customizationsicon100.png",15,styles.header_style4+"QLabel{font-size:13px;border:none}")

        self.modelSettingsPanel_layout.addWidget(objectsHeader,0)
        self.modelSettingsPanel_layout.addSpacing(3)
        self.modelSettingsPanel_layout.addWidget(pointsScrollView,1)
        self.modelSettingsPanel_layout.addSpacing(5)
        self.modelSettingsPanel_layout.addWidget(objectFooter,0)
        self.modelSettingsPanel_layout.addSpacing(15)

        self.modelSettingsPanel_layout.addWidget(customisationsHeader,0)
        self.modelSettingsPanel_layout.addWidget(lineScrollView,1)
        self.modelSettingsPanel_layout.addSpacing(5)
        self.modelSettingsPanel_layout.addWidget(bw,0)
        # self.modelSettingsPanel_layout.addSpacing()


        self.modelSettingPanel.setLayout(self.modelSettingsPanel_layout)  


        #================= DOCKS =================#
        self.rendererDock = QDockWidget("3D ModeView", self)
        self.rendererDock.setWidget(self.rendererWidget)
        self.rendererDockTitle = GetIconLabel("3D ModelView","assets/3dviewicon100.png",20,styles.header_style1+"QLabel{font-size:14px;border:none}")
        self.rendererDockTitle.setStyleSheet(f"background-color:{cl.SYS_BG1};border:1px solid {cl.SYS_BD4};border-bottom:none;padding-top:3px;padding-bottom:3px")
        self.rendererDock.setTitleBarWidget(self.rendererDockTitle)
        self.addDockWidget(Qt.RightDockWidgetArea, self.rendererDock)

        self.objectDock = QDockWidget("Model Settings", self)
        self.objectDock.setMinimumWidth(250)
        self.objectDock.setWidget(self.modelSettingPanel)
        self.objectDockTitle = GetIconLabel("Model Settings","assets/3dcubecutouticon100.png",20,styles.header_style1+"QLabel{font-size:14px;border:none}")
        self.objectDockTitle.setStyleSheet(f"background-color:{cl.SYS_BG1};border:1px solid {cl.SYS_BD4};padding-top:3px;padding-bottom:3px")
        self.objectDock.setTitleBarWidget(self.objectDockTitle)
        self.addDockWidget(Qt.RightDockWidgetArea, self.objectDock)
        self.objectDock.setFeatures(QDockWidget.NoDockWidgetFeatures)

        self.splitDockWidget(self.rendererDock, self.objectDock, Qt.Horizontal)

        self.quickActionDock = QDockWidget("Quick Actions", self)
        self.quickActionDock.setWidget(self.quickEditPanel)
        self.quickActionDock.setTitleBarWidget(QWidget())
        self.quickEditPanel.setFixedHeight(50)
        self.addDockWidget(Qt.RightDockWidgetArea, self.quickActionDock)

        self.splitDockWidget(self.rendererDock, self.quickActionDock, Qt.Vertical)

        self.toolbarDock = QDockWidget("Tools", self)
        self.toolbarDock.setWidget(self.toolBar)
        self.toolbarDock.setTitleBarWidget(QWidget())
        self.toolbarDock.setFeatures(QDockWidget.NoDockWidgetFeatures)
        self.toolbarDock.setFixedWidth(40)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.toolbarDock)

        QTimer.singleShot(0, lambda: self.resizeDocks(
            [self.rendererDock, self.objectDock],
            [self.width() * 0.75, self.width() * 0.25],
            Qt.Horizontal
        ))

        QTimer.singleShot(0, lambda: self.resizeDocks(
            [self.rendererDock, self.quickActionDock],
            [self.height() * 0.9, self.height() * 0.1],
            Qt.Vertical
        ))

        

        #================================================#


        #================ CONNECTORS ====================#
        self.addPointButton.setShortcut(Qt.Key_Return)
        self.addPointButton.clicked.connect(self.addPoint)

        self.addpointTool.mousePressEvent = self.addPoint
        self.multiplepointsTool.mousePressEvent = self.addMultiplePoints
        self.lineTool.mousePressEvent = self.addLine
        self.linePointTool.mousePressEvent = self.addPointsAlongLine
        self.surfaceTool.mousePressEvent = self.addSurface
        self.sensorTool.mousePressEvent = self.addSensor
        self.borderTool.mousePressEvent = self.borderSelectedPoints

        self.togglevibrationicon.mousePressEvent = self.toggleVibration

        self.objectsCombo.currentTextChanged.connect(self.loadObjects)

        self.update_btn.clicked.connect(self.updateCustmoisations)

        self.xyaxisIcon.mousePressEvent = lambda event: self.renderer.showXYView()
        self.yzaxisIcon.mousePressEvent = lambda event: self.renderer.showYZView()
        self.zxaxisIcon.mousePressEvent = lambda event: self.renderer.showZXView()
        self.isometricIcon.mousePressEvent = lambda event: self.renderer.showIsometric()
        
        self.rightIcon.mousePressEvent = lambda event: self.renderer.turn90Right()
        self.leftIcon.mousePressEvent = lambda event: self.renderer.turn90Left()
        self.fitViewIcon.mousePressEvent = lambda event : self.renderer.fitToView()
        self.snapshotIcon.mousePressEvent = lambda event : self.takeSnapShot()

        self.new3dmodelIcon.mousePressEvent = self.createNewModel
        self.savefileIcon.mousePressEvent = lambda event : self.saveFile()
        self.openfileIcon.mousePressEvent = lambda event : self.loadModel()
        self.deleteModelIcon.mousePressEvent = lambda event : self.deleteFile()
        self.viewOnlyIcon.mousePressEvent = self.viewOnlyMode

        self.selectAllBtn.mousePressEvent = self.selectAll
        self.deleteObjectsBtn.mousePressEvent = self.clearSelection
        self.clearSelectionsBtn.mousePressEvent = self.deleteSelections

        self.sectionIcon.mousePressEvent = self.addSectionalPoint
        self.pointsBwPointsIcon.mousePressEvent = self.addEquallySpacedPoints
        self.mirroIcon.mousePressEvent = self.createSurfaceCopies
        self.rulerIcon.mousePressEvent = self.showDistance

        self.renderer.pointSelectionChanged.connect(lambda e,c:self.loadObjects())
    
        #================================================#


        #================= INTIALISATIONS =================#
        self.setToolTips()
        self.loadInitialModel()
        #==================================================#
 
    #=================== DRAWING METHODS ===================#
    def addPoint(self,event=None):
        x = self.xi.text()
        y = self.yi.text()
        z = self.zi.text()

        if not any([x, y, z]):
            return
        elif not all([x, y, z]):
            missing_fields = []
            if not x:
                missing_fields.append("X Coordinate not provided")
            if not y:
                missing_fields.append("Y Coordinate not provided")
            if not z:
                missing_fields.append("Z Coordinate not provided")

            message_text ="\n".join(missing_fields)

            dialog = MessageDialog(
                self,
                messageHeading="Incomplete Input",
                message=message_text,
                type=MessageDialog.ERROR_DIALOG
            )
            dialog.exec_()
            self.setStatusText("Incomplete Coordinates","assets/errorstatusicon100.png")
            

        if x!="" and y !="" and z!="":
            self.renderer.addPoint(
                float(self.xi.text()),
                float(self.yi.text()),
                float(self.zi.text())
            )

            self.loadObjects()
            self.clearInputs()

            self.setStatusText(f"Point({x},{y},{z}) Added","assets/tickicon100.png")
    
    def addLine(self,event=None):
        selected_points = len(self.renderer.selectedPoints)
        if selected_points != 2:
            d = MessageDialog(self,"Invalid Number of Points",f"Number of Points Selected : {selected_points}\nTo Draw a line,select only 2 points",type=MessageDialog.ERROR_DIALOG)
            d.exec()
            return
        self.renderer.connectSelectedPoints()
        self.loadObjects()

    def addPointsAlongLine(self,event=None):
        points_dialog = InputDialog(title="Add Points Along Line",prompt="Number of Points to Add :",placeholder="Enter Integer")
        points , ok = points_dialog.getInput()
        if not ok:
            return 
        self.renderer.drawPointsAlongLine(int(points))
        self.loadObjects()
    
    def addSurface(self,event=None):
        selected_points = len(self.renderer.selectedPoints)
        if selected_points < 3:
            d = MessageDialog(self,"Insufficient Number of Points",f"Number of Points Selected : {selected_points}\nTo Draw a Surface,select 3 or more Points",type=MessageDialog.ERROR_DIALOG)
            d.exec()
            return
        self.renderer.drawSurfaceFromSelection()
        self.loadObjects()

    def addSensor(self,event=None):
        self.renderer.addSensor(
            float(self.xi.text()),
            float(self.yi.text()),
            float(self.zi.text())
        )
        self.loadObjects()
        self.clearInputs()

    def addMultiplePoints(self,event=None):
        num_points = InputDialog(title="Add Multiple Points",prompt="Number of Points to Add :",placeholder="Enter Integer",ok_text="Next",cancel_text="Cancel")
        points , ok = num_points.getInput()
        if not ok or ok == None:
            return 
        d = MultiplePointsDialog(points=int(points))
        points_ ,ok= d.getInput()
        if not ok or ok == None:
            return

        self.renderer.drawMultiplePoints(points_)
        self.loadObjects()

    def editPoint(self,idx):
        x = self.renderer.points[idx].x
        y = self.renderer.points[idx].y
        z = self.renderer.points[idx].z
        dialog = EditPointDialog(title="Edit Point",initial=[x,y,z])

        coords,ok = dialog.getInput()
        if ok:
            self.renderer.points[idx]=Point(coords[0],coords[1],coords[2]) 
            self.renderer.updatePlot()
            self.loadObjects()

    def loadPoint(self,name,x,y,z,handle_stretch=True,index=0,selected=False):
        i = GetIconLabel(name, "assets/pointicon100.png", 15, styles.text_style3)
        g = GetIconLabel(f"x:{x:.2f}  y:{y:.2f}  z:{z:.2f}", "assets/gridicon100.png", 15, styles.text_style3)

        b = QCheckBox()
        b.setChecked(True)

        e = GetIcon("assets/pencilicon100.png", 12)
        c = GetIcon("assets/cancelicon100.png", 18)
        e.mousePressEvent = lambda event : self.editPoint(index)
        c.mousePressEvent = lambda event: self.deletePoint(index)

        #============================ IMPORTANT ============================#
        w = GetBoxWidget([
                (GetBoxWidget([(i,1),(g,1)],Qt.Vertical,align=False,spacing=2),0),
                1,(b,0),"1",(e,0),"2",(c,0)
            ],
            Qt.Horizontal,contentMargins=(7,5,7,5),spacing=3
        )
        w.setCursor(Qt.PointingHandCursor)
        w.setProperty("selected", selected)
        def on_point_widget_click(event):
            if not w.property("selected"):
                w.setStyleSheet(f"border: 1px solid {cl.SYS_TH_BG1}")
                self.renderer.selectedPoints.append(index)
                w.setProperty("selected", True)
                self.renderer.updatePlot(points_only=True)
            else:
                w.setStyleSheet(f"QWidget:hover{{border: 1px solid {cl.SYS_BD4};border-right:none;border-left:none}}")
                self.renderer.selectedPoints.remove(index)
                w.setProperty("selected", False)
                self.renderer.updatePlot(points_only=True)
            self.selectionText.setText(f"Total Points Selected : {len(self.renderer.selectedPoints)}")
        if selected:
            w.setStyleSheet(f"border: 1px solid {cl.SYS_TH_BG1}")
        else:
            w.setStyleSheet(f"QWidget:hover{{border: 1px solid {cl.SYS_BD4};border-right:none;border-left:none}}")
        w.mousePressEvent = on_point_widget_click
        b.setStyleSheet("border:none")
        #===================================================================#

        if handle_stretch == True:
            # Remove existing stretch if present (usually the last item)
            count = self.objectsWidget_layout.count()
            if count > 0:
                last_item = self.objectsWidget_layout.itemAt(count - 1)
                if last_item.spacerItem():
                    item = self.objectsWidget_layout.takeAt(count - 1)
                    del item  # Optional: help GC

            self.objectsWidget_layout.addWidget(w)
            self.objectsWidget_layout.addStretch(1)
        else:
            self.objectsWidget_layout.addWidget(w)

    def loadLine(self,name,p1,p2,handle_stretch = True,index=0):
        i = GetIconLabel(name, "assets/linetoolicon100.png", 15, styles.text_style3)
        g = QLabel(f"({p1.x} , {p1.y} , {p1.z}) → ({p2.x} , {p2.y} , {p2.z})")
        g.setStyleSheet(styles.text_style3)

        b = QCheckBox()
        b.setChecked(True)

        e = GetIcon("assets/pencilicon100.png", 12)
        c = GetIcon("assets/cancelicon100.png", 18)

        w = GetBoxWidget([
                (GetBoxWidget([(i,1),(g,1)],Qt.Vertical,align=False,spacing=2),0),
                1,(b,0),"1",(e,0),"2",(c,0)
            ],
            Qt.Horizontal,contentMargins=(7,5,7,5),spacing=3
        )
        w.setCursor(Qt.PointingHandCursor)
        c.mousePressEvent = lambda event: self.deleteLine(index)

        if handle_stretch == True:
            # Remove existing stretch if present (usually the last item)
            count = self.objectsWidget_layout.count()
            if count > 0:
                last_item = self.objectsWidget_layout.itemAt(count - 1)
                if last_item.spacerItem():
                    item = self.objectsWidget_layout.takeAt(count - 1)
                    del item  # Optional: help GC

            self.objectsWidget_layout.addWidget(w)
            self.objectsWidget_layout.addStretch(1)
        else:
            self.objectsWidget_layout.addWidget(w)

    def loadSensor(self,name,x,y,z,handle_stretch=True,index=0,selected=False):
        i = GetIconLabel(name, "assets/sensoricon60.png", 15, styles.text_style3)
        g = GetIconLabel(f"x:{x:.2f}  y:{y:.2f}  z:{z:.2f}", "assets/gridicon100.png", 15, styles.text_style3)

        b = QCheckBox()
        b.setChecked(True)

        e = GetIcon("assets/pencilicon100.png", 12)
        c = GetIcon("assets/cancelicon100.png", 18)
        c.mousePressEvent = lambda event: self.deleteSensor(index)

        #============================ IMPORTANT ============================#
        w = GetBoxWidget([
                (GetBoxWidget([(i,1),(g,1)],Qt.Vertical,align=False,spacing=2),0),
                1,(b,0),"1",(e,0),"2",(c,0)
            ],
            Qt.Horizontal,contentMargins=(7,5,7,5),spacing=3
        )
        w.setCursor(Qt.PointingHandCursor)
        w.setProperty("selected", selected)
        def on_point_widget_click(event):
            if not w.property("selected"):
                self.renderer.selectedSensor = index
                w.setStyleSheet(f"border: 1px solid {cl.SYS_TH_BG1};border-right:none;border-left:none")
                w.setProperty("selected", True)
                self.renderer.updatePlot()
            else:
                self.renderer.selectedSensor = -1
                w.setStyleSheet(f"QWidget:hover{{border: 1px solid {cl.SYS_BD4};border-right:none;border-left:none}}")
                w.setProperty("selected", False)
                self.renderer.updatePlot()
        if selected:
            w.setStyleSheet(f"border: 1px solid {cl.SYS_TH_BG1}")
        else:
            w.setStyleSheet(f"QWidget:hover{{border: 1px solid {cl.SYS_BD4}}}")
        w.mousePressEvent = on_point_widget_click
        b.setStyleSheet("border:none")
        #===================================================================#

        if handle_stretch == True:
            # Remove existing stretch if present (usually the last item)
            count = self.objectsWidget_layout.count()
            if count > 0:
                last_item = self.objectsWidget_layout.itemAt(count - 1)
                if last_item.spacerItem():
                    item = self.objectsWidget_layout.takeAt(count - 1)
                    del item  # Optional: help GC

            self.objectsWidget_layout.addWidget(w)
            self.objectsWidget_layout.addStretch(1)
        else:
            self.objectsWidget_layout.addWidget(w)

    def loadSurface(self,name,handle_stretch=True):        
        i = GetIconLabel(name, "assets/surfaceicon100.png", 15, styles.text_style3)

        b = QCheckBox()
        b.setChecked(True)

        e = GetIcon("assets/pencilicon100.png", 12)
        c = GetIcon("assets/cancelicon100.png", 18)

        w = GetBoxWidget([
                (i,0),1,(b,0),"1",(e,0),"2",(c,0)
            ],
            Qt.Horizontal,contentMargins=(7,5,7,5),spacing=3
        )
        w.setCursor(Qt.PointingHandCursor)

        if handle_stretch == True:
            # Remove existing stretch if present (usually the last item)
            count = self.objectsWidget_layout.count()
            if count > 0:
                last_item = self.objectsWidget_layout.itemAt(count - 1)
                if last_item.spacerItem():
                    item = self.objectsWidget_layout.takeAt(count - 1)
                    del item  # Optional: help GC

            self.objectsWidget_layout.addWidget(w)
            self.objectsWidget_layout.addStretch(1)
        else:
            self.objectsWidget_layout.addWidget(w)

    def loadObjects(self,event=None):
        while self.objectsWidget_layout.count():
            child = self.objectsWidget_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if self.objectsCombo.text() == "Points":
            points = self.renderer.points
            total = len(points)
            for i in range(0,total):
                point = points[i]
                self.loadPoint(f"Point{i}",point.x,point.y,point.z,index=i,selected=(i in self.renderer.selectedPoints))
            self.selectionText.setText(f"Total Points Selected : {len(self.renderer.selectedPoints)}")

        elif self.objectsCombo.text() == "Lines":
            lines = self.renderer.lines
            total = len(lines)
            for i in range(0,total):
                line = lines[i]
                p1 = line.point1
                p2 = line.point2
                self.loadLine(f"Line{i}",p1,p2,False,index=i)
            self.selectionText.setText(f"Total Lines Selected : {len(self.renderer.selectedLines)}")

        elif self.objectsCombo.text() == "Surfaces":
            points = self.renderer.surfaces
            total = len(points)
            for i in range(0,len(points)):
                point = points[i]
                self.loadSurface(f"Surface{i}",False)
            self.selectionText.setText(f"Total Surfaces Selected : {len(self.renderer.selectedSurfaces)}")

        elif self.objectsCombo.text() == "Sensors":
            points = self.renderer.sensors
            total = len(points)
            for i in range(0,len(points)):
                point = points[i]
                self.loadSensor(f"Sensor{i}",point.x,point.y,point.z,index=i,selected=(i == self.renderer.selectedSensor))
            self.selectionText.setText(f"")


        self.objectsWidget_layout.addStretch(1)

    def deletePoint(self,index):
        self.renderer.deletePoint(index)
        self.loadObjects()

    def deleteLine(self,index):
        self.renderer.deleteLine(index)
        self.loadObjects()

    def deleteSensor(self,index):
        self.renderer.deleteSensor(index)
        self.loadObjects()

    def selectAll(self,event = None):
        objects = self.objectsCombo.text()
        if objects == "Points":
            self.renderer.selectedPoints = list(range(0,len(self.renderer.points)))
            self.renderer.updatePlot(points_only=True)   

        self.loadObjects() 

    def deleteSelections(self, event=None):
        objects = self.objectsCombo.text()
        if objects == "Points":
            for i in sorted(self.renderer.selectedPoints, reverse=True): 
                self.renderer.deletePoint(i,False)
        self.renderer.updatePlot()
        self.loadObjects()

    def clearSelection(self,event=None):
        objects = self.objectsCombo.text()
        if objects == "Points":
            self.renderer.selectedPoints.clear()
            self.renderer.updatePlot(points_only=True)   
        if objects == "Sensors":
            self.renderer.selectedSensor = -1   
            self.renderer.updatePlot()  

        self.loadObjects() 

    #=======================================================#


    #=============== FILE I/O ================#
    def saveFile(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save Model File",
            self.currentFile,
            "MODEL Files (*.model);;All Files (*)"
        )
        if not file_path:
            return  # User canceled

        if file_path != self.currentFile:
            old_path = self.currentFile
            new_path = file_path

            if os.path.exists(old_path):
                os.remove(old_path)

            current_tab = self.renderer_tab.currentTab()
            current_tab.setText(Path(new_path).name)
            current_tab.setRouteKey(new_path)

            if old_path in self.renderer_tab.itemMap:
                self.renderer_tab.itemMap[new_path] = self.renderer_tab.itemMap.pop(old_path)

            self.files[new_path] = self.files[old_path]
            self.files[new_path]["path"] = new_path
            del self.files[old_path]

            self.currentFile = new_path
        else:
            self.currentFile = file_path

        self.renderer.saveModel(self.currentFile)

    def loadModel(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Open Model File",
            "",
            "MODEL Files (*.model);;All Files (*)"
        )
        if not file_path:
            return  # User canceled
        
        self.renderer_tab.addTab(file_path,str(Path(file_path).name))
        self.renderer_tab.setCurrentTab(file_path)
        self.renderer_tab.currentTab().setFixedHeight(25)
        
        self.files[self.currentFile]["camera"] = self.renderer.plotter.camera_position
        self.renderer.saveModel(self.currentFile)
        self.renderer.loadModel(file_path)
        self.loadObjects()
        self.renderer.plotter.view_isometric()
        self.files[file_path]={
            "path":file_path,
            "saved":True,
            "camera":self.renderer.plotter.camera_position
        }
        self.currentFile = file_path

    def takeSnapShot(self):
        filename, _ = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save Snapshot",
            filter="PNG Image (*.png);;JPEG Image (*.jpg);;All Files (*)",
            options=QFileDialog.Options()
        )
        if filename:
            self.renderer.takeSnapshot(filename)

    def writeEmptyModelFile(self,file_path:str):
        file_contents = """{
    "points": [],
    "lines": [],
    "surfaces": [],
    "sensors": [],
    "metadata": {
        "created": "2025-06-24T00:27:34.170908",
        "numPoints": 13,
        "numLines": 20,
        "numSurfaces": 7,
        "numSensors": 0
    }
}"""
        path = Path(file_path)
        path.write_text(file_contents)
        
    def loadInitialModel(self):
        desktop = Path.home() 
        file_path = desktop / "Projects"
        file_path /= "Vision3D"
        file_path /= "3DModels"
        file_path /= "Untitled.model"
        self.writeEmptyModelFile(file_path)

        self.renderer.loadModel(str(file_path))
        self.loadObjects()

        self.files[str(file_path)] = {
            "path":str(file_path),
            "saved":True,
            "camera":self.renderer.plotter.camera_position
        }

        self.renderer_tab.addTab(str(file_path),"Untitled.model")
        self.renderer_tab.currentTab().setFixedHeight(25)

        self.currentFile = str(file_path)

    def tabChanged(self,i):
        self.files[self.currentFile]["camera"] = self.renderer.plotter.camera_position
        self.renderer.saveModel(self.currentFile)
        file_path = self.renderer_tab.tabItem(i).routeKey()
        self.renderer.loadModel(file_path)
        self.loadObjects()
        self.currentFile = file_path
        self.renderer.plotter.camera_position = self.files[file_path]["camera"]

    def createNewModel(self,event=None):
        self.files[self.currentFile]["camera"] = self.renderer.plotter.camera_position
        self.renderer.saveModel(self.currentFile)
        dialog = NewModelDialog()
        f , ok = dialog.getInput()
        if ok == True:
            file_name = f[0]
            folder = f[1]
            if not file_name.endswith(".model"):
                file_name += ".model"
            path = os.path.join(folder,file_name)
            if os.path.exists(path):
                d = MessageDialog(self,"File Already Exists",f"The file:\n\"{path}\"\nalready exists.\n\nPlease choose a different name or folder.",type=MessageDialog.WARNING_DIALOG)
                d.exec()
                return

            self.writeEmptyModelFile(path)
            self.renderer.loadModel(path)
            self.loadObjects()
            self.renderer_tab.addTab(path,file_name)
            self.renderer_tab.setCurrentTab(path)
            self.renderer_tab.currentTab().setFixedHeight(25)
            self.renderer.plotter.view_isometric()
            self.files[path] = {
                "path":path,
                "saved":True,
                "camera":self.renderer.plotter.camera_position
            }
            self.currentFile = path

    def closeFile(self,i,delete=False):
        path = self.renderer_tab.tabItem(i).routeKey()
        self.renderer_tab.removeTab(i)
        if delete:
            os.remove(path)
        del self.files[path]
        if self.renderer_tab.currentTab():
            path = self.renderer_tab.currentTab().routeKey()
            self.currentFile = path
            self.renderer.loadModel(path)
            self.loadObjects()  
            self.renderer.plotter.camera_position = self.files[path]["camera"]
        else:
            self.loadInitialModel()
    
    def deleteFile(self):
        self.closeFile(self.renderer_tab.currentIndex(),delete=True)
       

    #=========================================#


    #=================== UTILARY METHODS ===================#

    def viewOnlyMode(self,event=None):
        if self.viewOnly != True:
            self.objectDock.hide()
            self.quickActionDock.hide()
            self.toolbarDock.hide()
            self.viewOnly = True
            self.viewOnlyIcon.updateIconText("assets/fullscreenicon100.png","Focus:ON")
        else:
            self.objectDock.show()
            self.quickActionDock.show()
            self.toolbarDock.show()
            self.viewOnly = False
            self.viewOnlyIcon.updateIconText("assets/fullscreenofficon100.png","Focus:OFF")

        QTimer.singleShot(0, lambda: self.resizeDocks(
            [self.rendererDock, self.objectDock],
            [self.width() * 0.75, self.width() * 0.25],
            Qt.Horizontal
        ))

        QTimer.singleShot(0, lambda: self.resizeDocks(
            [self.rendererDock, self.quickActionDock],
            [self.height() * 0.9, self.height() * 0.1],
            Qt.Vertical
        ))

    def clearInputs(self):
        self.xi.clear()
        self.yi.clear()
        self.zi.clear()
        self.xi.setFocus()
    
    def toggleVibration(self, event=None):
        if not self.vibrating:
            self.renderer.startVibration()
            self.vibrating = True
            self.togglevibrationicon.updateIconText("assets/sonometercancelicon100.png", "Stop\nVibrations")
        else:
            self.renderer.stopVibration(restore_original=self.vib_og_surface.isChecked())
            self.vibrating = False
            self.togglevibrationicon.updateIconText("assets/sonometericon100.png", "Start\nVibrations")

    def setupCustomisations(self):
        #Color Pickers
        self.point_cp = ColorPickerButton(QColor(255, 0, 0), self.customisationsWidget)
        self.point_s_cp = ColorPickerButton(QColor(0, 0, 255), self.customisationsWidget)
        self.line_cp = ColorPickerButton(QColor(0, 255, 0), self.customisationsWidget)
        self.line_s_cp = ColorPickerButton(QColor(255, 0, 0), self.customisationsWidget)
        self.sensor_cp = ColorPickerButton(QColor(255, 255, 0), self.customisationsWidget)
        self.sensor_s_cp = ColorPickerButton(QColor(0, 255, 0), self.customisationsWidget)
        self.surface_cp = ColorPickerButton(QColor("#27fd05"), self.customisationsWidget)
        self.surface_s_cp = ColorPickerButton(QColor("#fdb305"), self.customisationsWidget)
        self.surface_edge_cp = ColorPickerButton(QColor("#ffffff"), self.customisationsWidget)


        #======= DISPLAY SETTING =======#
        
        #Opacity
        self.opac_l , self.opac_i = GetLabelLineEdit("Surface Opacity","Enter Decimal [0.00-1.00]",styles.text_style3)
        self.opac_i.setFixedHeight(25)
        self.opac_i.setText("0.60")

        #Point Size
        self.pointsize_l , self.pointsize_i = GetLabelLineEdit("Point Size","Enter Integer",styles.text_style3)
        self.pointsize_i.setFixedHeight(25)
        self.pointsize_i.setText("10")

        #Sensor Size
        self.sensorsize_l , self.sensorsize_i = GetLabelLineEdit("Sensor Size","Enter Integer",styles.text_style3)
        self.sensorsize_i.setFixedHeight(25)
        self.sensorsize_i.setText("10")

        #Line Width
        self.linewidth_l , self.linewidth_i = GetLabelLineEdit("Line Width","Enter Integer",styles.text_style3)
        self.linewidth_i.setFixedHeight(25)
        self.linewidth_i.setText("3")

        #Surface Edges
        self.edge_chbx = QCheckBox("Surface Edges")
        self.edge_chbx.setStyleSheet(styles.checkbox_style1+"QCheckBox{border:none;outline:none}")
        self.edge_chbx.setChecked(True)

        #===============================#

        #======= VIBRATION SETTINGS =======#
        self.vib_amplitude_l , self.vib_amplitude_i = GetLabelLineEdit("Amplitude","Enter Decimal",styles.text_style3)
        self.vib_amplitude_i.setFixedHeight(25)
        self.vib_amplitude_i.setText("0.05")

        self.vib_freq_l , self.vib_freq_i = GetLabelLineEdit("Frequency","Enter Hz",styles.text_style3)
        self.vib_freq_i.setFixedHeight(25)
        self.vib_freq_i.setText("2")

        self.vib_x_inf_l , self.vib_x_inf_i = GetLabelLineEdit("X Influence","Enter Decimal",styles.text_style3)
        self.vib_x_inf_i.setFixedHeight(25)
        self.vib_x_inf_i.setText("0.5")

        self.vib_y_inf_l , self.vib_y_inf_i = GetLabelLineEdit("Y Influence","Enter Decimal",styles.text_style3)
        self.vib_y_inf_i.setFixedHeight(25)
        self.vib_y_inf_i.setText("0.5")

        self.vib_spd_l , self.vib_spd_i = GetLabelLineEdit("Vibration Speed","Enter Integer [10-200]",styles.text_style3)
        self.vib_spd_i.setFixedHeight(25)
        self.vib_spd_i.setText("50")

        self.vib_og_surface = QCheckBox("Restore Original Surface")
        self.vib_og_surface.setStyleSheet(styles.checkbox_style1+"QCheckBox{border:none;outline:none}")
        self.vib_og_surface.setChecked(False)
        #==================================#



        sep1 = LabeledHorizontalLine(label="Display Settings",color=cl.SYS_BG8)
        sep2 = LabeledHorizontalLine(label="Vibrations Settings",color=cl.SYS_BG8)
        sep3 = LabeledHorizontalLine(label="Colors Settings",color=cl.SYS_BG8)


        self.customisationsWidget_layout.addWidget(sep1)
        self.customisationsWidget_layout.addSpacing(5)
        for i in [
            (self.opac_i,self.opac_l),
            (self.pointsize_i,self.pointsize_l),
            (self.sensorsize_i,self.sensorsize_l),
            (self.linewidth_i,self.linewidth_l),
        ]:
            label = i[1]
            label.setStyleSheet(styles.text_style3)

            semicolon = QLabel(":")
            semicolon.setStyleSheet(styles.text_style3)

            i[0].setFixedHeight(20)
            label.setFixedWidth(100)

            w = GetBoxWidget(
                [(label,0),"5",(semicolon,0),"7",(i[0],1)],
                Qt.Horizontal
            )

            self.customisationsWidget_layout.addWidget(w,0)
            self.customisationsWidget_layout.addSpacing(5)
        
        self.customisationsWidget_layout.addWidget(self.edge_chbx)


        self.customisationsWidget_layout.addWidget(sep2)
        self.customisationsWidget_layout.addSpacing(5)
        for i in [
            (self.vib_amplitude_i,self.vib_amplitude_l),
            (self.vib_freq_i,self.vib_freq_l),
            (self.vib_x_inf_i,self.vib_x_inf_l),
            (self.vib_y_inf_i,self.vib_y_inf_l),
            (self.vib_spd_i,self.vib_spd_l),
        ]:
            label = i[1]
            label.setStyleSheet(styles.text_style3)

            semicolon = QLabel(":")
            semicolon.setStyleSheet(styles.text_style3)

            i[0].setFixedHeight(20)
            label.setFixedWidth(100)

            w = GetBoxWidget(
                [(label,0),"5",(semicolon,0),"7",(i[0],1)],
                Qt.Horizontal
            )

            self.customisationsWidget_layout.addWidget(w,0)
            self.customisationsWidget_layout.addSpacing(5)

        self.customisationsWidget_layout.addWidget(self.vib_og_surface)


        
        self.customisationsWidget_layout.addWidget(sep3)
        for c in [
            (self.point_cp,QLabel("Point Color")),
            (self.point_s_cp,QLabel("Point Selected Color")),
            (self.line_cp,QLabel("Line Color")),
            (self.line_s_cp,QLabel("Line Selected Color")),
            (self.sensor_cp,QLabel("Sensor Color")),
            (self.sensor_s_cp,QLabel("Sensor Selected Color")),
            (self.surface_cp,QLabel("Surface Color")),
            (self.surface_s_cp,QLabel("Surface Selected Color")),
            (self.surface_edge_cp,QLabel("Surface Edge Color")),
        ]:
            label = c[1]
            label.setStyleSheet(styles.text_style3)
            label.setFixedWidth(150)

            c[0].setFixedHeight(15)
            c[0].setFixedWidth(70)

            semicolon = QLabel(":")
            semicolon.setStyleSheet(styles.text_style3)

            w = GetBoxWidget(
                [(label,0),"5",(semicolon,0),"5",(c[0],2)],
                Qt.Horizontal
            )


            self.customisationsWidget_layout.addWidget(w,0)
            self.customisationsWidget_layout.addSpacing(5)


        self.customisationsWidget_layout.addStretch(1)

    def updateCustmoisations(self,event=None):
        #Colors
        self.renderer.pointColor = self.point_cp.color().getRgb()[:3]
        self.renderer.pointSelectedColor = self.point_s_cp.color().getRgb()[:3]
        self.renderer.lineColor = self.line_cp.color().getRgb()[:3]
        self.renderer.lineSelectedColor = self.line_s_cp.color().getRgb()[:3]
        self.renderer.sensorColor = self.sensor_cp.color().getRgb()[:3]
        self.renderer.sensorSelectedColor = self.sensor_s_cp.color().getRgb()[:3]
        self.renderer.surfaceColor = self.surface_cp.color().getRgb()[:3]
        self.renderer.surfaceSelectedColor = self.surface_s_cp.color().getRgb()[:3]
        self.renderer.surfaceEdgeColor = self.surface_edge_cp.color().getRgb()[:3]

        #Display
        self.renderer.surfaceOpacity = float(self.opac_i.text())
        self.renderer.pointSize = int(self.pointsize_i.text())
        self.renderer.sensorSize = int(self.sensorsize_i.text())
        self.renderer.lineWidth = int(self.linewidth_i.text())
        self.renderer.showSurfaceEdges = self.edge_chbx.isChecked()

        #Vibrations
        self.renderer.vib_amplitude = float(self.vib_amplitude_i.text())
        self.renderer.vib_frequency = float(self.vib_freq_i.text())
        self.renderer.vib_x_inf = float(self.vib_x_inf_i.text())
        self.renderer.vib_y_inf = float(self.vib_y_inf_i.text())
        self.renderer.vib_speed = float(self.vib_spd_i.text())
        


        self.renderer.updatePlot()

    def createRibbon(self):
        self.new3dmodelIcon = VerticalIconTextButton("assets/new3dmodelicon100.png","New File",font_size=9,size=36,width=60)
        self.openfileIcon = VerticalIconTextButton("assets/3dmodelicon100.png","Open Model",font_size=9,size=35,width=60)
        self.savefileIcon = VerticalIconTextButton("assets/save3dicon100.png","Save Model",font_size=9,size=30,width=60)
        self.savefileAsIcon = VerticalIconTextButton("assets/saveas3dicon100.png","Save As",font_size=9,size=30,width=60)
        self.gltfexportIcon = VerticalIconTextButton("assets/gltficon100.png","Export GLTF",font_size=9,size=30,width=60)
        self.clearAllIcon = VerticalIconTextButton("assets/deleteviewicon100.png","Clear Model",font_size=9,size=27,width=60)
        self.deleteModelIcon = VerticalIconTextButton("assets/binicon100.png","Delete File",font_size=9,size=35,width=60)
        self.viewOnlyIcon = VerticalIconTextButton("assets/fullscreenofficon100.png","Focus:OFF",font_size=9,size=40,width=60)
        self.togglevibrationicon = VerticalIconTextButton("assets/sonometericon100.png","Start\nVibrations",font_size=9,size=25,width=60)
        self.importCSVIcon = VerticalIconTextButton("assets/importcsvicon100.png","Sensor CSV",font_size=9,size=30,width=60)

        self.xyaxisIcon = GetIcon("assets/xyaxisicon100.png",25)
        self.yzaxisIcon = GetIcon("assets/yzaxisicon100.png",25)
        self.zxaxisIcon = GetIcon("assets/zxaxisicon100.png",25)
        self.isometricIcon = GetIcon("assets/isometricviewicon100.png",25)

        self.rightIcon = GetIcon("assets/arrowrighticon100.png",22)
        self.leftIcon = GetIcon("assets/arrowlefticon100.png",22)
        self.fitViewIcon = GetIcon("assets/fitviewicon100.png",20)
        self.snapshotIcon = GetIcon("assets/cameraicon100.png",25)


        self.sectionIcon = GetIcon("assets/dashlineicon100.png",24)
        self.pointsBwPointsIcon = GetIcon("assets/multiplepointsicon100.png",24)
        self.mirroIcon = GetIcon("assets/layericon100.png",24)
        self.paddingIcon = GetIcon("assets/paddingicon100.png",24)
        self.shiftIcon = GetIcon("assets/originicon100.png",24)
        
        self.rulerIcon = GetIcon("assets/rulericon100.png",24)
        self.linerulerIcon = GetIcon("assets/linerulericon100.png",24)
        self.angleIcon = GetIcon("assets/angleicon100.png",24)
        self.intersectIcon = GetIcon("assets/intersecticon100.png",24)
        self.normalIcon = GetIcon("assets/normalicon100.png",24)



        sep1 = SeparatorLine(orientation="V",length=75)
        sep2 = SeparatorLine(orientation="V",length=75)
        sep3 = SeparatorLine(orientation="V",length=75)
        sep4 = SeparatorLine(orientation="V",length=75)


    
        self.viewOptions = GetBoxWidget(
            [
                (GetBoxWidget([
                    (self.xyaxisIcon,0),
                    (self.yzaxisIcon,0),
                    (self.zxaxisIcon,0),
                    (self.isometricIcon,0),
                ],Qt.Horizontal,spacing=12),1),
                (GetBoxWidget([
                    (self.leftIcon,0),
                    (self.rightIcon,0),
                    "5",
                    (self.fitViewIcon,0),
                    "5",
                    (self.snapshotIcon,0),
                ],Qt.Horizontal,spacing=12),1),
            ],
            Qt.Vertical,
            spacing=10,
            contentMargins=(0,10,0,0)
        )

        self.geometryOptions = GetBoxWidget([
            (GetBoxWidget([
                (self.sectionIcon,0),
                "-2",
                (self.pointsBwPointsIcon,0),
                (self.mirroIcon,0),
                (self.paddingIcon,0),
                (self.shiftIcon,0),
            ],Qt.Horizontal,spacing=5),1),
            (GetBoxWidget([
                (self.rulerIcon,0),
                "2",
                (self.linerulerIcon,0),
                (self.angleIcon,0),
                (self.intersectIcon,0),
                (self.normalIcon,0),
            ],Qt.Horizontal,spacing=5),1)
        ],
            Qt.Vertical,
            spacing=10,
            contentMargins=(0,10,0,0)
        )


        self.ribbon = GetBoxWidget(
            [
                "5",
                (self.new3dmodelIcon,0),
                (self.openfileIcon,0),
                "3",
                (self.savefileIcon,0),
                (self.importCSVIcon,0),
                "3",
                (self.gltfexportIcon,0),
                "5",
                (self.clearAllIcon,0),
                (self.deleteModelIcon,0),
                "5",
                (sep1,1),
                "10",
                (self.viewOptions,0),
                "10",
                (sep2,1),
                "5",
                (self.geometryOptions,0),
                "5",
                (sep4,0),
                "5",
                (self.viewOnlyIcon,0),
                (self.togglevibrationicon,0),
                1
            ],
            Qt.Horizontal,
            contentMargins=(10,5,10,10)
        )

        self.setMenuWidget(self.ribbon)

    def setToolTips(self):

        self.addpointTool.setToolTip(getTooltipHTML("Point Tool","Add a Point in the Model by entering Coordinates in the\nQuick Actions Panel"))
        self.lineTool.setToolTip(getTooltipHTML("Line Tool","Connect Two Points with a Line.\nMake Sure Exactly 2 Points are Selected"))
        self.linePointTool.setToolTip(getTooltipHTML("Point Line Tool","Add points along a Selected Line"))
        self.multiplepointsTool.setToolTip(getTooltipHTML("Multiple Points Tool","Add Multiple Points at Once to the Model"))
        self.borderTool.setToolTip(getTooltipHTML("Border Tool","Connect Coplanar in Sequential Order.\nMake Sure 3 or more Coplanar Points are Selected"))
        self.surfaceTool.setToolTip(getTooltipHTML("Surface Tool","Create a Surface in the Model.\nMake Sure 3 or more Points are Selected"))
        self.sensorTool.setToolTip(getTooltipHTML("Sensor Tool","Add a Sensor in the Model by entering Coordinates in the\nQuick Actions Panel"))

        self.xyaxisIcon.setToolTip(getTooltipHTML("XY View","Display Model in the XY Plane"))
        self.yzaxisIcon.setToolTip(getTooltipHTML("YZ View","Display Model in the YZ Plane"))
        self.zxaxisIcon.setToolTip(getTooltipHTML("ZX View","Display Model in the ZX Plane"))
        self.isometricIcon.setToolTip(getTooltipHTML("Isometric View","Display Model from Isomteric Perpective"))
        self.rightIcon.setToolTip(getTooltipHTML("90 Degree Right","Turn the Model by 90 degrees in anitclockwise direction"))
        self.leftIcon.setToolTip(getTooltipHTML("90 Degree Left","Turn the Model by 90 degrees in clockwise direction"))
        self.fitViewIcon.setToolTip(getTooltipHTML("Fit View","Scale the Model to Fit in Current View"))
        self.snapshotIcon.setToolTip(getTooltipHTML("Snapshot","Capture Snapshot of the Model in Current View and Save as *.png file"))

        self.sectionIcon.setToolTip(getTooltipHTML("Sectional Point Tool","Apply Section Formula on 2 Selected Points"))
        self.pointsBwPointsIcon.setToolTip(getTooltipHTML("Insert Points Tool","Insert Points between 2 Selected Points"))
        self.rulerIcon.setToolTip(getTooltipHTML("Distance Tool","Measure Distance between Selected Object"))
        self.mirroIcon.setToolTip(getTooltipHTML("Surface Copy Tool","Create Surface Copies from a set of Coplanar Points,Each Surface Separated by a Specified Distance"))

        self.selectAllBtn.setToolTip(getTooltipHTML("Select All","All Object of this type will be Selected"))
        self.deleteObjectsBtn.setToolTip(getTooltipHTML("Clear Selections","All Selected Objects will be\nDe-Selected"))

    def setStatusText(self,message,icon):
        self.statusText.setText(message)
        icon = QIcon(icon)
        pixmap = icon.pixmap(20, 20)
        self.statusIcon.setPixmap(pixmap)

    def eventFilter(self, obj, event):
        if event.type() == QEvent.KeyPress:
            key = event.key()
            
            if key == Qt.Key_Right:
                cursor_pos = obj.cursorPosition()
                text_length = len(obj.text())
                if cursor_pos == text_length:
                    if obj == self.xi:
                        self.yi.setFocus()
                    elif obj == self.yi:
                        self.zi.setFocus()
                    return True  # prevent default if desired

            elif key == Qt.Key_Left:
                cursor_pos = obj.cursorPosition()
                text_length = len(obj.text())
                if cursor_pos == text_length:
                    if obj == self.zi:
                        self.yi.setFocus()
                    elif obj == self.yi:
                        self.xi.setFocus()
                    return True

        return super().eventFilter(obj, event)
   
    #=======================================================#


    #===================== Geometry Tools =====================#

    def addSectionalPoint(self,event = None):
        if len(self.renderer.selectedPoints) != 2:
            d = MessageDialog(self,"Invalid Number of Points",f"Number of Points Selected : {len(self.renderer.selectedPoints)}\nTo Apply Section Formula,select exactly 2 points",type=MessageDialog.ERROR_DIALOG)
            d.exec()
            return
        p1_idx = self.renderer.selectedPoints[0]
        p2_idx = self.renderer.selectedPoints[1]

        p1 = self.renderer.points[p1_idx]
        p2 = self.renderer.points[p2_idx]

        dialog = PointSectionDialog(p1=[p1.x,p1.y,p1.z],p2=[p2.x,p2.y,p2.z])
        ratio , ok = dialog.getInput()
        if ok:
            coord = Geometry.sectionFormula([p1.x,p1.y,p1.z],[p2.x,p2.y,p2.z],ratio[0],ratio[1])
            self.renderer.addPoint(coord[0],coord[1],coord[2])
            self.loadObjects()

    def addEquallySpacedPoints(self,event=None):
        if len(self.renderer.selectedPoints) != 2:
            d = MessageDialog(self,"Invalid Number of Points",f"Number of Points Selected : {len(self.renderer.selectedPoints)}\nTo Add Points bewteen Points,select exactly 2 points",type=MessageDialog.ERROR_DIALOG)
            d.exec()
            return
        p1_idx = self.renderer.selectedPoints[0]
        p2_idx = self.renderer.selectedPoints[1]

        p1 = self.renderer.points[p1_idx]
        p2 = self.renderer.points[p2_idx]

        dialog = InputDialog(title="Add Equally Spaced Points",prompt="Number of Points to Add",placeholder="Enter Integer",ok_text="Add Points")
        
        points , ok = dialog.getInput()
        if ok:
            coords = Geometry.insertEquallySpacedPoints([p1.x,p1.y,p1.z],[p2.x,p2.y,p2.z],int(points))
            for point in coords:
                self.renderer.addPoint(point[0], point[1], point[2],update=False)
            self.renderer.updatePlot()
            self.loadObjects()

    def borderSelectedPoints(self,event = None):
        if len(self.renderer.selectedPoints) < 3:
            d = MessageDialog(self,"Insufficient Number of Points",f"Number of Points Selected : {len(self.renderer.selectedPoints)}\nTo create Border , select a 3 or more Coplanar Points",type=MessageDialog.ERROR_DIALOG)
            d.exec()
            return
        
        points = []
        for i in self.renderer.selectedPoints:
            point = self.renderer.points[i]
            points.append([point.x,point.y,point.z])

        self.drawBorder(points)

    def drawBorder(self,points,update=True):
        order = Geometry.connectCoplanarPoints3D(points)
        for l in order:
            p1_l = l[0]
            p2_l = l[1]

            p1 = Point(p1_l[0],p1_l[1],p1_l[2])
            p2 = Point(p2_l[0],p2_l[1],p2_l[2])
            self.renderer.lines.append(Line(p1,p2))
            if update:
                self.renderer.updatePlot()
                self.loadObjects()
        
    def createSurfaceCopies(self,event=None):
        if len(self.renderer.selectedPoints) < 3:
            d = MessageDialog(self,"Insufficient Number of Points",f"Number of Points Selected : {len(self.renderer.selectedPoints)}\nTo create Copies , select a 3 or more Coplanar Points",type=MessageDialog.ERROR_DIALOG)
            d.exec()
            return

        dialog = SurfaceCopyDialog(title="Create Surface Copies")
        inputs , ok = dialog.getInput()
        if ok:
            points = []
            for i in self.renderer.selectedPoints:
                point = self.renderer.points[i]
                points.append([point.x,point.y,point.z])

            surfaces = Geometry.generateOffsetCopies(points,reps=int(inputs[0]),dist=float(inputs[1]))

            for s in surfaces:
                surfacePoints = []
                for p in s:
                    self.renderer.points.append(Point(p[0],p[1],p[2]))
                    surfacePoints.append(Point(p[0],p[1],p[2]))
                if inputs[4] == True:
                    surface = Surface(surfacePoints)
                    self.renderer.surfaces.append(surface)
                
                if inputs[3] == True:
                    self.drawBorder(s,update=False)
            
            if inputs[2] == True:
                last_surface = surfaces[-1]
                for i in range(0,len(last_surface)):
                    p1 = Point(points[i][0],points[i][1],points[i][2])
                    p2 = Point(last_surface[i][0],last_surface[i][1],last_surface[i][2])
                    self.renderer.lines.append(Line(p1,p2))

            self.renderer.updatePlot()
            self.loadObjects()
                
    def showDistance(self,event = None):
        if len(self.renderer.selectedPoints) != 2:
            d = MessageDialog(self,"Invalid Number of Points",f"Number of Points Selected : {len(self.renderer.selectedPoints)}\nTo Measure Distance,select exactly 2 points",type=MessageDialog.ERROR_DIALOG)
            d.exec()
            return
        
        p1 = self.renderer.points[self.renderer.selectedPoints[0]]
        p2 = self.renderer.points[self.renderer.selectedPoints[1]]
        
        dist = Geometry.distance3D([p1.x,p1.y,p1.z],[p2.x,p2.y,p2.z])

        d = MessageDialog(self,"Measurement",f"Distance between Selected Points is {dist:.4f}",MessageDialog.INFO_DIALOG)
        d.exec()

    #==========================================================#