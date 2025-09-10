"""
Electrode Array Visualization Widget

This module provides the main visualization widget for displaying electrode arrays
using PyQt6 and QPainter. It handles the rendering of electrodes, interaction,
and state management.
"""

import sys
from typing import Dict, List, Optional, Tuple
from PyQt6.QtWidgets import QWidget, QApplication
from PyQt6.QtCore import Qt, QRectF, QPointF, pyqtSignal
from PyQt6.QtGui import QPainter, QPen, QBrush, QColor, QFont
import math

from config_parser import ArrayConfigParser, ArrayConfig, Electrode, ElectrodeGroup


class ElectrodeArrayWidget(QWidget):
    """Widget for visualizing and interacting with electrode arrays."""
    
    # Signal emitted when an electrode is clicked
    electrode_clicked = pyqtSignal(str)  # electrode_id
    
    def __init__(self, config_path: str = "array.yaml", parent=None):
        """Initialize the electrode array widget."""
        super().__init__(parent)
        
        # Load configuration
        self.parser = ArrayConfigParser(config_path)
        self.config = self.parser.parse()
        
        # Visual settings
        self.electrode_size = self.config.visual_config.get('electrode_size', 30)
        self.electrode_spacing = self.config.visual_config.get('electrode_spacing', 40)
        self.grid_margin = self.config.visual_config.get('grid_margin', 50)
        
        # Colors
        colors = self.config.visual_config.get('colors', {})
        self.colors = {
            'normal': QColor(colors.get('normal', '#E0E0E0')),
            'active': QColor(colors.get('active', '#FF6B6B')),
            'independent': QColor(colors.get('independent', '#4ECDC4')),
            'parallel': QColor(colors.get('parallel', '#45B7D1')),
            'background': QColor(colors.get('background', '#F8F9FA')),
            'grid_line': QColor(colors.get('grid_line', '#DEE2E6')),
            'text': QColor(colors.get('text', '#495057'))
        }
        
        # Electrode states (electrode_id -> state)
        self.electrode_states = {}
        
        # Initialize all electrodes to normal state
        for electrode in self.parser.get_all_electrodes():
            self.electrode_states[electrode.id] = electrode.state
        
        # Enable mouse tracking for interaction
        self.setMouseTracking(True)
        
        # Calculate widget size based on electrode layout
        self._calculate_widget_size()
        
        # Setup UI
        self.setStyleSheet(f"background-color: {colors.get('background', '#F8F9FA')};")
        
    def _calculate_widget_size(self):
        """Calculate the required widget size based on electrode positions."""
        all_electrodes = self.parser.get_all_electrodes()
        
        if not all_electrodes:
            self.setMinimumSize(400, 300)
            return
        
        # Find the maximum position coordinates
        max_x = max(electrode.position[0] for electrode in all_electrodes)
        max_y = max(electrode.position[1] for electrode in all_electrodes)
        
        # Calculate required size
        width = (max_x + 1) * self.electrode_spacing + 2 * self.grid_margin + 100  # Extra space for labels
        height = (max_y + 1) * self.electrode_spacing + 2 * self.grid_margin + 100
        
        self.setMinimumSize(int(width), int(height))
    
    def _electrode_position_to_pixel(self, grid_pos: Tuple[int, int]) -> QPointF:
        """Convert electrode grid position to pixel coordinates."""
        x = self.grid_margin + grid_pos[0] * self.electrode_spacing
        y = self.grid_margin + grid_pos[1] * self.electrode_spacing
        return QPointF(x, y)
    
    def _pixel_to_electrode_position(self, pixel_pos: QPointF) -> Optional[Tuple[int, int]]:
        """Convert pixel coordinates to electrode grid position."""
        grid_x = round((pixel_pos.x() - self.grid_margin) / self.electrode_spacing)
        grid_y = round((pixel_pos.y() - self.grid_margin) / self.electrode_spacing)
        return (grid_x, grid_y)
    
    def _find_electrode_at_position(self, grid_pos: Tuple[int, int]) -> Optional[Electrode]:
        """Find the electrode at the given grid position."""
        all_electrodes = self.parser.get_all_electrodes()
        for electrode in all_electrodes:
            if electrode.position == grid_pos:
                return electrode
        return None
    
    def paintEvent(self, event):
        """Paint the electrode array."""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        
        # Draw background
        painter.fillRect(self.rect(), QBrush(self.colors['background']))
        
        # Draw section labels
        self._draw_section_labels(painter)
        
        # Draw electrodes
        self._draw_electrodes(painter)
        
        # Draw grid lines (optional)
        self._draw_grid_lines(painter)
    
    def _draw_section_labels(self, painter: QPainter):
        """Draw labels for different sections (reservoir, channels)."""
        painter.setPen(QPen(self.colors['text'], 2))
        font = QFont("Arial", 12, QFont.Weight.Bold)
        painter.setFont(font)
        
        # Reservoir label
        reservoir_y = self.grid_margin - 20
        painter.drawText(self.grid_margin, reservoir_y, "Reservoir Area")
        
        # Channel label
        channel_start_y = self.grid_margin + self.config.channel_config.get('start_position', [0, 3])[1] * self.electrode_spacing - 20
        painter.drawText(self.grid_margin, channel_start_y, "Channel Area (18×3 Matrix)")
    
    def _draw_electrodes(self, painter: QPainter):
        """Draw all electrodes with their current states."""
        # Draw independent electrodes
        for electrode in self.config.independent_electrodes:
            self._draw_electrode(painter, electrode, 'independent')
        
        # Draw parallel electrode groups
        for group in self.config.parallel_groups:
            for electrode in group.electrodes:
                self._draw_electrode(painter, electrode, 'parallel')
        
        # Draw channel electrodes
        for electrode in self.config.channel_electrodes:
            self._draw_electrode(painter, electrode, 'normal')
    
    def _draw_electrode(self, painter: QPainter, electrode: Electrode, base_type: str):
        """Draw a single electrode."""
        # Get pixel position
        pixel_pos = self._electrode_position_to_pixel(electrode.position)
        
        # Determine color based on state and type
        state = self.electrode_states.get(electrode.id, 'normal')
        if state == 'active':
            color = self.colors['active']
        elif base_type == 'independent':
            color = self.colors['independent']
        elif base_type == 'parallel':
            color = self.colors['parallel']
        else:
            color = self.colors['normal']
        
        # Draw electrode circle
        radius = self.electrode_size / 2
        electrode_rect = QRectF(
            pixel_pos.x() - radius,
            pixel_pos.y() - radius,
            self.electrode_size,
            self.electrode_size
        )
        
        # Set brush and pen
        painter.setBrush(QBrush(color))
        painter.setPen(QPen(QColor('#000000'), 1))
        
        # Draw the electrode
        painter.drawEllipse(electrode_rect)
        
        # Draw electrode ID
        painter.setPen(QPen(self.colors['text'], 1))
        font = QFont("Arial", 8)
        painter.setFont(font)
        
        # Center the text
        text_rect = painter.fontMetrics().boundingRect(electrode.id)
        text_x = pixel_pos.x() - text_rect.width() / 2
        text_y = pixel_pos.y() + text_rect.height() / 4
        
        painter.drawText(QPointF(text_x, text_y), electrode.id)
    
    def _draw_grid_lines(self, painter: QPainter):
        """Draw optional grid lines for reference."""
        painter.setPen(QPen(self.colors['grid_line'], 1, Qt.PenStyle.DotLine))
        
        # Find the range of electrode positions
        all_electrodes = self.parser.get_all_electrodes()
        if not all_electrodes:
            return
        
        min_x = min(electrode.position[0] for electrode in all_electrodes)
        max_x = max(electrode.position[0] for electrode in all_electrodes)
        min_y = min(electrode.position[1] for electrode in all_electrodes)
        max_y = max(electrode.position[1] for electrode in all_electrodes)
        
        # Draw vertical grid lines
        for x in range(min_x, max_x + 1):
            start_y = self.grid_margin + min_y * self.electrode_spacing
            end_y = self.grid_margin + max_y * self.electrode_spacing
            painter.drawLine(
                QPointF(self.grid_margin + x * self.electrode_spacing, start_y),
                QPointF(self.grid_margin + x * self.electrode_spacing, end_y)
            )
        
        # Draw horizontal grid lines
        for y in range(min_y, max_y + 1):
            start_x = self.grid_margin + min_x * self.electrode_spacing
            end_x = self.grid_margin + max_x * self.electrode_spacing
            painter.drawLine(
                QPointF(start_x, self.grid_margin + y * self.electrode_spacing),
                QPointF(end_x, self.grid_margin + y * self.electrode_spacing)
            )
    
    def mousePressEvent(self, event):
        """Handle mouse press events for electrode interaction."""
        if not self.config.settings.get('click_interaction', True):
            return
        
        if event.button() == Qt.MouseButton.LeftButton:
            # Convert click position to grid position
            click_pos = QPointF(event.position().x(), event.position().y())
            grid_pos = self._pixel_to_electrode_position(click_pos)
            
            # Find electrode at this position
            electrode = self._find_electrode_at_position(grid_pos)
            if electrode:
                self._toggle_electrode_state(electrode)
                self.electrode_clicked.emit(electrode.id)
                self.update()  # Repaint the widget
    
    def _toggle_electrode_state(self, electrode: Electrode):
        """Toggle the state of an electrode between normal and active."""
        current_state = self.electrode_states.get(electrode.id, 'normal')
        new_state = 'active' if current_state == 'normal' else 'normal'
        
        # For parallel electrodes, toggle all electrodes in the group
        if electrode.group_id:
            try:
                group = self.parser.get_parallel_group_by_id(electrode.group_id)
                for group_electrode in group.electrodes:
                    self.electrode_states[group_electrode.id] = new_state
            except ValueError:
                # If group not found, just toggle the individual electrode
                self.electrode_states[electrode.id] = new_state
        else:
            # Individual electrode
            self.electrode_states[electrode.id] = new_state
    
    def set_electrode_state(self, electrode_id: str, state: str):
        """Set the state of a specific electrode."""
        if electrode_id in self.electrode_states:
            self.electrode_states[electrode_id] = state
            self.update()
    
    def get_electrode_state(self, electrode_id: str) -> str:
        """Get the current state of an electrode."""
        return self.electrode_states.get(electrode_id, 'normal')
    
    def get_active_electrodes(self) -> List[str]:
        """Get a list of all active electrode IDs."""
        return [electrode_id for electrode_id, state in self.electrode_states.items() if state == 'active']
    
    def reset_all_electrodes(self):
        """Reset all electrodes to normal state."""
        for electrode_id in self.electrode_states:
            self.electrode_states[electrode_id] = 'normal'
        self.update()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    widget = ElectrodeArrayWidget("array.yaml")
    widget.setWindowTitle("Electrode Array Visualization Test")
    widget.show()
    
    sys.exit(app.exec())