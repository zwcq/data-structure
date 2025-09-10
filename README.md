# Electrode Array Visualization

A PyQt6-based application for visualizing and interacting with electrode arrays. This application automatically parses YAML configuration files and renders interactive electrode arrays with support for independent electrodes, parallel electrode groups, and channel matrices.

## Features

### Core Functionality
- **YAML Configuration Parsing**: Automatically loads electrode layout from `array.yaml`
- **18×3 Channel Matrix**: Displays channel electrodes in a structured 18-row, 3-column grid
- **Independent Electrodes**: Support for standalone electrodes in reservoir areas
- **Parallel Electrode Groups**: Synchronized electrode groups that change state together
- **Interactive Interface**: Click electrodes to toggle their states
- **Visual Highlighting**: Different colors for electrode types and states

### Electrode Types
1. **Independent Electrodes**: Standalone electrodes (R1, R2, R3, R4)
2. **Parallel Electrodes**: Grouped electrodes that operate together (P1, P2 groups)
3. **Channel Electrodes**: 18×3 matrix of electrodes (C1-C54)

### Visual Features
- **Color-coded electrodes**: Different colors for different types and states
- **Grid layout**: Organized electrode positioning with proper spacing
- **Coordinate display**: Shows electrode positions and IDs
- **Real-time updates**: Immediate visual feedback on state changes

## Installation

### Requirements
- Python 3.7+
- PyQt6
- PyYAML

### Setup
1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Ensure `array.yaml` configuration file exists in the project directory

## Usage

### Running the Application
```bash
python main.py
```

Or with a custom configuration file:
```bash
python main.py path/to/your/array.yaml
```

### Application Interface
- **Main Visualization Area**: Scrollable electrode array display
- **Control Panel**: Shows electrode information and active electrode list
- **Menu Bar**: File operations and help
- **Status Bar**: Real-time status updates

### Interaction
- **Click electrodes**: Toggle between normal and active states
- **Parallel groups**: Clicking any electrode in a parallel group toggles the entire group
- **Reset**: Use the "Reset All Electrodes" button to return all to normal state
- **Reload**: Refresh the configuration from file

## Configuration File (array.yaml)

The application uses a YAML configuration file to define the electrode layout:

```yaml
# Reservoir configuration
reservoir:
  independent_electrodes:
    - id: R1
      position: [0, 0]
      type: independent
  
  parallel_electrodes:
    - group_id: P1
      electrodes:
        - id: P1_1
          position: [0, 1]
        - id: P1_2
          position: [1, 1]
      type: parallel

# Channel configuration - 18 rows x 3 columns
channels:
  rows: 18
  columns: 3
  start_position: [0, 3]
  electrode_prefix: C

# Visual properties
visual:
  electrode_size: 30
  electrode_spacing: 40
  colors:
    normal: "#E0E0E0"
    active: "#FF6B6B"
    independent: "#4ECDC4"
    parallel: "#45B7D1"
```

## Project Structure

```
├── main.py                    # Main application entry point
├── electrode_widget.py        # PyQt6 visualization widget
├── config_parser.py          # YAML configuration parser
├── array.yaml                # Electrode configuration file
├── requirements.txt           # Python dependencies
├── test_electrode_array.py    # Unit tests
├── test_core.py              # Core functionality tests
└── README.md                 # This file
```

## Code Architecture

### Core Components

1. **ArrayConfigParser** (`config_parser.py`)
   - Parses YAML configuration files
   - Creates electrode and group objects
   - Provides electrode lookup functionality

2. **ElectrodeArrayWidget** (`electrode_widget.py`)
   - PyQt6 widget for electrode visualization
   - Handles mouse interactions and state management
   - Uses QPainter for custom electrode rendering

3. **ElectrodeArrayMainWindow** (`main.py`)
   - Main application window with menus and controls
   - Integrates visualization widget with control panel
   - Handles file operations and user interface

### Data Structures

- **Electrode**: Represents individual electrodes with ID, position, type, and state
- **ElectrodeGroup**: Manages parallel electrode groups
- **ArrayConfig**: Contains complete electrode array configuration

## Testing

The project includes comprehensive test suites:

### Run Unit Tests
```bash
python test_electrode_array.py
```

### Run Core Functionality Tests
```bash
python test_core.py
```

### Test Configuration Parser
```bash
python config_parser.py
```

## Customization

### Adding New Electrode Types
1. Update the YAML configuration structure
2. Modify the `ArrayConfigParser` to handle new types
3. Add rendering logic in `ElectrodeArrayWidget`
4. Update visual configuration as needed

### Changing Visual Appearance
Modify the `visual` section in `array.yaml`:
- `electrode_size`: Diameter of electrodes in pixels
- `electrode_spacing`: Distance between electrodes
- `colors`: Color scheme for different states and types

### Extending Functionality
The modular design allows easy extension:
- Add new interaction modes in `ElectrodeArrayWidget`
- Implement new configuration options in `ArrayConfigParser`
- Create additional UI components in the main window

## Troubleshooting

### Common Issues

1. **Configuration file not found**
   - Ensure `array.yaml` exists in the current directory
   - Check file path and permissions

2. **PyQt6 import errors**
   - Install PyQt6: `pip install PyQt6`
   - On Linux, may need additional packages: `apt-get install python3-pyqt6`

3. **Display issues in headless environments**
   - Use `xvfb-run` for virtual display: `xvfb-run python main.py`
   - Core functionality can be tested without GUI using `test_core.py`

### Dependencies
If you encounter missing dependencies:
```bash
pip install PyQt6 PyYAML
```

## License

This project is part of the data-structure repository and follows the same licensing terms.

## Contributing

1. Follow the existing code structure and style
2. Add tests for new functionality
3. Update documentation for any changes
4. Ensure all tests pass before submitting