import sys
import subprocess
from datetime import datetime
from PyQt6.QtWidgets import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Scanman")

        # Create a central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.setGeometry(0, 0, 850, 500)


        # Create the layout for the central widget
        self.dialogLayout = QVBoxLayout(central_widget)

        title_label = QLabel("<h1>Scanman</h1>")
        subtitle_label = QLabel("<h3>The comprehensive network discovery tool</h3>")
        self.dialogLayout.addWidget(title_label)
        self.dialogLayout.addWidget(subtitle_label)

        # Create input fields and store references to them as instance variables
        self.ip_address_input = QLineEdit()
        self.ports_input = QLineEdit()
        self.rate_input = QLineEdit()
        formLayout = QFormLayout()
        formLayout.addRow("IP address:", self.ip_address_input)
        formLayout.addRow("Ports:", self.ports_input)
        formLayout.addRow("Rate:", self.rate_input)
        self.dialogLayout.addLayout(formLayout)

        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )
        buttons.accepted.connect(self.buttonOK_clicked)
        buttons.rejected.connect(self.buttonCancel_clicked)
        self.dialogLayout.addWidget(buttons)

        # Initialize the QTabWidget
        self.tab_widget = QTabWidget()
        self.dialogLayout.addWidget(self.tab_widget)

        # Create a QLabel for the status bar
        self.status_label = QLabel("Status: Idle")
        self.statusBar().addWidget(self.status_label)


        self._createMenu()
        self._createToolBar()
        self._createStatusBar()
        
    def buttonOK_clicked(self):
        ip_address = self.ip_address_input.text()
        ports = self.ports_input.text()
        rate = self.rate_input.text()


        # Validate input (you may want to add further validation logic)
        if not ip_address or not ports or not rate:
            QMessageBox.warning(self, "Input Error", "Please fill in all the fields.")
            return


        try:
            # Construct the nmap command

            now = datetime.now()
            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
            filename = "scan_output-" + dt_string + ".txt"
            nmap_cmd = ["nmap", "-p", ports, "--min-rate", rate, "--stats-every", "1s", "-oG", filename, ip_address]

            result = subprocess.run(nmap_cmd, capture_output=True, text=True)


            # Open a new tab with the contents of the output file
            with open(filename, "r") as file:
                output_data = file.read()
                self.create_output_tab(output_data)

            #QMessageBox.information(self, "Scan complete", "The scan is complete.")
            


        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}")



    def create_output_tab(self, content):
        # Create a new tab and add a text area to display the content
        results_tab = QWidget()
        results_layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setPlainText(content)
        results_layout.addWidget(text_edit)
        results_tab.setLayout(results_layout)

        # Add the results tab to the tab widget
        self.tab_widget.addTab(results_tab, "Results")


    def buttonCancel_clicked(self):
        message = QMessageBox()
        message.setMinimumSize(700, 700)
        message.setWindowTitle("Scanman")
        message.setText("Are you sure you want to exit?")
        message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        message.setDefaultButton(QMessageBox.StandardButton.No)
        message.setIcon(QMessageBox.Icon.Warning)
        x = message.exec()
        if x == QMessageBox.StandardButton.Yes:
            self.close()

    def _createMenu(self):
        menu = self.menuBar().addMenu("&Menu")
        menu.addAction("&Exit", self.close)
        menu.addAction("&Load config", self.close)
        menu.addAction("&Save config", self.close)
        

        edit_menu = self.menuBar().addMenu("&Edit")
        edit_menu.addAction("&Undo")
        edit_menu.addAction("&Redo")

        settings_menu = self.menuBar().addMenu("&Settings")
        settings_menu.addAction("&Preferences")
        settings_menu.addAction("&About")
        

    def _createToolBar(self):
        tools = QToolBar()
       # tools.addAction("Exit", self.close)

        self.addToolBar(tools)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Status progess: Running?")
        self.setStatusBar(status)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()

    window.show()
    sys.exit(app.exec())
