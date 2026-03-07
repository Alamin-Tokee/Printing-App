from PyQt6.QtWidgets import (
    QLabel, QPushButton,  QLineEdit, QMessageBox, QDialog, QFormLayout
)
from PyQt6.QtCore import Qt
import database, data_content
# ---------------- Sign-In Dialog ----------------
class SignInDialog(QDialog):
    def __init__(self, project=None):
        super().__init__()
        self.setWindowTitle("Sign In")
        self.setFixedSize(400, 350)
        self.setStyleSheet("background-color: #2c2c2c; color: white;")
        self.project = project
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


         # OR Label
        title_label = QLabel("User Login")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setStyleSheet("color: white; font-weight: bold;font-size: 20px; margin-bottom: 10px;")

        # OR Label
        or_label = QLabel("────────  OR  ────────")
        or_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        or_label.setStyleSheet("color: white; font-weight: bold;")

        # Add widgets
        layout.addRow(title_label)  # Title
        layout.addRow("EMP ID:", self.emp_id_input)
        layout.addRow("Password:", self.pass_input)
        layout.addRow("", or_label)  # OR separator
        layout.addRow("Access Code:", self.access_code_input)

        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("""
            QPushButton {
                background-color: #00b894;
                border-radius: 10px;
                padding: 8px;
                text-align: center;
                font-weight: bold;
                margin-top: 10px;
                color: white;
            }
            QPushButton:hover {
                background-color: #019875;
            }
        """)

        self.login_btn.clicked.connect(self.check_credentials)
        layout.addRow("", self.login_btn)

    def check_credentials(self):
        emp_id = self.emp_id_input.text()
        password = self.pass_input.text()

        access_code = self.access_code_input.text()

        if emp_id and password:
            verity_user = data_content.verify_hrms_login_credentials(emp_id, password)
            print(f"HRMS login verification for user {emp_id}: {verity_user}")
            if verity_user:
                if self.project:
                    has_permission = database.check_user_permission(emp_id, self.project)
                    print(f"Permission check for user {emp_id} on project {self.project}: {has_permission}")
                    if has_permission:
                        self.emp_id = emp_id  # Store user ID for later use
                        self.project = self.project  # Store project for later use
                        self.accept()
                    else:
                        QMessageBox.warning(self, "Permission Denied", "You don't have permission to access this project.")
                else:
                    QMessageBox.warning(self, "Permission Denied", "You do not have permission to access this project.")

        elif access_code:
             if self.project == "ecd_printing" and access_code == "ECD123":
                self.emp_id = access_code  # Store user ID for later use
                self.project = self.project
                self.accept()
             elif self.project == "fifo_inventory" and access_code == "FIFO123":
                self.emp_id = access_code  # Store user ID for later use
                self.project = self.project
                self.accept()
             else:
                QMessageBox.warning(self, "Invalid Access Code", "The access code you entered is incorrect.")

        else:
             QMessageBox.warning(self, "Error", "Please fill all fields")