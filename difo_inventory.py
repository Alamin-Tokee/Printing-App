from PyQt6.QtWidgets import (
    QGridLayout, QMainWindow, QTextEdit, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QStackedWidget, QLineEdit,
    QTableWidget, QTableWidgetItem, QFrame, QMessageBox, QGraphicsDropShadowEffect
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtWidgets import QHeaderView
from PyQt6.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt6.QtCore import QMarginsF
from PyQt6.QtGui import QColor, QPageLayout, QPainter, QPixmap
from datetime import datetime
from PyQt6.QtGui import QTextDocument, QPageSize, QPageLayout
from PyQt6.QtCore import QSizeF
import database, data_content 


class DifoPanel(QMainWindow):
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
        self.ecd_page = self.create_mapping_page()
        self.print_page = self.create_print_page()

        self.stack.addWidget(self.dashboard_page)
        self.stack.addWidget(self.ecd_page)
        self.stack.addWidget(self.print_page)

        main_layout.addWidget(self.sidebar)
        main_layout.addWidget(self.stack)

        self.statusBar().showMessage("Connected to Database")

    # ---------------- SIDEBAR ----------------
    def create_sidebar(self):
        sidebar = QFrame()
        sidebar.setObjectName("sidebar")
        sidebar.setFixedWidth(220)

        layout = QVBoxLayout(sidebar)
        title = QLabel("ECD Printing")
        title.setObjectName("title")
        layout.addWidget(title)
        btn_dashboard = QPushButton("Dashboard")
        btn_users = QPushButton("Mapping")
        print_label = QPushButton("Printing")

        btn_dashboard.clicked.connect(self.show_dashboard)
        btn_users.clicked.connect(self.show_users)
        print_label.clicked.connect(self.show_print_label)

        layout.addWidget(btn_dashboard)
        layout.addWidget(btn_users)
        layout.addWidget(print_label)
        layout.addStretch()

        return sidebar

    def show_dashboard(self):
        self.stack.setCurrentIndex(0)
        self.update_dashboard_stats()

    def show_users(self):
        self.stack.setCurrentIndex(1)

    def show_print_label(self):
        self.stack.setCurrentIndex(2)


    #----------------- PRINTING ----------------
    def create_print_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)
        title = QLabel("Printing")
        title.setObjectName("title")


        input_layout = QHBoxLayout()
        self.barcode = QLineEdit()
        self.barcode.setPlaceholderText("Enter Barcode")
        self.barcode.setMinimumWidth(200)
        print_btn = QPushButton("Print")
        input_layout.addWidget(self.barcode)
        input_layout.addWidget(print_btn)
        print_btn.clicked.connect(self.print_label)
        self.barcode.returnPressed.connect(self.print_label)
        # print_btn.setDefault(True)
        # print_btn.setAutoDefault(True)

        content_layout = QHBoxLayout()
        self.preview_area = QWidget()
        preview_layout = QVBoxLayout(self.preview_area)
        preview_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.setSpacing(15)

        # Style (vertical decoration)
        self.preview_area.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0,
                    x2:0, y2:1,
                    stop:0 #f5f7fa,
                    stop:1 #c3cfe2
                );
                border-radius: 15px;
                border: 1px solid #bbb;
            }
        """)

        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(25)
        shadow.setXOffset(0)
        shadow.setYOffset(5)
        shadow.setColor(QColor(0,0,0,120))

        self.preview_area.setGraphicsEffect(shadow)

        # Text
        self.preview_text = QLabel("Barcode scans will appear here")
        self.preview_text.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Image
        self.image_label = QLabel()
        pixmap = QPixmap("inc/ECD.jpg")

        if not pixmap.isNull():
            self.image_label.setPixmap(
                pixmap.scaled(450, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            )
            self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add to layout
        preview_layout.addWidget(self.preview_text)
        preview_layout.addWidget(self.image_label)

                    

        self.previous_scan = QTableWidget()
        self.previous_scan.setColumnCount(3)
        self.previous_scan.setHorizontalHeaderLabels(["ID", "Barcode", "Scan Time"])

        self.previous_scan.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.previous_scan.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.previous_scan.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)


        # Stretch columns
        self.previous_scan.horizontalHeader().setStretchLastSection(True)
       

        # Add to content layout
        content_layout.addWidget(self.preview_area, 1)
        content_layout.addWidget(self.previous_scan, 1)

        # =======================
        # Add everything to main
        # =======================
        layout.addWidget(title)
        layout.addLayout(input_layout)
        layout.addLayout(content_layout)

        self.load_scan_history()

        return page
    

    # Load scan history from database
    
    def load_scan_history(self):
        history = database.get_scan_history()
        self.previous_scan.setRowCount(len(history))

        for row_idx, (id, barcode, scan_time) in enumerate(history):
            self.previous_scan.setItem(row_idx, 0, QTableWidgetItem(str(id)))
            self.previous_scan.setItem(row_idx, 1, QTableWidgetItem(barcode))
            self.previous_scan.setItem(row_idx, 2, QTableWidgetItem(scan_time))
    

    #----------------- PRINTING LOGIC ----------------
    def print_label(self):
        barcode = self.barcode.text().strip()
        if not barcode:
            QMessageBox.warning(self, "Input Error", "Please enter a barcode.")
            return
        
        try:
            database.add_scan_history(barcode)
        except Exception as e:
            QMessageBox.critical(self, "Database Error", f"Error adding scan history: {e}")
            return
        

        get_wbst_code = data_content.get_wbst_code_by_barcode(barcode)
        get_mapping_date = database.get_ecd_mapping_by_wbst_code(get_wbst_code)
        #print("Mapping Data:", get_mapping_date)
        get_ecd_properties = data_content.get_ecd_mapping_properties(get_mapping_date[2], get_mapping_date[3])
        #print("ECD Properties:", get_ecd_properties)

        fie_url = get_ecd_properties[0]['file_url'] if get_ecd_properties else None

        # For demo, we just show the barcode in preview
        self.preview_text.setText(f"Printing label for:\n{barcode}")

        #update preview image
        pixmap = QPixmap(fie_url)  # Replace with dynamic image generation if needed
        if not pixmap.isNull():
            self.image_label.setPixmap(
                pixmap.scaled(450, 300, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            )

            # Directly print the image
            printer = QPrinter(QPrinter.PrinterMode.HighResolution)
            printer.setFullPage(True)
            painter = QPainter(printer)

            # Get printer DPI
            dpi = printer.resolution()

            #Convert mm to pixels
            def mm_to_px(mm_val):
                return int(mm_val * dpi / 25.4)
            
            width_px = mm_to_px(160)
            height_px = mm_to_px(90)

            # Scale image to fit page
            scaled_pixmap = pixmap.scaled(
                width_px, height_px,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation
            )

            # Center image on page
            page_rect = printer.pageRect(QPrinter.Unit.DevicePixel)
            x = (page_rect.width() - scaled_pixmap.width()) // 2
            y = (page_rect.height() - scaled_pixmap.height()) // 2
            painter.drawPixmap(int(x), int(y), scaled_pixmap)
            painter.end()

        # Add to previous scans
        #current_text = self.previous_scan.toPlainText()
        #new_entry = f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')} - {barcode}"
        ##self.previous_scan.setText(current_text + new_entry + "\n")
        self.load_scan_history()

        # Clear input
        self.barcode.clear()

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

    # ---------------- ECD MAPPINGS ----------------
    def create_mapping_page(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        grid_layout = QGridLayout()
        grid_layout.setSpacing(8)

        self.wbst_code_input = QLineEdit()
        self.wbst_code_input.setPlaceholderText("WBST Code")

        self.wbst_product_model = QLineEdit()
        self.wbst_product_model.setPlaceholderText("Product Model")

        self.wbst_product_version = QLineEdit()
        self.wbst_product_version.setPlaceholderText("Product Version")

        #---------------- FIELD DEFINITIONS ----------------
        row1_fields = [
            ("WBST Code", self.wbst_code_input),
            ("Product Model", self.wbst_product_model),
            ("Product Version", self.wbst_product_version)
        ]

        #---------------- ADD ROW1 ----------------
        for col, (label_text, widget) in enumerate(row1_fields):
            label = QLabel(label_text)
            label.setStyleSheet("color: white;")
            grid_layout.addWidget(label, 0, col)
            grid_layout.addWidget(widget, 1, col)


        add_btn = QPushButton("Add User")
        add_btn.setFixedWidth(150)
        #delete_btn = QPushButton("Delete Selected")

        add_btn.clicked.connect(self.add_ecd_mapping)
       # delete_btn.clicked.connect(self.delete_user)



        # Button layout (left aligned)
        button_layout = QHBoxLayout()
        button_layout.addStretch()   # pushes buttons to right
        button_layout.addWidget(add_btn)
        #button_layout.addWidget(delete_btn)


        # -------- HORIZONTAL SPLIT AREA --------
        # content_layout = QHBoxLayout()

        # # LEFT SIDE (Print / Data View)
        # self.preview_area = QTextEdit()
        # self.preview_area.setReadOnly(True)
        # self.preview_area.setPlaceholderText("User details will appear here...")
        

        # RIGHT SIDE (Table)
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "WBST Code", "Product Model", "Product Version", "Insert Time"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)


         # Add both sides
        # content_layout.addWidget(self.preview_area, 1)  # left stretch
        # content_layout.addWidget(self.table, 2)         # right stretch bigger


        side_title = QLabel("ECD Mappings")
        side_title.setStyleSheet("font-size: 20px; font-weight: bold;color: white;")
        side_title.setObjectName("side_title")
        layout.addWidget(side_title)
        # layout.addWidget(self.name_input)
        # layout.addWidget(self.email_input)
        layout.addLayout(grid_layout)
        layout.addLayout(button_layout)
        #layout.addWidget(delete_btn)
        #layout.addLayout(content_layout)
        layout.addWidget(self.table)

        self.load_ecd_mappings()
        return page

    def load_ecd_mappings(self):
        data = database.get_ecd_mappings()
        self.table.setRowCount(len(data))

        for row_idx, row_data in enumerate(data):
            for col_idx, col_data in enumerate(row_data):
                self.table.setItem(row_idx, col_idx, QTableWidgetItem(str(col_data)))

        self.update_dashboard_stats()

    def add_ecd_mapping(self):
        wsbt_code = self.wbst_code_input.text().strip()
        product_model = self.wbst_product_model.text().strip()
        product_version = self.wbst_product_version.text().strip()

        if not wsbt_code or not product_model or not product_version:
            QMessageBox.warning(self, "Input Error", "All fields are required.")
            return

        database.add_ecd_mapping(wsbt_code, product_model, product_version)
        self.wbst_code_input.clear()
        self.wbst_product_model.clear()
        self.wbst_product_version.clear()
        self.load_ecd_mappings()

        # Open print preview popup


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