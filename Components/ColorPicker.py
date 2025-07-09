# -- Paste the ColorPickerButton class here --
from PyQt5.QtWidgets import QPushButton, QColorDialog
from PyQt5.QtGui import QColor

class ColorPickerButton(QPushButton):
    def __init__(self, initial_color=QColor(255, 0, 0), parent=None):
        super().__init__(parent)
        self._color = initial_color if isinstance(initial_color, QColor) else QColor(initial_color)
        self.setFixedSize(30, 20)
        self._update_style()
        self.clicked.connect(self._open_color_dialog)

    def _open_color_dialog(self):
        color = QColorDialog.getColor(self._color, self)
        if color.isValid():
            self._color = color
            self._update_style()

    def _update_style(self):
        self.setStyleSheet(f"background-color: {self._color.name()}; border: 1px solid #aaa;")

    def color(self) -> QColor:
        return self._color

    def setColor(self, color: QColor):
        if color.isValid():
            self._color = color
            self._update_style()

# -- End of ColorPickerButton class --
