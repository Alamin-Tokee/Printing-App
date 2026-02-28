from PyQt6.QtWidgets import (
    QMainWindow, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QLineEdit,
    QTableWidget, QTableWidgetItem, QFrame, QMessageBox, QDateEdit, QGridLayout
)
from PyQt6.QtCore import Qt, QTimer, QDate
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

        grid_layout = QGridLayout()
        grid_layout.setSpacing(10)

        # ----------- INPUT FIELDS -----------

        self.item_code_input = QLineEdit()
        self.item_code_input.setPlaceholderText("Item Code")

        self.item_name_input = QLineEdit()
        self.item_name_input.setPlaceholderText("Item Name")

        self.item_qty_input = QLineEdit()
        self.item_qty_input.setPlaceholderText("Item Quantity")

        self.material_input = QLineEdit()
        self.material_input.setPlaceholderText("Material Type")

        self.batch_input = QLineEdit()
        self.batch_input.setPlaceholderText("Batch Number")

        self.pallet_box_input = QLineEdit()
        self.pallet_box_input.setPlaceholderText("Pallet Box Number")

        self.po_input = QLineEdit()
        self.po_input.setPlaceholderText("PO Number")

        self.shift_input = QLineEdit()
        self.shift_input.setPlaceholderText("Shift")

        self.supplier_input = QLineEdit()
        self.supplier_input.setPlaceholderText("Supplier Name")

        self.receive_date = QDateEdit()
        self.receive_date.setDate(QDate.currentDate())
        self.receive_date.setCalendarPopup(True)
        self.receive_date.setDisplayFormat("dd-MM-yyyy")
        self.receive_date.setMinimumHeight(38)

        self.expiry_date = QDateEdit()
        self.expiry_date.setDate(QDate.currentDate())
        self.expiry_date.setCalendarPopup(True)
        self.expiry_date.setDisplayFormat("dd-MM-yyyy")
        self.expiry_date.setMinimumHeight(38)

        # ----------- FIELD DEFINITIONS -----------

        row1_fields = [
            ("Item Code", self.item_code_input),
            ("Item Name", self.item_name_input),
            ("Item Quantity", self.item_qty_input),
            ("Material Type", self.material_input),
            ("Batch Number", self.batch_input),
            ("Pallet Box Number", self.pallet_box_input),
        ]

        row2_fields = [
            ("PO Number", self.po_input),
            ("Shift Number", self.shift_input),
            ("Supplier Name", self.supplier_input),
            ("Receive Date", self.receive_date),
            ("Expiry Date", self.expiry_date),
        ]

        # ----------- ADD ROW 1 -----------

        for col, (label_text, widget) in enumerate(row1_fields):
            label = QLabel(label_text)
            label.setStyleSheet("color: white;")
            grid_layout.addWidget(label, 0, col)
            grid_layout.addWidget(widget, 1, col)

        # ----------- ADD ROW 2 -----------

        for col, (label_text, widget) in enumerate(row2_fields):
            label = QLabel(label_text)
            label.setStyleSheet("color: white;")
            grid_layout.addWidget(label, 2, col)
            grid_layout.addWidget(widget, 3, col)

        # Equal column stretch
        for i in range(6):
            grid_layout.setColumnStretch(i, 1)

        # ----------- BUTTONS -----------

        add_btn = QPushButton("Add User")
        add_btn.setFixedWidth(150)   # limited width
        #delete_btn = QPushButton("Delete Selected")
        #delete_btn.setFixedWidth(150)

        add_btn.clicked.connect(self.add_user)
        #delete_btn.clicked.connect(self.delete_user)

        # Button layout (left aligned)
        button_layout = QHBoxLayout()
        button_layout.addStretch()   # pushes buttons to right
        button_layout.addWidget(add_btn)
        #button_layout.addWidget(delete_btn)

        # ----------- TABLE -----------

        self.table = QTableWidget()
        self.table.setColumnCount(12)  # 11 fields + ID
        self.table.setHorizontalHeaderLabels([
            "ID",
            "Item Code",
            "Item Name",
            "Quantity",
            "Material",
            "Batch",
            "Pallet Box",
            "PO Number",
            "Shift",
            "Supplier",
            "Receive Date",
            "Expiry Date"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)

        # ----------- MAIN LAYOUT -----------

        side_title = QLabel("Manage Users")
        side_title.setStyleSheet("font-size: 20px; font-weight: bold;color: white;")

        layout.addWidget(side_title)
        layout.addLayout(grid_layout)
        layout.addLayout(button_layout)   # buttons left aligned
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
        # ---------- GET VALUES FROM INPUTS ----------
        item_code = self.item_code_input.text().strip()
        item_name = self.item_name_input.text().strip()
        item_qty = self.item_qty_input.text().strip()
        material = self.material_input.text().strip()
        batch = self.batch_input.text().strip()
        pallet_box = self.pallet_box_input.text().strip()
        po_number = self.po_input.text().strip()
        shift = self.shift_input.text().strip()
        supplier = self.supplier_input.text().strip()
        receive_date = self.receive_date.date().toString("yyyy-MM-dd")
        expiry_date = self.expiry_date.date().toString("yyyy-MM-dd")

        # ---------- VALIDATION ----------
        required_fields = [item_code, item_name, item_qty]
        if not all(required_fields):
            QMessageBox.warning(self, "Input Error", "Item Code, Item Name and Quantity are required.")
            return

        if not item_qty.isdigit():
            QMessageBox.warning(self, "Input Error", "Item Quantity must be a number.")
            return

        # ---------- INSERT INTO DATABASE ----------
        database.add_user(
            item_code, item_name, item_qty, material, batch,
            pallet_box, po_number, shift, supplier,
            receive_date, expiry_date
        )

        # ---------- CLEAR INPUTS ----------
        self.item_code_input.clear()
        self.item_name_input.clear()
        self.item_qty_input.clear()
        self.material_input.clear()
        self.batch_input.clear()
        self.pallet_box_input.clear()
        self.po_input.clear()
        self.shift_input.clear()
        self.supplier_input.clear()
        self.receive_date.setDate(QDate.currentDate())
        self.expiry_date.setDate(QDate.currentDate())

        # ---------- REFRESH TABLE ----------
        self.load_users()

        # ---------- OPTIONAL: Print Preview ----------
        self.open_print_preview(item_code, item_name, item_qty, material, batch, pallet_box,
                                po_number, shift, supplier, receive_date, expiry_date)

    def open_print_preview(self, item_code, item_name, item_qty, material, batch, pallet_box,
                                po_number, shift, supplier, receive_date, expiry_date):
        printer = QPrinter(QPrinter.PrinterMode.HighResolution)
        # Correct PyQt6 margins
        label_size = QSizeF(100, 78)  # mm
        printer.setPageSize(QPageSize(label_size, QPageSize.Unit.Millimeter))
        # Set small margins
        printer.setPageMargins(QMarginsF(2, 2, 2, 2), QPageLayout.Unit.Millimeter)
        preview = QPrintPreviewDialog(printer, self)
        preview.setWindowTitle("Print Preview")

        preview.paintRequested.connect(lambda printer: self.print_document(printer, item_code, item_name, item_qty, material, batch, pallet_box,
                                po_number, shift, supplier, receive_date, expiry_date))

        #QTimer.singleShot(5000, preview.close)

        preview.exec()

    
    def print_document(self, printer, item_code, item_name, item_qty, material, batch, pallet_box,
                                po_number, shift, supplier, receive_date, expiry_date):
       
        # ---- Create printer ----
        #printer = QPrinter(QPrinter.PrinterMode.HighResolution)

        # Set custom page size: 78mm x 100mm
    
        # ---- Create document ----
        document = QTextDocument()

        today = datetime.now().strftime("%d %B %Y")
        #invoice_no = datetime.now().strftime("%Y%m%d%H%M%S")
        html_content = f"""
        <html>
        <head>
        <style>
            @page {{
                size: 75mm 100mm;
                margin: 0;
            }}

            body {{
                margin: 0;
                padding: 0;
                font-family: Arial, sans-serif;
            }}

            .label {{
                width: 75mm;
                height: 100mm;
                padding: 1mm;
                box-sizing: border-box;
                border: 1px solid black;
                page-break-after: avoid;
                overflow: hidden;
                font-size: 2pt;
            }}

            .center {{
                text-align: center;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                font-size: 1.8pt;
            }}

            td {{
                padding: 0px;
                vertical-align: top;
            }}

            hr {{
                margin: 3px 0;
            }}


        </style>
        </head>
        <body>
        <div class="label">

            <!-- UPPER SECTION -->
            <div class="upper_section">

                <!-- LEFT: QR and Item Code -->
                <table>
                    <tr>

                         <!-- LEFT -->
                        <td width="20%" valign="top">
                            <img src="qr.png" width="10" height="10"><br>
                        </td>

                        <!-- CENTER -->
                        <td width="55%" align="center" valign="top">
                            <b style="font-size:2.5pt;">Walton Hi-Tech Industries PLC</b><br>
                            <span style="font-size:2pt;">
                                Chandra, Kaliakoir, Gazipur
                            </span><br><br><br>

                            <span style="font-size:1.8pt;border:1px solid black;padding:2px;">
                                <b>498379674936934769456794769546</b>
                            </span>
                            <br><br><br>
                        </td>

                        <!-- RIGHT -->
                        <td width="25%" align="right" valign="top">
                            <span style="font-size:1.5pt;">{today}</span><br>
                            <img src="qr.png" width="12" height="12">
                        </td>
                    </tr>
                </table>

            </div>

            <!-- LOWER SECTION: Item Details Table -->
            <div class="lower_section">
                <table>
                    <tr style="font-size:1.8pt;">
                        <td width="40%" valign="top" style="text-align: left;font-size:2px">
                            <b style="margin-top: 1pt;">Item Code</b>: {item_code} <br><br>
                            <b style="margin-top: 1pt;">Item Name:</b>{item_name} <br><br>
                            <b style="margin-top: 1pt;">Item Qty:</b>{item_qty} PCS <br><br>
                            <b style="margin-top: 1pt;">Expiry Date:</b>{expiry_date} <br><br>
                            <b style="margin-top: 1pt;">Received Date:</b>{receive_date} <br><br>
                            <b style="margin-top: 1pt;">Pallet/Box:</b>{pallet_box} <br><br>
                        </td>

                        <!-- CENTER -->
                        <td width="40%" align="center" valign="top" style="text-align: left;font-size:2px">
                            <b style="margin-top: 1pt;text-align: left;">Material:</b>{material} <br><br>
                            <b style="margin-top: 1pt;text-align: left;">Shift:</b>{shift} <br><br>
                            <b style="margin-top: 1pt;text-align: left;" >Batch No:</b>{batch} <br><br>
                            <b style="margin-top: 1pt;text-align: left;">Supplier:</b>{supplier} <br><br>
                        </td>

                        <td width="20%" align="right" valign="top" style="text-align: left;font-size:2px">
                            <b style="margin-top: 1pt;text-align: left;">iQC Status</b> <br><br>
                            <b style="margin-top: 1pt;text-align: left;">Pass</b> <br><br>
                            <b style="margin-top: 1pt;text-align: left;">Fail</b> <br><br>
                        </td> 

                    </tr>
                </table>
            </div>
        </div>
        </body>
        </html>
        """

        document.setHtml(html_content)

        # Correct Qt6 single-page label sizing
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