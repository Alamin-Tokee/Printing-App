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

        self.setWindowTitle("Professional Dark Dashboard")
        self.setMinimumSize(1000, 600)

        self.init_ui()

    # ---------------- MAIN UI ----------------
    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        # Center layout
        main_layout = QVBoxLayout(main_widget)
        main_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        card_layout = QHBoxLayout()
        card_layout.setSpacing(50)  # space between cards
        card_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("Smart Printing Application")
        title.setObjectName("title")

        # FIFO Card
        fifo_card = self.create_card("FIFO")
        fifo_card.clicked.connect(self.open_fifo)

        # DIFO Card
        difo_card = self.create_card("DIFO")
        difo_card.clicked.connect(self.open_difo)

        card_layout.addWidget(fifo_card)
        card_layout.addWidget(difo_card)

        main_layout.addWidget(title)
        main_layout.addLayout(card_layout)

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
        self.fifo_window = FifoPanel()
        self.fifo_window.show()
        #self.close()  # optional

    def open_difo(self):
        sign_in = SignInDialog()
        if sign_in.exec():  # Only open DIFO if login succeeded
            self.difo_window = DifoPanel()
            self.difo_window.show()
            #self.close()  # optional