from PyQt6.QtWidgets import (
    QPushButton,  QLineEdit, QMessageBox, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt
# ---------------- Sign-In Dialog ----------------
class SignInDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("DIFO Sign In")
        self.setFixedSize(400, 350)
        self.setStyleSheet("background-color: #2c2c2c; color: white;")
        self.init_ui()

    def init_ui(self):
        layout = QFormLayout(self)

        # Fields
        self.emp_id_input = QLineEdit()
        self.emp_id_input.setPlaceholderText("Enter your EMP ID")
        self.emp_id_input.setStyleSheet("padding: 5px; border-radius: 5px;")

        self.pass_input = QLineEdit()
        self.pass_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.pass_input.setPlaceholderText("Enter your password")
        self.pass_input.setStyleSheet("padding: 5px; border-radius: 5px;")

        self.access_code_input = QLineEdit()
        self.access_code_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.access_code_input.setPlaceholderText("Enter access code")
        self.access_code_input.setStyleSheet("padding: 5px; border-radius: 5px;")

        layout.addRow("EMP ID:", self.emp_id_input)
        layout.addRow("Password:", self.pass_input)
        layout.addRow("Access Code:", self.access_code_input)

        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #00b894;
                border-radius: 10px;
                padding: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #019875;
            }
        """)
        self.login_btn.clicked.connect(self.check_credentials)
        layout.addWidget(self.login_btn)

    def check_credentials(self):
        emp_id = self.emp_id_input.text()
        password = self.pass_input.text()
        access_code = self.access_code_input.text()

        if emp_id and password and access_code:
            self.accept()
        else:
            QMessageBox.warning(self, "Error", "Please fill all fields")