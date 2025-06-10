import sys
from PyQt5.QtWidgets import QApplication
from modules.gui import FrenAgentGUI

def launch_gui():
    app = QApplication(sys.argv)
    window = FrenAgentGUI()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    launch_gui()