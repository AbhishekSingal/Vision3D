import Styles.colors as cl

input_style1 = f"""
QLineEdit {{
    background-color: {cl.SYS_BG9};
    color: {cl.SYS_FG1};
    border: 1px solid {cl.SYS_BD5};
    border-radius: 3px;
    padding: 5px;
}}

QLineEdit::placeholder {{
    color: #bbbbbb;
}}

QLineEdit:hover {{
    border: 1px solid #888888;
}}
"""

input_style2 = f"""
QLineEdit {{
    background-color: {cl.SYS_BG9};
    color: {cl.SYS_FG1};
    border: 1px solid {cl.SYS_BD5};
    border-radius: 3px;
    padding: 3px;
    font-size:10px;
}}

QLineEdit::placeholder {{
    color: #bbbbbb;
    font-size:10px;
}}

QLineEdit:hover {{
    border: 1px solid #888888;
}}
"""

input_style3 = f"""
QLineEdit {{
    background-color: {cl.SYS_BG3};
    color: {cl.SYS_FG1};
    border: 1px solid {cl.SYS_BD5};
    border-radius: 3px;
    padding: 5px;
}}

QLineEdit::placeholder {{
    color: #bbbbbb;
}}

QLineEdit:hover {{
    border: 1px solid #888888;
}}
"""

input_style4 = f"""
QLineEdit {{
    background-color: {cl.SYS_BG3};
    color: {cl.SYS_FG1};
    border: 1px solid {cl.SYS_BD5};
    border-radius: 3px;
    padding: 5px;
    font-size:10px;
}}

QLineEdit::placeholder {{
    color: #bbbbbb;
    font-size:10px;
}}

QLineEdit:hover {{
    border: 1px solid #888888;
}}
"""


button_style1=f"""
QPushButton{{
    background-color:{cl.SYS_TH_BG1};
    color:{cl.SYS_FG4};
    border:1px solid {cl.SYS_TH_BD1};
    border-radius:3px;
    font-size:14px;
    font-weight:600;

}}

QPushButton:hover{{
    background-color:{cl.SYS_TH_BGH1};
}}
"""

button_style2=f"""
QPushButton{{
    background-color:{cl.SYS_BG3};
    color:{cl.SYS_FG4};
    border:1px solid {cl.SYS_BD4};
    border-radius:3px;
    font-size:14px;
    font-weight:600;

}}

QPushButton:hover{{
    background-color:{cl.SYS_BG4};
}}
"""

button_style3=f"""
QPushButton{{
    background-color:{cl.SYS_TH_BG1};
    color:{cl.SYS_FG4};
    border:1px solid {cl.SYS_TH_BD1};
    border-radius:3px;
    font-size:14px;
    font-weight:500;

}}

QPushButton:hover{{
    background-color:{cl.SYS_TH_BGH1};
}}
"""

button_style4=f"""
QPushButton{{
    background-color:{cl.SYS_BG3};
    color:{cl.SYS_FG4};
    border:1px solid {cl.SYS_BD4};
    border-radius:3px;
    font-size:14px;
    font-weight:500;

}}

QPushButton:hover{{
    background-color:{cl.SYS_BG4};
}}
"""

button_style5=f"""
QPushButton{{
    background-color:{cl.SYS_TH_BG1};
    color:{cl.SYS_FG4};
    border:1px solid {cl.SYS_TH_BD1};
    border-radius:3px;
    font-size:12px;
    font-weight:500;

}}

QPushButton:hover{{
    background-color:{cl.SYS_TH_BGH1};
}}
"""

button_style6=f"""
QPushButton{{
    background-color:{cl.SYS_BG3};
    color:{cl.SYS_FG4};
    border:1px solid {cl.SYS_BD4};
    border-radius:3px;
    font-size:12px;
    font-weight:500;

}}

QPushButton:hover{{
    background-color:{cl.SYS_BG4};
}}
"""

header_style1=f"""
QLabel{{
    color:{cl.SYS_FG1};
    font-size:28px;
    font-weight:600;
}}
"""

header_style2=f"""
QLabel{{
    color:{cl.SYS_FG1};
    font-size:28px;
    font-weight:400;
}}
"""

header_style3=f"""
QLabel{{
    color:{cl.SYS_FG1};
    font-size:20px;
    font-weight:600;
}}
"""


header_style4=f"""
QLabel{{
    color:{cl.SYS_FG3};
    font-size:12px;
    font-weight:600;
    border: none;             
    outline: none;            
    background: transparent;
}}
"""


text_style1=f"""
QLabel{{
    color:{cl.SYS_FG1};
    font-size:14px;
    font-weight:500;
    border: none;             
    outline: none;            
    background: transparent;
}}
"""

text_style2=f"""
QLabel{{
    color:{cl.SYS_FG1};
    font-size:16px;
    font-weight:500;
}}
"""

text_style3=f"""
QLabel{{
    color:{cl.SYS_FG1};
    font-size:12px;
    font-weight:500;
    border: none;             
    outline: none;            
    background: transparent;
}}
"""

text_style4=f"""
QLabel{{
    color:{cl.SYS_FG2};
    font-size:12px;
    font-weight:500;
    border: none;             
    outline: none;            
    background: transparent;
}}
"""

splitter_style1=f"""
QSplitter::handle {{
    background-color: {cl.SYS_BG2};
}}
"""


iconbtn_style1=f"""
QPushButton{{
    border:none;
    color:white;
    outline:none;
    font-size:14px;
    font-weight:500;
    padding-left:5px;
    text-align:left;
    margin:3px;
}}
"""

