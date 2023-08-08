import sys
import subprocess
# import ipaddress
# import socket
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
        self.rate_input.setPlaceholderText("Optional")
        self.dialogLayout.addLayout(formLayout)

        # Create checkboxes for either a TCP or UDP scan. Only one can be selected at a time, and the default is TCP. Make the boxes right next to each other.
        self.tcp_checkbox = QCheckBox("TCP")
        self.udp_checkbox = QCheckBox("UDP")
        self.tcp_checkbox.setChecked(True) # Set TCP default
        self.tcp_checkbox.toggled.connect(lambda: self.udp_checkbox.setChecked(not self.tcp_checkbox.isChecked())) # Toggle the other checkbox when this one is clicked
        self.udp_checkbox.toggled.connect(lambda: self.tcp_checkbox.setChecked(not self.udp_checkbox.isChecked())) # The same for the other checkbox
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.tcp_checkbox)
        checkbox_layout.addWidget(self.udp_checkbox)
        self.dialogLayout.addLayout(checkbox_layout)

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
        #self._createToolBar()
        self._createStatusBar()
        
    def buttonOK_clicked(self):
        ip_address = self.ip_address_input.text()
        ports = self.ports_input.text()
        rate = self.rate_input.text()
        protocol = "TCP" if self.tcp_checkbox.isChecked() else "UDP"


        # Validate input (you may want to add further validation logic)
        if not ip_address or not ports:
            QMessageBox.warning(self, "Input Error", "Please fill in IP and ports.")
            return
   

        try:
            # Construct the nmap command

            now = datetime.now()
            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
            filename = "scan_output-" + dt_string + ".txt"
    
            if rate:
                if protocol == "TCP": nmap_cmd = ["nmap", "-sV", "-p", ports, "--min-rate", rate, "--stats-every", "1s", "-oG", filename, ip_address]
                else: nmap_cmd = ["nmap", "-sU", "-p", ports, "--min-rate", rate, "--stats-every", "1s", "-oG", filename, ip_address]
            else:
                if protocol == "TCP": nmap_cmd = ["nmap", "-sV", "-p", ports, "--stats-every", "1s", "-oG", filename, ip_address]
                else: nmap_cmd = ["nmap", "-sU", "-p", ports, "--stats-every", "1s", "-oG", filename, ip_address]

            result = subprocess.run(nmap_cmd, capture_output=True, text=True)

            # Open a new tab with the contents of the output file
            with open(filename, "r") as file:
                output_data = file.read()
                self.create_output_tab(output_data, ip_address)

            #QMessageBox.information(self, "Scan complete", "The scan is complete.")


        except subprocess.CalledProcessError as e:
            QMessageBox.warning(self, "Error", f"An error occurred: {e}")

        except Exception as e:
            QMessageBox.warning(self, "Error", f"An unexpected error occurred: {e}")



    def create_output_tab(self, content, ip_address):
        # Create a new tab and add a text area to display the content
        results_tab = QWidget()
        results_layout = QVBoxLayout()
        text_edit = QTextEdit()
        text_edit.setPlainText(content)
        results_layout.addWidget(text_edit)
        results_tab.setLayout(results_layout)

        # Add the results tab to the tab widget
        self.tab_widget.addTab(results_tab, ip_address)


    def buttonCancel_clicked(self):
        pass




    # if exit button is clicked, ask if user wants to exit
    def closeEvent(self, event):
        message = QMessageBox()
        message.setMinimumSize(700, 700)
        message.setWindowTitle("Scanman")


        # if a result tab is open, ask if user wants to save the results file, then exit
        if self.tab_widget.count() > 0:
            message.setText("Would you like to save the results?")
            message.setStandardButtons(QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            message.setDefaultButton(QMessageBox.StandardButton.Yes)
            message.setIcon(QMessageBox.Icon.Warning)
            x = message.exec()
            if x == QMessageBox.StandardButton.Yes:
                self.save_results()
                event.accept()
            else:
                event.accept()
                # delete the results file
                # os.remove("scan_output.txt")


    def save_results(self):
        pass


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
        

   # def _createToolBar(self):
    #    tools = QToolBar()
       # tools.addAction("Exit", self.close)

   #     self.addToolBar(tools)

    def _createStatusBar(self):
        status = QStatusBar()
        status.showMessage("Status progess: Running?")
        self.setStatusBar(status)


if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
