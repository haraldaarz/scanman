import sys
from PyQt6.QtWidgets import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("QDialog")
        self.setCentralWidget(QLabel("I'm the Central Widget"))

        dialogLayout = QVBoxLayout()
        formLayout = QFormLayout()
        
        title_label = QLabel("<h1>Scanman</h1>")
        subtitle_label = QLabel("<h3>The comprehensive network discovery tool</h3>")
        dialogLayout.addWidget(title_label)
        dialogLayout.addWidget(subtitle_label)

        formLayout.addRow("IP address:", QLineEdit())
        formLayout.addRow("Ports:", QLineEdit())
        formLayout.addRow("Rate:", QLineEdit())
        dialogLayout.addLayout(formLayout)

        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        dialogLayout.addWidget(buttons) 
        self.setLayout(dialogLayout)

        self._createMenu()
        self._createToolBar()
        self._createStatusBar()


    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)

    def _createToolBar(self):
        tools = QToolBar()
        tools.addAction("Exit", self.close)
        self.addToolBar(tools)


    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("I'm the Status Bar")
        self.setStatusBar(status)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
