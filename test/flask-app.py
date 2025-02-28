import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QFrame, QVBoxLayout, QHBoxLayout, QWidget, QMenu,
    QSizePolicy, QLabel, QLineEdit, QPushButton, QComboBox, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtGui import QIcon, QAction, QPixmap
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Main Window with Three Horizontal Frames and Menubar")
        self.setWindowIcon(QIcon('vladpos_logo.png'))
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()

        # Set up the central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # Create frames
        frame1 = QFrame()
        frame1.setFrameShape(QFrame.Shape.NoFrame)
        frame1.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        frame2 = QFrame()
        frame2.setFrameShape(QFrame.Shape.NoFrame)
        frame2.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        frame3 = QFrame()
        frame3.setFrameShape(QFrame.Shape.NoFrame)
        frame3.setSizePolicy(QSizePolicy.Policy.Preferred, QSizePolicy.Policy.Expanding)

        # Add frames to layout
        main_layout.addWidget(frame1, 1)
        main_layout.addWidget(frame2, 5)
        main_layout.addWidget(frame3, 2)

        # Create menubar
        menubar = self.menuBar()

        # Create Cash Register menu
        cash_register_menu = QMenu("Cash Register", self)
        cash_register_menu.setIcon(QIcon('receipt.png'))
        cash_register_action = QAction(QIcon('receipt.png'), 'Cash Register Action', self)
        cash_register_menu.addAction(cash_register_action)
        menubar.addMenu(cash_register_menu)

        # Create Spravki menu
        spravki_menu = QMenu("Spravki", self)
        spravki_menu.setIcon(QIcon('paper.png'))
        spravki_action = QAction(QIcon('paper.png'), 'Spravki Action', self)
        spravki_menu.addAction(spravki_action)
        menubar.addMenu(spravki_menu)

        # Create Settings menu
        settings_menu = QMenu("Settings", self)
        settings_menu.setIcon(QIcon('setting.png'))
        settings_action = QAction(QIcon('setting.png'), 'Settings Action', self)
        settings_menu.addAction(settings_action)
        menubar.addMenu(settings_menu)

        # Frame 1 Contents
        frame1_layout = QHBoxLayout()
        frame1.setLayout(frame1_layout)

        self.input1 = QLineEdit()
        self.input1.setPlaceholderText("Input 1")
        frame1_layout.addWidget(self.input1, 3)  # Biggest

        self.input2 = QLineEdit()
        self.input2.setPlaceholderText("Input 2")
        frame1_layout.addWidget(self.input2, 1)  # Small

        self.input3 = QLineEdit()
        self.input3.setPlaceholderText("Input 3")
        frame1_layout.addWidget(self.input3, 1)  # Like the second

        self.popup_menu1 = QComboBox()
        self.popup_menu1.addItems(["Option 1", "Option 2", "Option 3", "Option 4"])
        frame1_layout.addWidget(self.popup_menu1, 2)  # A little bit more bigger

        self.add_button = QPushButton("Add")
        frame1_layout.addWidget(self.add_button, 2)  # Bigger

        # Frame 2 Contents
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels(["Input 1", "Input 2", "Input 3", "Popup Menu", "Multiplication", "Actions"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        frame2_layout = QVBoxLayout()
        frame2.setLayout(frame2_layout)
        frame2_layout.addWidget(self.table)

        # Frame 3 Contents
        frame3_layout = QVBoxLayout()
        frame3.setLayout(frame3_layout)

        sub_frame1 = QFrame()
        sub_frame1.setFrameShape(QFrame.Shape.NoFrame)
        sub_frame1_layout = QVBoxLayout()
        sub_frame1.setLayout(sub_frame1_layout)
        image_label = QLabel()
        image_label.setPixmap(QPixmap('user.png'))
        image_label.setScaledContents(True)  # Scale the image to fit the label
        image_label.setMaximumSize(100,100)  # Set maximum size for the image label
        sub_frame1_layout.addWidget(image_label, alignment=Qt.AlignmentFlag.AlignCenter)
        image_text_label = QLabel("Image Label")
        image_text_label.setAlignment(Qt.AlignmentFlag.AlignCenter)  # Center the text under the image
        sub_frame1_layout.addWidget(image_text_label)

        sub_frame2 = QFrame()
        sub_frame2.setFrameShape(QFrame.Shape.NoFrame)
        sub_frame2_layout = QVBoxLayout()
        sub_frame2.setLayout(sub_frame2_layout)
        popup_menu2 = QComboBox()
        popup_menu2.addItems(["Option 1", "Option 2", "Option 3", "Option 4"])
        sub_frame2_layout.addWidget(popup_menu2)
        button1 = QPushButton("Button 1")
        sub_frame2_layout.addWidget(button1)
        button2 = QPushButton("Button 2")
        sub_frame2_layout.addWidget(button2)

        sub_frame3 = QFrame()
        sub_frame3.setFrameShape(QFrame.Shape.NoFrame)
        sub_frame3_layout = QVBoxLayout()
        sub_frame3.setLayout(sub_frame3_layout)
        input4 = QLineEdit()
        input4.setPlaceholderText("Input 4")
        sub_frame3_layout.addWidget(input4)
        button3 = QPushButton("Button 3")
        sub_frame3_layout.addWidget(button3)
        button4 = QPushButton("Button 4")
        sub_frame3_layout.addWidget(button4)

        sub_frame4 = QFrame()
        sub_frame4.setFrameShape(QFrame.Shape.NoFrame)
        sub_frame4_layout = QVBoxLayout()
        sub_frame4.setLayout(sub_frame4_layout)
        input5 = QLineEdit()
        input5.setPlaceholderText("Input 5")
        sub_frame4_layout.addWidget(input5)
        button5 = QPushButton("Button 5")
        sub_frame4_layout.addWidget(button5)
        button6 = QPushButton("Button 6")
        sub_frame4_layout.addWidget(button6)

        frame3_sub_layout = QHBoxLayout()
        frame3_layout.addLayout(frame3_sub_layout)
        frame3_sub_layout.addWidget(sub_frame1)
        frame3_sub_layout.addWidget(sub_frame2)
        frame3_sub_layout.addWidget(sub_frame3)
        frame3_sub_layout.addWidget(sub_frame4)

        # Set equal stretch for sub-frames
        frame3_sub_layout.setStretch(0, 1)
        frame3_sub_layout.setStretch(1, 1)
        frame3_sub_layout.setStretch(2, 1)
        frame3_sub_layout.setStretch(3, 1)

        # Connect the add button to the function
        self.add_button.clicked.connect(self.add_to_table)

    def add_to_table(self):
        row_position = self.table.rowCount()
        self.table.insertRow(row_position)

        input1_text = self.input1.text()
        input2_text = self.input2.text()
        input3_text = self.input3.text()
        popup_text = self.popup_menu1.currentText()

        # Add the input data to the table
        self.table.setItem(row_position, 0, QTableWidgetItem(input1_text))
        self.table.setItem(row_position, 1, QTableWidgetItem(input2_text))
        self.table.setItem(row_position, 2, QTableWidgetItem(input3_text))
        self.table.setItem(row_position, 3, QTableWidgetItem(popup_text))

        # Calculate the multiplication of input2 and input3
        try:
            multiplication_result = float(input2_text) * float(input3_text)
        except ValueError:
            multiplication_result = "Error"
        self.table.setItem(row_position, 4, QTableWidgetItem(str(multiplication_result)))

        # Add a delete button with trash icon
        delete_button = QPushButton()
        delete_button.setIcon(QIcon('trash_icon.png'))
        delete_button.clicked.connect(lambda: self.remove_row(row_position))
        self.table.setCellWidget(row_position, 5, delete_button)

        # Clear the inputs after adding to the table
        self.input1.clear()
        self.input2.clear()
        self.input3.clear()
        self.popup_menu1.setCurrentIndex(0)

    def remove_row(self, row):
        self.table.removeRow(row)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())