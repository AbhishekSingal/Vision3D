from PyQt5.QtWidgets import QWidget,QHBoxLayout,QVBoxLayout
from PyQt5.QtCore import Qt


def GetBoxWidget(widgets: list, orientation: Qt.Orientation, spacing: int = 0,align=True,contentMargins = (0,0,0,0)) -> QWidget:
    widget = QWidget()
    widget.setStyleSheet("QWidget{border: none; outline: none}")
    widget.setAttribute(Qt.WA_StyledBackground, True)

    layout = QHBoxLayout() if orientation == Qt.Orientation(Qt.Horizontal) else QVBoxLayout()
    alignment = Qt.Alignment(Qt.AlignVCenter) if orientation == Qt.Orientation(Qt.Horizontal) else Qt.Alignment(Qt.AlignHCenter)

    layout.setContentsMargins(contentMargins[0],contentMargins[1],contentMargins[2],contentMargins[3])
    layout.setSpacing(spacing)

    for w in widgets:
        if isinstance(w, int):
            layout.addStretch(w)
        elif isinstance(w, str):
            layout.addSpacing(int(w))
        elif isinstance(w, tuple):
            if align == True:
                layout.addWidget(w[0], w[1], alignment)
            else:
                layout.addWidget(w[0], w[1])

    widget.setLayout(layout)
    return widget

