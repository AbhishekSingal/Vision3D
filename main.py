# ──────────────── Qt Imports ────────────────
from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QGuiApplication
from qfluentwidgets import setTheme,Theme

# ──────────────── System Imports ────────────────
import sys, os

# ──────────────── Project Imports ────────────────
from ModelWindow import ModelWindow
import Styles.styles as styles
import Styles.colors as cl


# DPI and Graphics Settings
QGuiApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
QApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)
QApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)

#Initlialize App
app = QApplication(sys.argv)
app.setStyleSheet(styles.dock_style1)
setTheme(Theme.DARK)



#Platform Specific Settings
if sys.platform == 'darwin':
    import objc
    from AppKit import NSApp, NSAppearance
    os.environ['QT_MAC_WANTS_LAYER'] = '1'
    NSApp.setAppearance_(NSAppearance.appearanceNamed_("NSAppearanceNameDarkAqua"))

if sys.platform == "win32":
    os.environ["QT_QPA_PLATFORM"] = "windows:darkmode=1"


modelWindow = ModelWindow()
modelWindow.show()
sys.exit(app.exec_())