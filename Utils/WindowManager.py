# ──────────────── Project Imports ────────────────
from Windows.DynamicInfoWindow import DynamicInfoWindow
from Windows.LoginWindow import LoginWindow
from Windows.LaunchWindow import LaunchWindow
from Windows.SignalAnalysisWindow import SignalAnalysisWindow
from Windows.LoadingWindow import LoadingWindow
from Windows.NewProjectWindow import NewProjectWindow
from Windows.ModelWindow import ModelWindow

import Styles.styles as styles
import Styles.colors as cl


class WindowManager:
    def __init__(self):
        
        self.loading = LoadingWindow()
        self.loginWindow = LoginWindow()
        self.launchWindow = LaunchWindow()
        self.dynamicInfoWindow = DynamicInfoWindow()
        self.signalAnalysisWindow = SignalAnalysisWindow()
        self.newProjectWindow = NewProjectWindow()
        self.modelWindow = ModelWindow()

        self.loginWindow.loginPanel.button.clicked.connect(self.showLaunchWindow)

        self.launchWindow.launchPanel.proceedBtn.mousePressEvent = self.launchProject
        self.launchWindow.launchPanel.addProjectBtn.mousePressEvent = self.showNewProjectWindow

        self.newProjectWindow.newProjectPanel.createBtn.mousePressEvent = self.hideNewProjectWindow

        self.dynamicInfoWindow.toolbar.saIcon.mousePressEvent = self.showSignalAnalysisWindow
        self.dynamicInfoWindow.toolbar.closeIcon.mousePressEvent = self.showLaunchWindow

        self.currentWindow = self.loginWindow

    def _showLoadingWindow(self,delay):
        self.loading.showWithDelay(delay)

    def _switchToWindow(self,window,hide_current = True):
        self._showLoadingWindow(1000)
        if hide_current == True:
            self.currentWindow.close()
            self.currentWindow = window
        window.show()
        self.loading.close()
        

    def _hideWindow(self,window):
        window.close()

    def showLoginWindow(self,event = None):
        self._switchToWindow(self.loginWindow)

    def showLaunchWindow(self,event = None):
        self._switchToWindow(self.launchWindow)
        self.launchWindow.launchPanel.workspace = "NONE"
        
    def showDynamicInfoWindow(self,event=None):
        self._switchToWindow(self.dynamicInfoWindow)

    def showNewProjectWindow(self,event=None):
        self._switchToWindow(self.newProjectWindow,hide_current=False)

    def showModelWindow(self,event=None):
        self._switchToWindow(self.modelWindow,hide_current=False)

    def hideNewProjectWindow(self,event=None):
        self._hideWindow(self.newProjectWindow)
    
    def showSignalAnalysisWindow(self,event=None):
        self._showLoadingWindow(1000)
        self.signalAnalysisWindow.show()
        self.loading.close()

    def launchProject(self,event=None):
        wkspc = self.launchWindow.launchPanel.workspace
        if wkspc == "DI":
            self.dynamicInfoWindow.project = self.launchWindow.launchPanel.searchInput.text()
            self.showDynamicInfoWindow()

        self.launchWindow.launchPanel.resetCards()
        self.launchWindow.launchPanel.searchInput.clear()
            
