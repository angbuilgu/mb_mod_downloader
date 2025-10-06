import sys
import os
from PyQt6.QtWidgets import QApplication
from mnb.gui.main_window import MainWindow
from mnb.utils.config import Config

def main():
    app = QApplication(sys.argv)
    config_path = os.path.join(os.getcwd(), "config.json")
    config = Config(config_path)

    main_window = MainWindow(None) # Pass None for nexus_client as it's not used
    main_window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()