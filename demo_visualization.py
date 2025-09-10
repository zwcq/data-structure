"""
Visual demonstration of the electrode array layout.

This script creates a text-based representation of the electrode array
to demonstrate the layout and functionality.
"""

import sys
from config_parser import ArrayConfigParser


def create_text_visualization():
    """Create a text-based visualization of the electrode array."""
    print("Electrode Array Visualization")
    print("=" * 60)
    
    parser = ArrayConfigParser("array.yaml")
    config = parser.parse()
    all_electrodes = parser.get_all_electrodes()
    
    # Find the bounds of the electrode grid
    positions = [e.position for e in all_electrodes]
    min_x = min(pos[0] for pos in positions)
    max_x = max(pos[0] for pos in positions)
    min_y = min(pos[1] for pos in positions)
    max_y = max(pos[1] for pos in positions)
    
    print(f"Grid dimensions: {max_x - min_x + 1} × {max_y - min_y + 1}")
    print(f"Total electrodes: {len(all_electrodes)}")
    print()
    
    # Create a grid representation
    grid = {}
    for electrode in all_electrodes:
        grid[electrode.position] = electrode
    
    # Print the grid
    print("Electrode Layout:")
    print("-" * 40)
    
    # Print column headers
    header = "   "
    for x in range(min_x, max_x + 1):
        header += f"{x:>4}"
    print(header)
    
    # Print each row
    for y in range(min_y, max_y + 1):
        row = f"{y:2d} "
        for x in range(min_x, max_x + 1):
            if (x, y) in grid:
                electrode = grid[(x, y)]
                # Use different symbols for different types
                if electrode.type == 'independent':
                    symbol = f"[{electrode.id}]"
                elif electrode.type == 'parallel':
                    symbol = f"({electrode.id[0:3]})"
                else:  # channel
                    symbol = f" {electrode.id} "
                row += f"{symbol:>4}"
            else:
                row += "    "
        print(row)
    
    print()
    print("Legend:")
    print("  [Rx]  - Independent electrodes (reservoir)")
    print("  (Px)  - Parallel electrodes (reservoir)")
    print("   Cx   - Channel electrodes (18×3 matrix)")
    print()
    
    # Show electrode type summary
    print("Electrode Summary:")
    print("-" * 20)
    
    types = {}
    for electrode in all_electrodes:
        if electrode.type not in types:
            types[electrode.type] = []
        types[electrode.type].append(electrode)
    
    for electrode_type, electrodes in types.items():
        print(f"{electrode_type.capitalize()}: {len(electrodes)} electrodes")
        if electrode_type == 'parallel':
            groups = {}
            for e in electrodes:
                if e.group_id not in groups:
                    groups[e.group_id] = []
                groups[e.group_id].append(e)
            for group_id, group_electrodes in groups.items():
                electrode_ids = [e.id for e in group_electrodes]
                print(f"  Group {group_id}: {', '.join(electrode_ids)}")
        elif electrode_type == 'channel':
            print(f"  Matrix: 18 rows × 3 columns (C1 to C54)")
        else:
            electrode_ids = [e.id for e in electrodes]
            print(f"  IDs: {', '.join(electrode_ids)}")
    
    print()
    
    # Show configuration details
    print("Configuration Details:")
    print("-" * 25)
    visual = config.visual_config
    print(f"Electrode size: {visual.get('electrode_size', 30)}px")
    print(f"Electrode spacing: {visual.get('electrode_spacing', 40)}px")
    print(f"Grid margin: {visual.get('grid_margin', 50)}px")
    
    colors = visual.get('colors', {})
    print("\nColor scheme:")
    for color_name, color_value in colors.items():
        print(f"  {color_name}: {color_value}")
    
    settings = config.settings
    print(f"\nInteraction enabled: {settings.get('click_interaction', True)}")
    print(f"Window title: {settings.get('window_title', 'N/A')}")


def demonstrate_electrode_states():
    """Demonstrate how electrode states would work."""
    print("\n" + "=" * 60)
    print("Electrode State Demonstration")
    print("=" * 60)
    
    parser = ArrayConfigParser("array.yaml")
    
    # Simulate electrode state changes
    print("Initial state: All electrodes normal")
    print("\nSimulating electrode interactions:")
    print("-" * 35)
    
    # Simulate clicking an independent electrode
    print("1. Click electrode R1 (independent)")
    print("   → R1 becomes active (red)")
    
    # Simulate clicking a parallel electrode
    print("\n2. Click electrode P1_1 (parallel group)")
    print("   → P1_1 and P1_2 both become active (synchronized)")
    
    # Simulate clicking a channel electrode
    print("\n3. Click electrode C10 (channel)")
    print("   → C10 becomes active (individual)")
    
    print("\nParallel electrode behavior:")
    print("- Clicking any electrode in a parallel group toggles the entire group")
    print("- This ensures synchronized control of related electrodes")
    
    print("\nColor coding:")
    print("  🔵 Blue - Parallel electrodes (normal state)")
    print("  🟢 Teal - Independent electrodes (normal state)")  
    print("  ⚪ Gray - Channel electrodes (normal state)")
    print("  🔴 Red  - Any electrode in active state")


def show_application_features():
    """Show the key features of the application."""
    print("\n" + "=" * 60)
    print("Application Features")
    print("=" * 60)
    
    features = [
        "✅ YAML Configuration Parsing",
        "✅ PyQt6 GUI with QPainter rendering",
        "✅ Interactive electrode clicking",
        "✅ Real-time state visualization",
        "✅ Parallel electrode synchronization",
        "✅ 18×3 channel matrix support",
        "✅ Color-coded electrode types",
        "✅ Modular, extensible architecture",
        "✅ Comprehensive testing suite",
        "✅ Detailed documentation"
    ]
    
    for feature in features:
        print(f"  {feature}")
    
    print("\nTechnical Specifications:")
    print("-" * 25)
    print("• Total Electrodes: 62")
    print("  - 4 Independent (R1-R4)")
    print("  - 4 Parallel in 2 groups (P1: P1_1,P1_2 | P2: P2_1,P2_2)")
    print("  - 54 Channel in 18×3 matrix (C1-C54)")
    print("• Framework: PyQt6")
    print("• Configuration: YAML")
    print("• Rendering: QPainter")
    print("• Testing: unittest + custom test suites")


if __name__ == "__main__":
    create_text_visualization()
    demonstrate_electrode_states()
    show_application_features()