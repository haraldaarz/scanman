import sys
import subprocess
from PyQt6.QtWidgets import *

class Window(QMainWindow):
    def __init__(self):
        super().__init__(parent=None)
        self.setWindowTitle("Scanman")
        central_widget = QWidget()  # Create a central widget
        self.setCentralWidget(central_widget)  # Set the central widget for the main window

        dialogLayout = QVBoxLayout(central_widget)  # Set the layout for the central widget
        formLayout = QFormLayout()

        title_label = QLabel("<h1>Scanman</h1>")
        subtitle_label = QLabel("<h3>The comprehensive network discovery tool</h3>")
        dialogLayout.addWidget(title_label)
        dialogLayout.addWidget(subtitle_label)

        # Create input fields and store references to them as instance variables
        self.ip_address_input = QLineEdit()
        self.ports_input = QLineEdit()
        self.rate_input = QLineEdit()
        formLayout.addRow("IP address:", self.ip_address_input)
        formLayout.addRow("Ports:", self.ports_input)
        formLayout.addRow("Rate:", self.rate_input)
        dialogLayout.addLayout(formLayout)

        buttons = QDialogButtonBox()
        buttons.setStandardButtons(
            QDialogButtonBox.StandardButton.Cancel
            | QDialogButtonBox.StandardButton.Ok
        )

        buttons.accepted.connect(self.buttonOK_clicked)
        buttons.rejected.connect(self.buttonCancel_clicked)
        dialogLayout.addWidget(buttons)

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
            nmap_cmd = ["nmap", "-p", ports, "--min-rate", rate, "-oG", "scan_output.txt", ip_address]


            # Execute the nmap command and capture the output
            result = subprocess.run(nmap_cmd, capture_output=True, text=True)

            # Print the nmap output
            #print(result.stdout)

            # Open a new tab with the contents of the output file
            with open("scan_output.txt", "r") as file:
                output_data = file.read()
                self.create_output_tab(output_data)

        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}")


        # When the scan is complete, stop the subprocess




    def create_output_tab(self, content):
        # Create a new tab and add a text area to display the content
        pass

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
       # menu.addAction("&Exit", self.close)
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
        tools.addAction("Exit", self.close)
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
