import sys
import subprocess
import os
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
        self.vuln_checkbox = QCheckBox("Vulnerability Scan")
        self.tcp_checkbox.setChecked(True) # Set TCP default

        # Both tcp and udp cant be checked at the same time, and vuln scan can only be checked if tcp is checked
        self.tcp_checkbox.toggled.connect(lambda: self.udp_checkbox.setChecked(False))
        self.udp_checkbox.toggled.connect(lambda: self.tcp_checkbox.setChecked(False))
        self.tcp_checkbox.toggled.connect(lambda: self.vuln_checkbox.setEnabled(self.tcp_checkbox.isChecked()))
        self.udp_checkbox.toggled.connect(lambda: self.vuln_checkbox.setEnabled(self.tcp_checkbox.isChecked()))

        # Add the checkboxes to a horizontal layout
        checkbox_layout = QHBoxLayout()
        checkbox_layout.addWidget(self.tcp_checkbox)
        checkbox_layout.addWidget(self.udp_checkbox)
        checkbox_layout.addWidget(self.vuln_checkbox)
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
        vuln_scan = self.vuln_checkbox.isChecked()


        # Validate input (you may want to add further validation logic)
        if not ip_address or not ports:
            QMessageBox.warning(self, "Input Error", "Please fill in IP and ports.")
            return
   

        try:
            # Construct the nmap command

            now = datetime.now()
            dt_string = now.strftime("%d-%m-%Y-%H-%M-%S")
            filename = "scan_output-" + dt_string + ".txt"
    
            nmap_cmd = ["nmap", "-sV", "-p", ports, "--stats-every", "1s", "-oG", filename]

            if rate:
                nmap_cmd.extend(["--min-rate", rate])

            if vuln_scan:
                nmap_cmd.extend(["--script=vulners"])

            if protocol == "TCP":
                nmap_cmd.append(ip_address)
            else:
                nmap_cmd.extend(["-sU", ip_address])

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
        # TODO
        pass




    def closeEvent(self, event):
        if self.tab_widget.count() > 0:
            message = QMessageBox()
            message.setMinimumSize(700, 700)
            message.setWindowTitle("Scanman")
            message.setText("Would you like to save the results?")
            message.setStandardButtons(
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            message.setDefaultButton(QMessageBox.StandardButton.Yes)
            message.setIcon(QMessageBox.Icon.Warning)
            x = message.exec()
            if x == QMessageBox.StandardButton.Yes: # if yes
                current_tab_index = self.tab_widget.currentIndex() # get current tab index
                current_tab = self.tab_widget.widget(current_tab_index) # get current tab
                text_edit = current_tab.layout().itemAt(0).widget() # get text edit widget
                self.save_results(text_edit.toPlainText()) # save the results of the text edit widget to a file, using the save_results function
                event.accept()
            else:
                event.accept()
                # TODO: Delete the output files


    def save_results(self, content):
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save Results",
            "",
            "Text Files (*.txt);;All Files (*)"
        )

        if file_name:
            with open(file_name, "w") as file:
                file.write(content)

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