combo_style1 = f"""
QComboBox {{
    background-color: transparent;
    border: 1px solid #3B3B3B;
    color: white;
    padding: 6px;
    border-radius: 4px;
    font-size: 13px;
}}

QComboBox::drop-down {{
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 24px;
    background-color: transparent;
}}

QComboBox::down-arrow {{
    image: url(assets/downtriangle24.png);  /* Optional custom arrow */
    width: 12px;
    height: 12px;
}}

QComboBox QAbstractItemView {{
    background-color: #2B2B2B;
    color: white;
    padding: 0px;
    margin: 0px;
    border: 1px solid #3B3B3B;
    selection-background-color: #505050;
    selection-color: white;

    /* Most important */
    outline: none;
    show-decoration-selected: 1;
}}
"""


infotext_style1=f"""
QLabel{{
    color : {cl.SYS_FG2};
    font-size : 14px;
    border: none;             
    outline: none;            
    background: transparent;
}}
"""

infotext_style2=f"""
QLabel{{
    color : {cl.SYS_FG3};
    font-size : 14px;
    border: none;             
    outline: none;            
    background: transparent;
}}
"""



table_style1=f"""
QTableWidget{{
    color:white;
}}
QHeaderView::section{{
    color:white;
    font-weight:600;
    background-color:{cl.SYS_BG1};
    font-size:12px;
    outline:none;
    border:none;
    border-right:1px solid {cl.SYS_BD1};
}}


QTableWidget {{
    gridline-color: #444444;
    alternate-background-color: #2e2e2e;
    border : 1px solid {cl.SYS_BD3};
    background-color: {cl.SYS_BG2}
}}
"""

table_style2=f"""
QTableWidget{{
    color:white;
}}
QHeaderView::section{{
    color:white;
    font-weight:500;
    background-color:{cl.SYS_BG2};
    font-size:11px;
    outline:none;
    border:none;
    border-right:1px solid {cl.SYS_BD1};
}}


QTableWidget {{
    gridline-color: #444444;
    alternate-background-color: #2e2e2e;
    font-size:10px;
}}
"""

date_style1=f"""
QDateEdit{{
    background-color: #2e2e2e;
    color: white;
    border: 1px solid #555;
    padding: 4px;
}}
"""


scrollbar_style = f"""
QScrollArea {{
    border: 1px solid {cl.SYS_BD3}
}}

QScrollBar:vertical {{
    background: {cl.SYS_BD3};  /* Dark background track */
    width: 16px;
    margin: 0px;
    border: none;
}}

QScrollBar::handle:vertical {{
    background: {cl.SYS_BG7};
    min-height: 20px;
    border-radius: 0px;
    margin: 12px 0;
}}

QScrollBar::handle:vertical:hover {{
    background: {cl.SYS_BG8};
}}

QScrollBar::add-line:vertical,
QScrollBar::sub-line:vertical {{
    background: {cl.SYS_BG4};
    height: 12px;
    subcontrol-origin: margin;
    border: none;
}}

QScrollBar::sub-line:vertical {{
    subcontrol-position: top;
    image: url(assets/upicon100.png); 
}}

QScrollBar::add-line:vertical {{
    subcontrol-position: bottom;
    image: url(assets/downicon100.png);
}}

QScrollBar::up-arrow:vertical, QScrollBar::down-arrow:vertical {{
    width: 8px;
    height: 8px;
    background: none;
}}

QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical {{
    background: none;
}}

/* Horizontal scrollbar styles */

QScrollBar:horizontal {{
    background: {cl.SYS_BD3};
    height: 16px;
    margin: 0px;
    border: none;
}}

QScrollBar::handle:horizontal {{
    background: {cl.SYS_BG7};
    min-width: 20px;
    border-radius: 0px;
    margin: 0 12px;
}}

QScrollBar::handle:horizontal:hover {{
    background: {cl.SYS_BG8};
}}

QScrollBar::add-line:horizontal,
QScrollBar::sub-line:horizontal {{
    background: {cl.SYS_BG4};
    width: 12px;
    subcontrol-origin: margin;
    border: none;
}}

QScrollBar::sub-line:horizontal {{
    subcontrol-position: left;
    image: url(assets/lefticon100.png); 
}}

QScrollBar::add-line:horizontal {{
    subcontrol-position: right;
    image: url(assets/righticon100.png);
}}

QScrollBar::left-arrow:horizontal, QScrollBar::right-arrow:horizontal {{
    width: 8px;
    height: 8px;
    background: none;
}}

QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal {{
    background: none;
}}

QScrollBar::corner {{
    background: {cl.SYS_BD3};
    border: none;
}}

QAbstractScrollArea::corner {{
    background: {cl.SYS_BD3};
    border: none;
}}
"""



dock_style1= f"""
QDockWidget {{
    background-color: {cl.SYS_BG4};
    color: white;
    font-weight: 600;
    border: 1px solid {cl.SYS_BD1};
}}

QDockWidget::title {{
    background-color: {cl.SYS_BG5};
    border:1px solid {cl.SYS_BD3};
    padding: 4px;
}}
"""

panel_style1=f"""
QWidget{{
    background-color:{cl.SYS_BG1};
    border-left:1px solid {cl.SYS_BD3};
    border-right:1px solid {cl.SYS_BD3};
    border-bottom:1px solid {cl.SYS_BD3};
}}
"""

checkbox_style1=f"""
QCheckBox{{
    color:{cl.SYS_FG1};
    font-size:12px;
}}
"""
