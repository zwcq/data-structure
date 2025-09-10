"""
Main PyQt6 Electrode Array Visualization Application

This is the main application that combines the configuration parser and
visualization widget to create a complete electrode array visualization interface.
"""

import sys
from pathlib import Path
from PyQt6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, 
                            QWidget, QPushButton, QLabel, QScrollArea, QFrame,
                            QStatusBar, QMenuBar, QMessageBox, QFileDialog)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon, QFont

from electrode_widget import ElectrodeArrayWidget
from config_parser import ArrayConfigParser


class ElectrodeArrayMainWindow(QMainWindow):
    """Main window for the electrode array visualization application."""
    
    def __init__(self, config_path: str = "array.yaml"):
        """Initialize the main window."""
        super().__init__()
        
        self.config_path = config_path
        self.electrode_widget = None
        
        # Initialize UI
        self.init_ui()
        
        # Load the electrode array
        self.load_array_config(config_path)
    
    def init_ui(self):
        """Initialize the user interface."""
        # Set window properties
        self.setWindowTitle("Electrode Array Visualization")
        self.setGeometry(100, 100, 1000, 700)
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Create main layout
        main_layout = QHBoxLayout(central_widget)
        
        # Create electrode visualization area (scrollable)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setMinimumWidth(600)
        main_layout.addWidget(self.scroll_area, stretch=3)
        
        # Create control panel
        control_panel = self.create_control_panel()
        main_layout.addWidget(control_panel, stretch=1)
        
        # Create menu bar
        self.create_menu_bar()
        
        # Create status bar
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_bar.showMessage("Ready")
        
        # Apply styling
        self.setStyleSheet("""
            QMainWindow {
                background-color: #f8f9fa;
            }
            QScrollArea {
                border: 1px solid #dee2e6;
                border-radius: 5px;
            }
            QFrame#controlPanel {
                background-color: #ffffff;
                border: 1px solid #dee2e6;
                border-radius: 5px;
                margin: 5px;
            }
            QPushButton {
                background-color: #007bff;
                color: white;
                border: none;
                padding: 8px 16px;
                border-radius: 4px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003d7a;
            }
            QLabel {
                color: #495057;
                font-weight: bold;
            }
        """)
    
    def create_menu_bar(self):
        """Create the application menu bar."""
        menubar = self.menuBar()
        
        # File menu
        file_menu = menubar.addMenu('File')
        
        # Load configuration action
        load_action = QAction('Load Configuration...', self)
        load_action.setShortcut('Ctrl+O')
        load_action.triggered.connect(self.load_configuration_dialog)
        file_menu.addAction(load_action)
        
        # Reload action
        reload_action = QAction('Reload', self)
        reload_action.setShortcut('F5')
        reload_action.triggered.connect(self.reload_configuration)
        file_menu.addAction(reload_action)
        
        file_menu.addSeparator()
        
        # Exit action
        exit_action = QAction('Exit', self)
        exit_action.setShortcut('Ctrl+Q')
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Help menu
        help_menu = menubar.addMenu('Help')
        
        # About action
        about_action = QAction('About', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)
    
    def create_control_panel(self):
        """Create the control panel for electrode interaction."""
        control_frame = QFrame()
        control_frame.setObjectName("controlPanel")
        control_layout = QVBoxLayout(control_frame)
        
        # Title
        title_label = QLabel("Control Panel")
        title_label.setFont(QFont("Arial", 14, QFont.Weight.Bold))
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        control_layout.addWidget(title_label)
        
        # Electrode information section
        info_label = QLabel("Electrode Information")
        info_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        control_layout.addWidget(info_label)
        
        self.electrode_info_label = QLabel("Click an electrode to see details")
        self.electrode_info_label.setWordWrap(True)
        self.electrode_info_label.setStyleSheet("background-color: #f8f9fa; padding: 10px; border: 1px solid #dee2e6; border-radius: 3px;")
        control_layout.addWidget(self.electrode_info_label)
        
        # Active electrodes section
        active_label = QLabel("Active Electrodes")
        active_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        control_layout.addWidget(active_label)
        
        self.active_electrodes_label = QLabel("None")
        self.active_electrodes_label.setWordWrap(True)
        self.active_electrodes_label.setStyleSheet("background-color: #f8f9fa; padding: 10px; border: 1px solid #dee2e6; border-radius: 3px;")
        control_layout.addWidget(self.active_electrodes_label)
        
        # Control buttons
        buttons_label = QLabel("Controls")
        buttons_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        control_layout.addWidget(buttons_label)
        
        # Reset button
        reset_button = QPushButton("Reset All Electrodes")
        reset_button.clicked.connect(self.reset_electrodes)
        control_layout.addWidget(reset_button)
        
        # Reload button
        reload_button = QPushButton("Reload Configuration")
        reload_button.clicked.connect(self.reload_configuration)
        control_layout.addWidget(reload_button)
        
        # Add stretch to push everything to the top
        control_layout.addStretch()
        
        return control_frame
    
    def load_array_config(self, config_path: str):
        """Load and display the electrode array configuration."""
        try:
            # Create electrode widget
            self.electrode_widget = ElectrodeArrayWidget(config_path)
            
            # Connect signals
            self.electrode_widget.electrode_clicked.connect(self.on_electrode_clicked)
            
            # Set the widget in the scroll area
            self.scroll_area.setWidget(self.electrode_widget)
            
            # Update status
            self.status_bar.showMessage(f"Loaded configuration: {config_path}")
            
            # Update electrode information
            self.update_electrode_info()
            
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to load configuration:\n{str(e)}")
            self.status_bar.showMessage("Failed to load configuration")
    
    def on_electrode_clicked(self, electrode_id: str):
        """Handle electrode click events."""
        if self.electrode_widget is None:
            return
        
        # Get electrode information
        try:
            electrode = self.electrode_widget.parser.get_electrode_by_id(electrode_id)
            state = self.electrode_widget.get_electrode_state(electrode_id)
            
            # Update info display
            info_text = f"ID: {electrode.id}\n"
            info_text += f"Type: {electrode.type}\n"
            info_text += f"Position: {electrode.position}\n"
            info_text += f"State: {state}\n"
            
            if electrode.group_id:
                info_text += f"Group: {electrode.group_id}\n"
            
            self.electrode_info_label.setText(info_text)
            
            # Update active electrodes list
            self.update_active_electrodes_display()
            
            # Update status bar
            self.status_bar.showMessage(f"Clicked electrode: {electrode_id} (State: {state})")
            
        except Exception as e:
            self.electrode_info_label.setText(f"Error: {str(e)}")
    
    def update_electrode_info(self):
        """Update the electrode information display."""
        if self.electrode_widget is None:
            return
        
        try:
            config = self.electrode_widget.config
            total_electrodes = len(self.electrode_widget.parser.get_all_electrodes())
            
            info_text = f"Total Electrodes: {total_electrodes}\n"
            info_text += f"Independent: {len(config.independent_electrodes)}\n"
            info_text += f"Parallel Groups: {len(config.parallel_groups)}\n"
            info_text += f"Channel Electrodes: {len(config.channel_electrodes)}\n"
            
            self.electrode_info_label.setText(info_text)
            
        except Exception as e:
            self.electrode_info_label.setText(f"Error: {str(e)}")
    
    def update_active_electrodes_display(self):
        """Update the active electrodes display."""
        if self.electrode_widget is None:
            return
        
        active_electrodes = self.electrode_widget.get_active_electrodes()
        if active_electrodes:
            self.active_electrodes_label.setText(", ".join(active_electrodes))
        else:
            self.active_electrodes_label.setText("None")
    
    def reset_electrodes(self):
        """Reset all electrodes to normal state."""
        if self.electrode_widget is not None:
            self.electrode_widget.reset_all_electrodes()
            self.update_active_electrodes_display()
            self.status_bar.showMessage("All electrodes reset to normal state")
    
    def reload_configuration(self):
        """Reload the current configuration."""
        if self.config_path:
            self.load_array_config(self.config_path)
    
    def load_configuration_dialog(self):
        """Show a dialog to load a new configuration file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Load Electrode Array Configuration",
            "",
            "YAML files (*.yaml *.yml);;All files (*)"
        )
        
        if file_path:
            self.config_path = file_path
            self.load_array_config(file_path)
    
    def show_about(self):
        """Show the about dialog."""
        QMessageBox.about(
            self,
            "About Electrode Array Visualization",
            "Electrode Array Visualization v1.0\n\n"
            "A PyQt6 application for visualizing and interacting with electrode arrays.\n"
            "Supports independent and parallel electrodes with configurable layouts.\n\n"
            "Features:\n"
            "• YAML configuration parsing\n"
            "• Interactive electrode visualization\n"
            "• Click to toggle electrode states\n"
            "• Parallel electrode synchronization\n"
            "• 18×3 channel matrix support"
        )


def main():
    """Main application entry point."""
    app = QApplication(sys.argv)
    
    # Set application properties
    app.setApplicationName("Electrode Array Visualization")
    app.setApplicationVersion("1.0")
    app.setOrganizationName("Data Structure Lab")
    
    # Check for configuration file
    config_file = "array.yaml"
    if len(sys.argv) > 1:
        config_file = sys.argv[1]
    
    # Verify configuration file exists
    if not Path(config_file).exists():
        QMessageBox.critical(
            None,
            "Configuration Error",
            f"Configuration file not found: {config_file}\n\n"
            "Please ensure array.yaml exists in the current directory."
        )
        sys.exit(1)
    
    # Create and show main window
    window = ElectrodeArrayMainWindow(config_file)
    window.show()
    
    # Start the application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()