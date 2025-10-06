import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLineEdit, QPushButton, QListWidget, QListWidgetItem, QTextEdit, QLabel, QStatusBar, QFileDialog, QComboBox, QStackedWidget, QInputDialog
)
from PyQt6.QtGui import QDesktopServices
from mnb.utils.mod_list_manager import ModListManager
from PyQt6.QtCore import Qt, QUrl

class MainWindow(QMainWindow):
    """The main window of the application."""

    def __init__(self, nexus_client):
        super().__init__()
        self.mod_list_manager = ModListManager() # Instantiate ModListManager
        self.setWindowTitle("Mount & Blade Mod Downloader")
        self.setGeometry(100, 100, 800, 600)

        # --- Central Widget and Layouts ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QVBoxLayout(central_widget)

        # --- Initial Buttons ---
        initial_buttons_layout = QHBoxLayout()
        self.export_mode_button = QPushButton("Export Mods")
        self.import_mode_button = QPushButton("Import Mods")
        initial_buttons_layout.addWidget(self.export_mode_button)
        initial_buttons_layout.addWidget(self.import_mode_button)
        main_layout.addLayout(initial_buttons_layout)

        # --- Stacked Widget for different views ---
        self.stacked_widget = QStackedWidget()
        main_layout.addWidget(self.stacked_widget)

        # --- Export View ---
        self.export_widget = QWidget()
        self.export_layout = QVBoxLayout(self.export_widget)
        self.stacked_widget.addWidget(self.export_widget)

        # --- Import View ---
        self.import_widget = QWidget()
        self.import_layout = QVBoxLayout(self.import_widget)
        self.stacked_widget.addWidget(self.import_widget)

        self._setup_export_ui()
        self._setup_import_ui()

        # --- Status Bar ---
        self.setStatusBar(QStatusBar(self))
        self.statusBar().showMessage("Ready. Select Export or Import.")

        # --- Connections ---
        self.export_mode_button.clicked.connect(self._show_export_view)
        self.import_mode_button.clicked.connect(self._show_import_view)

        # Initially show the main buttons
        self.stacked_widget.setCurrentWidget(self.export_widget) # Default to export view for now, will adjust later

    def _setup_export_ui(self):
        # Input fields for Mod ID and File ID
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Mod ID:"))
        self.export_mod_id_input = QLineEdit()
        self.export_mod_id_input.setPlaceholderText("Enter Mod ID")
        input_layout.addWidget(self.export_mod_id_input)

        input_layout.addWidget(QLabel("File ID:"))
        self.export_file_id_input = QLineEdit()
        self.export_file_id_input.setPlaceholderText("Enter File ID")
        input_layout.addWidget(self.export_file_id_input)

        self.add_to_export_list_button = QPushButton("Add to List")
        input_layout.addWidget(self.add_to_export_list_button)
        self.export_layout.addLayout(input_layout)

        # Display for exported mods
        self.export_list_widget = QListWidget()
        self.export_list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.export_layout.addWidget(self.export_list_widget)

        # Buttons for export functionality
        export_buttons_layout = QHBoxLayout()
        self.export_list_file_button = QPushButton("Export List to File")
        self.clear_export_list_button = QPushButton("Clear List")
        self.delete_selected_mod_button = QPushButton("Delete Selected Mod")
        self.edit_mod_name_button = QPushButton("Edit Mod Name")
        export_buttons_layout.addWidget(self.export_list_file_button)
        export_buttons_layout.addWidget(self.clear_export_list_button)
        export_buttons_layout.addWidget(self.delete_selected_mod_button)
        export_buttons_layout.addWidget(self.edit_mod_name_button)
        self.export_layout.addLayout(export_buttons_layout)

        # Connections for export UI
        self.add_to_export_list_button.clicked.connect(self._add_mod_to_export_list)
        self.export_list_file_button.clicked.connect(self.export_mod_list)
        self.clear_export_list_button.clicked.connect(self.clear_export_list)
        self.delete_selected_mod_button.clicked.connect(self._delete_selected_mod_from_export_list)
        self.edit_mod_name_button.clicked.connect(self._edit_selected_mod_name)

    def _setup_import_ui(self):
        # Import file selection
        import_file_layout = QHBoxLayout()
        self.import_file_path_display = QLineEdit()
        self.import_file_path_display.setReadOnly(True)
        import_file_layout.addWidget(self.import_file_path_display)
        self.browse_import_file_button = QPushButton("Browse...")
        import_file_layout.addWidget(self.browse_import_file_button)
        self.import_layout.addLayout(import_file_layout)

        # Display for imported mods
        self.import_list_widget = QListWidget()
        self.import_list_widget.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        self.import_layout.addWidget(self.import_list_widget)

        # Buttons for import functionality
        import_buttons_layout = QHBoxLayout()
        self.import_list_file_button = QPushButton("Import List from File")
        self.open_all_downloads_button = QPushButton("Open All Mod Download Pages")
        self.open_selected_downloads_button = QPushButton("Open Selected Mod Download Pages")
        import_buttons_layout.addWidget(self.import_list_file_button)
        import_buttons_layout.addWidget(self.open_all_downloads_button)
        import_buttons_layout.addWidget(self.open_selected_downloads_button)
        self.import_layout.addLayout(import_buttons_layout)

        # Connections for import UI
        self.browse_import_file_button.clicked.connect(self._browse_import_file)
        self.import_list_file_button.clicked.connect(self.import_mod_list)
        self.open_all_downloads_button.clicked.connect(self.open_all_downloads)
        self.open_selected_downloads_button.clicked.connect(self._open_selected_downloads)

    def _show_export_view(self):
        self.stacked_widget.setCurrentWidget(self.export_widget)
        self.statusBar().showMessage("Export Mode: Enter Mod and File IDs to build your list.")
        self._update_export_list_display() # Refresh display when switching views

    def _show_import_view(self):
        self.stacked_widget.setCurrentWidget(self.import_widget)
        self.statusBar().showMessage("Import Mode: Load a mod list from a file.")
        self.import_list_widget.clear() # Clear previous import display

    def _add_mod_to_export_list(self):
        mod_id_text = self.export_mod_id_input.text().strip()
        file_id_text = self.export_file_id_input.text().strip()

        if not mod_id_text or not file_id_text:
            self.statusBar().showMessage("Please enter both Mod ID and File ID.")
            return

        try:
            mod_id = int(mod_id_text)
            file_id = int(file_id_text)
        except ValueError:
            self.statusBar().showMessage("Mod ID and File ID must be integers.")
            return
        
        # In this simplified version, we don't fetch mod names. Use a placeholder.
        file_name = f"Mod_{mod_id}_File_{file_id}"
        game_domain = "mountandblade2bannerlord" # Default game domain

        self.mod_list_manager.add_mod(game_domain, mod_id, file_id, file_name)
        self._update_export_list_display()
        self.statusBar().showMessage(f"Added {file_name} to export list.")
        self.export_mod_id_input.clear()
        self.export_file_id_input.clear()

    def _delete_selected_mod_from_export_list(self):
        selected_items = self.export_list_widget.selectedItems()
        if not selected_items:
            self.statusBar().showMessage("Please select at least one mod to delete from the export list.")
            return
        
        for item in selected_items:
            mod_info = item.data(Qt.ItemDataRole.UserRole)
            if mod_info:
                self.mod_list_manager.remove_mod(mod_info['mod_id'], mod_info['file_id'])
                self.statusBar().showMessage(f"Removed {mod_info['file_name']} from export list.")
        self._update_export_list_display()

    def _browse_import_file(self):
        filepath, _ = QFileDialog.getOpenFileName(self, "Select Mod List File", "", "JSON Files (*.json);;All Files (*)")
        if filepath:
            self.import_file_path_display.setText(filepath)
            self.statusBar().showMessage(f"Selected file: {filepath}")

    def _edit_selected_mod_name(self):
        selected_items = self.export_list_widget.selectedItems()
        if not selected_items:
            self.statusBar().showMessage("Please select a mod to edit its name.")
            return
        if len(selected_items) > 1:
            self.statusBar().showMessage("Please select only one mod to edit its name.")
            return

        selected_item = selected_items[0]
        mod_info = selected_item.data(Qt.ItemDataRole.UserRole)
        if not mod_info:
            return

        current_name = mod_info.get('file_name', '')
        new_name, ok = QInputDialog.getText(self, "Edit Mod Name", "Enter new name for the mod:", QLineEdit.EchoMode.Normal, current_name)

        if ok and new_name and new_name != current_name:
            mod_id = mod_info['mod_id']
            file_id = mod_info['file_id']
            self.mod_list_manager.update_mod_name(mod_id, file_id, new_name)
            self._update_export_list_display()
            self.statusBar().showMessage(f"Mod name updated to: {new_name}")
        elif ok and not new_name:
            self.statusBar().showMessage("Mod name cannot be empty.")

    def import_mod_list(self):
        filepath = self.import_file_path_display.text().strip()
        if not filepath:
            self.statusBar().showMessage("Please select a file to import.")
            return

        try:
            self.mod_list_manager.import_from_file(filepath)
            self._update_import_list_display()
            self.statusBar().showMessage(f"Mod list imported from {filepath}")
        except Exception as e:
            self.statusBar().showMessage(f"Error importing mod list: {e}")

    def _update_import_list_display(self):
        self.import_list_widget.clear()
        for mod_info in self.mod_list_manager.get_mod_list():
            item_text = f"{mod_info['file_name']} (Mod ID: {mod_info['mod_id']}, File ID: {mod_info['file_id']})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, mod_info)
            self.import_list_widget.addItem(item)

    def _open_selected_downloads(self):
        selected_items = self.import_list_widget.selectedItems()
        if not selected_items:
            self.statusBar().showMessage("Please select mods to open their download pages.")
            return

        for item in selected_items:
            mod_info = item.data(Qt.ItemDataRole.UserRole)
            if mod_info:
                game_domain = mod_info.get('game_domain')
                mod_id = mod_info.get('mod_id')
                file_id_int = mod_info.get('file_id')

                if all([game_domain, mod_id, file_id_int]):
                    nexus_url = f"https://www.nexusmods.com/{game_domain}/mods/{mod_id}?tab=files&file_id={file_id_int}"
                    QDesktopServices.openUrl(QUrl(nexus_url))
                    self.statusBar().showMessage(f"Opening {mod_info['file_name']} in browser...")
                else:
                    self.statusBar().showMessage(f"Skipping {mod_info.get('file_name', 'unknown mod')} due to missing data.")
        self.statusBar().showMessage("Selected mod pages opened in browser.")

    def clear_export_list(self):
        self.mod_list_manager.clear_list()
        self._update_export_list_display()
        self.statusBar().showMessage("Export list cleared.")

    def _update_export_list_display(self):
        self.export_list_widget.clear()
        for mod_info in self.mod_list_manager.get_mod_list():
            item_text = f"{mod_info['file_name']} (Mod ID: {mod_info['mod_id']}, File ID: {mod_info['file_id']})"
            item = QListWidgetItem(item_text)
            item.setData(Qt.ItemDataRole.UserRole, mod_info)
            self.export_list_widget.addItem(item)

    def export_mod_list(self):
        if not self.mod_list_manager.get_mod_list():
            self.statusBar().showMessage("Export list is empty.")
            return

        filepath, _ = QFileDialog.getSaveFileName(self, "Export Mod List", "", "JSON Files (*.json);;All Files (*)")
        if filepath:
            try:
                self.mod_list_manager.export_to_file(filepath)
                self.statusBar().showMessage(f"Mod list exported to {filepath}")
            except Exception as e:
                self.statusBar().showMessage(f"Error exporting mod list: {e}")

    def open_all_downloads(self):
        mod_list = self.mod_list_manager.get_mod_list()
        if not mod_list:
            self.statusBar().showMessage("Export list is empty. Nothing to open.")
            return

        for mod_info in mod_list:
            game_domain = mod_info.get('game_domain')
            mod_id = mod_info.get('mod_id')
            file_id_int = mod_info.get('file_id')

            if all([game_domain, mod_id, file_id_int]):
                nexus_url = f"https://www.nexusmods.com/{game_domain}/mods/{mod_id}?tab=files&file_id={file_id_int}"
                QDesktopServices.openUrl(QUrl(nexus_url))
                self.statusBar().showMessage(f"Opening {mod_info['file_name']} in browser...")
            else:
                self.statusBar().showMessage(f"Skipping {mod_info.get('file_name', 'unknown mod')} due to missing data.")
        self.statusBar().showMessage("All available mod pages opened in browser.")