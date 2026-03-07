from PyQt6.QtWidgets import (
    QMainWindow,QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel
)
from PyQt6.QtCore import Qt


from fifo_inventory import FifoPanel
from difo_inventory import DifoPanel
from signin import SignInDialog


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
        # self.setWindowTitle("Smart Printing Application")
        self.setMinimumSize(1000, 600)

        self.drag_pos = None

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # -------- TITLE BAR --------
        title_bar = QWidget()
        title_bar.setFixedHeight(40)
        title_bar.setStyleSheet("background-color:#2b2b2b;")

        title_layout = QHBoxLayout(title_bar)
        title_layout.setContentsMargins(10, 0, 10, 0)

        title = QLabel("Smart Printing Application")
        title.setStyleSheet("color:white;font-size:15px;font-weight:bold;")

        btn_min = QPushButton("—")
        btn_max = QPushButton("□")
        btn_close = QPushButton("✕")

        btn_min.clicked.connect(self.showMinimized)
        btn_max.clicked.connect(self.toggle_maximize)
        btn_close.clicked.connect(self.close)

        btn_style = """
        QPushButton{
            color:white;
            background:transparent;
            border:none;
            font-size:16px;
            padding:5px 10px;
        }
        QPushButton:hover{
            background:#444;
        }
        """

        btn_min.setStyleSheet(btn_style)
        btn_max.setStyleSheet(btn_style)
        btn_close.setStyleSheet(btn_style)

        title_layout.addWidget(title)
        title_layout.addStretch()
        title_layout.addWidget(btn_min)
        title_layout.addWidget(btn_max)
        title_layout.addWidget(btn_close)

        main_layout.addWidget(title_bar)

        # -------- CENTER CONTENT --------
        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout = QHBoxLayout()
        card_layout.setSpacing(50)
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title_label = QLabel("Smart Printing Application")
        title_label.setStyleSheet("font-size:28px;font-weight:bold;color:white;")

        fifo_card = self.create_card("FIFO")
        fifo_card.clicked.connect(self.open_fifo)

        difo_card = self.create_card("DIFO")
        difo_card.clicked.connect(self.open_difo)

        card_layout.addWidget(fifo_card)
        card_layout.addWidget(difo_card)

        center_layout.addWidget(title_label)
        center_layout.addLayout(card_layout)

        main_layout.addLayout(center_layout)

        # enable dragging
        title_bar.mousePressEvent = self.mousePressEvent
        title_bar.mouseMoveEvent = self.mouseMoveEvent

    # ---------------- WINDOW DRAG ----------------
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_pos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if self.drag_pos:
            self.move(self.pos() + event.globalPosition().toPoint() - self.drag_pos)
            self.drag_pos = event.globalPosition().toPoint()

    # ---------------- MAXIMIZE ----------------
    def toggle_maximize(self):
        if self.isMaximized():
            self.showNormal()
        else:
            self.showMaximized()

    def create_card(self, text):
        card = QPushButton(text)
        card.setFixedSize(150, 150)
        card.setStyleSheet("""
            QPushButton {
                background-color: lightgray;
                border-radius: 15px;
                font-size: 18px;
                text-align: center;
                color: black;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: lightgreen;
            }
        """)
        return card

    def open_fifo(self):
        project = "fifo_inventory"
        sign_in = SignInDialog(project)
        if sign_in.exec():  # Only open FIFO if login succeeded
            emp_id = sign_in.emp_id  # Store logged-in user ID
            project = sign_in.project  # Store project for later use
            self.fifo_window = FifoPanel(emp_id, project)
            self.fifo_window.show()
            #self.close()  # optional

    def open_difo(self):
        project = "ecd_printing"
        sign_in = SignInDialog(project)
        if sign_in.exec():  # Only open DIFO if login succeeded
            emp_id = sign_in.emp_id  # Store logged-in user ID
            project = sign_in.project  # Store project for later use
            self.difo_window = DifoPanel(emp_id, project)
            self.difo_window.show()
            #self.close()  # optional




#Previous Laypout Code for Reference


# class MainWindow(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowFlags(Qt.WindowType.FramelessWindowHint)
#         self.setWindowTitle("Smart Printing Application")
#         self.setMinimumSize(1000, 600)

#         self.init_ui()

#     # ---------------- MAIN UI ----------------
#     def init_ui(self):
#         main_widget = QWidget()
#         self.setCentralWidget(main_widget)

#         # Center layout
#         main_layout = QVBoxLayout(main_widget)
#         main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         card_layout = QHBoxLayout()
#         card_layout.setSpacing(50)  # space between cards
#         card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

#         title = QLabel("Smart Printing Application")
#         title.setObjectName("title")

#         # FIFO Card
#         fifo_card = self.create_card("FIFO")
#         fifo_card.clicked.connect(self.open_fifo)

#         # DIFO Card
#         difo_card = self.create_card("DIFO")
#         difo_card.clicked.connect(self.open_difo)

#         card_layout.addWidget(fifo_card)
#         card_layout.addWidget(difo_card)

#         main_layout.addWidget(title)
#         main_layout.addLayout(card_layout)



