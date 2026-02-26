from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QLineEdit,
    QTableWidget, QTableWidgetItem, QFrame, QMessageBox
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtPrintSupport import QPrinter, QPrintPreviewDialog
from PyQt6.QtCore import QMarginsF
from PyQt6.QtGui import QPageLayout
from datetime import datetime
from PyQt6.QtGui import QTextDocument, QPageSize, QPageLayout
from PyQt6.QtCore import QSizeF
import database


class FifoPanel(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Professional Dark Dashboard")
        self.setMinimumSize(1000, 600)

        self.init_ui()

    # ---------------- MAIN UI ----------------
    def init_ui(self):
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QHBoxLayout(main_widget)

        self.sidebar = self.create_sidebar()
        self.stack = QStackedWidget()

        self.dashboard_page = self.create_dashboard_page()
        self.users_page = self.create_users_page()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.users_page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        self.statusBar().showMessage("Connected to Database")

    # ---------------- SIDEBAR ----------------
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)
        title = QLabel("FIFO Inventory")
        title.setObjectName("title")
        layout.addWidget(title)
        btn_dashboard = QPushButton("Dashboard")
        btn_users = QPushButton("Users")

        btn_dashboard.clicked.connect(self.show_dashboard)
        btn_users.clicked.connect(self.show_users)

        layout.addWidget(btn_dashboard)
        layout.addWidget(btn_users)
        layout.addStretch()

        return sidebar

    def show_dashboard(self):
        self.stack.setCurrentIndex(0)
        self.update_dashboard_stats()

    def show_users(self):
        self.stack.setCurrentIndex(1)

    # ---------------- DASHBOARD ----------------
    def create_dashboard_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        title = QLabel("Dashboard Overview")
        title.setObjectName("title")

        self.user_count_label = QLabel()
        self.user_count_label.setObjectName("card")
        self.user_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout.addWidget(title)
        layout.addWidget(self.user_count_label)
        layout.addStretch()

        self.update_dashboard_stats()
        return page

    def update_dashboard_stats(self):
        users = database.get_users()
        self.user_count_label.setText(f"Total Users: {len(users)}")

    # ---------------- USERS ----------------
    def create_users_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        input_layout = QHBoxLayout()

        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Name")
        self.name_input.setMinimumWidth(200)

        self.email_input = QLineEdit()
        self.email_input.setPlaceholderText("Email")
        self.email_input.setMinimumWidth(200)

        self.material_input = QLineEdit()
        self.material_input.setPlaceholderText("Material Type")

        self.bath_input = QLineEdit()
        self.bath_input.setPlaceholderText("Bath Number")

        self.po_input = QLineEdit()
        self.po_input.setPlaceholderText("PO Number")


        input_layout.addWidget(self.name_input)
        input_layout.addWidget(self.email_input) 
        input_layout.addWidget(self.material_input)
        input_layout.addWidget(self.bath_input)
        input_layout.addWidget(self.po_input)

        add_btn = QPushButton("Add User")
        delete_btn = QPushButton("Delete Selected")

        add_btn.clicked.connect(self.add_user)
        delete_btn.clicked.connect(self.delete_user)


        # -------- HORIZONTAL SPLIT AREA --------
        # content_layout = QHBoxLayout()

        # # LEFT SIDE (Print / Data View)
        # self.preview_area = QTextEdit()
        # self.preview_area.setReadOnly(True)
        # self.preview_area.setPlaceholderText("User details will appear here...")
        

        # RIGHT SIDE (Table)
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Email"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)


         # Add both sides
        # content_layout.addWidget(self.preview_area, 1)  # left stretch
        # content_layout.addWidget(self.table, 2)         # right stretch bigger


        side_title = QLabel("Manage Users")
        side_title.setObjectName("side_title")
        layout.addWidget(side_title)
        # layout.addWidget(self.name_input)
        # layout.addWidget(self.email_input)
        layout.addLayout(input_layout)
        layout.addWidget(add_btn)
        layout.addWidget(delete_btn)
        #layout.addLayout(content_layout)
        layout.addWidget(self.table)

        self.load_users()
        return page

    def load_users(self):
        data = database.get_users()
        self.table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        self.update_dashboard_stats()

    def add_user(self):
        name = self.name_input.text().strip()
        email = self.email_input.text().strip()

        if not name or not email:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        database.add_user(name, email)
        self.name_input.clear()
        self.email_input.clear()
        self.load_users()

        # Open print preview popup
        self.open_print_preview(name, email)


    def open_print_preview(self, name, email):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        # Correct PyQt6 margins
        label_size = QSizeF(100, 78)  # mm
        printer.setPageSize(QPageSize(label_size, QPageSize.Unit.Millimeter))
        # Set small margins
        printer.setPageMargins(QMarginsF(2, 2, 2, 2), QPageLayout.Unit.Millimeter)
        preview = QPrintPreviewDialog(printer, self)
        preview.setWindowTitle("Print Preview")

        preview.paintRequested.connect(lambda printer: self.print_document(printer, name, email))

        QTimer.singleShot(5000, preview.close)

        preview.exec()

    
    def print_document(self, printer, name, email):
       
        # ---- Create printer ----
        #printer = QPrinter(QPrinter.PrinterMode.HighResolution)

        # Set custom page size: 78mm x 100mm
    
        # ---- Create document ----
        document = QTextDocument()

        today = datetime.now().strftime("%d %B %Y")
        invoice_no = datetime.now().strftime("%Y%m%d%H%M%S")

        html_content = f"""
        <div style="font-family: Arial; font-size:2pt; padding:5px; width:75mm;">
            <p style="text-align:center; margin:0.5pt;">INVOICE</p>

            <p style="margin:0.5pt 0;">
                <b>Your Company</b><br>
                123 Street<br>
                City, Country
            </p>

            <table width="100%" style="margin:0.5pt 0;">
                <tr>
                    <td><b>Invoice No:</b> {invoice_no}</td>
                    <td align="right"><b>Date:</b> {today}</td>
                </tr>
            </table>

            <p style="margin:0.5pt 0;">Bill To:</p>
            <p style="margin:0.5pt 0;">
                <b>Name:</b> {name}<br>
                <b>Email:</b> {email}
            </p>

            <hr style="margin:0.5pt 0;">
            <p style="text-align:center; margin:0.5pt 0;">Thank you for your business!</p>
        </div>
        """

        document.setHtml(html_content)

        # ✅ Correct Qt6 single-page label sizing
        page_rect = printer.pageLayout().paintRect(QPageLayout.Unit.Millimeter)
        document.setPageSize(QSizeF(page_rect.width(), page_rect.height()))

        # ---- Print / Preview ----
        document.print(printer)


    def delete_user(self):
        selected_row = self.table.currentRow()

        if selected_row < 0:
            QMessageBox.warning(self, "Selection Error", "Select a user first.")
            return

        user_id = int(self.table.item(selected_row, 0).text())
        database.delete_user(user_id)
        self.load_users()