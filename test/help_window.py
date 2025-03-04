from PyQt6.QtWidgets import QDialog, QVBoxLayout, QTextEdit, QDialogButtonBox

class HelpWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Помощ")
        self.setGeometry(100, 100, 400, 300)
        layout = QVBoxLayout()
        help_text = QTextEdit()
        help_text.setReadOnly(True)
        help_text.setText("Създадена от: 'ВладиКомпютърс 2000' ЕООД\nВерсия: 2.0\n© 2025 Всички права запазени.")
        layout.addWidget(help_text)
        button_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok)
        button_box.accepted.connect(self.accept)
        layout.addWidget(button_box)
        self.setLayout(layout)
