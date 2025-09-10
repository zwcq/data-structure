"""
Test script for core electrode array functionality without GUI components.

This script tests the configuration parser and core logic without requiring
PyQt6 GUI components, which may not be available in headless environments.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from config_parser import ArrayConfigParser, Electrode, ElectrodeGroup


def test_configuration_parsing():
    """Test the configuration parsing functionality."""
    print("Testing configuration parsing...")
    
    try:
        parser = ArrayConfigParser("array.yaml")
        config = parser.parse()
        
        print("✓ Configuration loaded successfully")
        print(f"  - Independent electrodes: {len(config.independent_electrodes)}")
        print(f"  - Parallel groups: {len(config.parallel_groups)}")
        print(f"  - Channel electrodes: {len(config.channel_electrodes)}")
        
        # Validate expected structure
        assert len(config.independent_electrodes) == 4
        assert len(config.parallel_groups) == 2
        assert len(config.channel_electrodes) == 54  # 18x3 matrix
        
        print("✓ Configuration structure validated")
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_electrode_retrieval():
    """Test electrode retrieval functionality."""
    print("\nTesting electrode retrieval...")
    
    try:
        parser = ArrayConfigParser("array.yaml")
        
        # Test getting all electrodes
        all_electrodes = parser.get_all_electrodes()
        expected_total = 4 + 4 + 54  # independent + parallel + channel
        assert len(all_electrodes) == expected_total
        print(f"✓ Found {len(all_electrodes)} total electrodes")
        
        # Test getting specific electrodes
        r1 = parser.get_electrode_by_id('R1')
        assert r1.id == 'R1'
        assert r1.type == 'independent'
        print("✓ Retrieved independent electrode R1")
        
        c1 = parser.get_electrode_by_id('C1')
        assert c1.id == 'C1'
        assert c1.type == 'channel'
        print("✓ Retrieved channel electrode C1")
        
        # Test parallel group retrieval
        p1_group = parser.get_parallel_group_by_id('P1')
        assert p1_group.group_id == 'P1'
        assert len(p1_group.electrodes) == 2
        print("✓ Retrieved parallel group P1")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_electrode_positions():
    """Test electrode position logic."""
    print("\nTesting electrode positions...")
    
    try:
        parser = ArrayConfigParser("array.yaml")
        all_electrodes = parser.get_all_electrodes()
        
        # Check that all positions are unique
        positions = [e.position for e in all_electrodes]
        unique_positions = set(positions)
        assert len(positions) == len(unique_positions)
        print("✓ All electrode positions are unique")
        
        # Check channel electrode arrangement (18x3 matrix)
        channel_electrodes = [e for e in all_electrodes if e.type == 'channel']
        channel_positions = [e.position for e in channel_electrodes]
        
        # Channel electrodes should start at position [0, 3] and form an 18x3 grid
        min_x = min(pos[0] for pos in channel_positions)
        max_x = max(pos[0] for pos in channel_positions)
        min_y = min(pos[1] for pos in channel_positions)
        max_y = max(pos[1] for pos in channel_positions)
        
        # Should span 3 columns (0, 1, 2) and 18 rows
        assert max_x - min_x == 2  # 3 columns
        assert max_y - min_y == 17  # 18 rows
        print("✓ Channel electrode matrix dimensions correct")
        
        # Check that electrode IDs are sequential for channels
        channel_ids = [int(e.id[1:]) for e in channel_electrodes]  # Remove 'C' prefix
        channel_ids.sort()
        expected_ids = list(range(1, 55))  # C1 to C54
        assert channel_ids == expected_ids
        print("✓ Channel electrode IDs are sequential")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_parallel_electrode_logic():
    """Test parallel electrode group logic."""
    print("\nTesting parallel electrode logic...")
    
    try:
        parser = ArrayConfigParser("array.yaml")
        config = parser.parse()
        
        # Test that parallel electrodes have correct group assignments
        for group in config.parallel_groups:
            for electrode in group.electrodes:
                assert electrode.group_id == group.group_id
                assert electrode.type == 'parallel'
            print(f"✓ Parallel group {group.group_id} configured correctly")
        
        # Test that we can find parallel groups
        p1_group = parser.get_parallel_group_by_id('P1')
        p2_group = parser.get_parallel_group_by_id('P2')
        
        assert len(p1_group.electrodes) == 2
        assert len(p2_group.electrodes) == 2
        print("✓ Both parallel groups found with correct electrode counts")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def test_visual_configuration():
    """Test visual configuration parsing."""
    print("\nTesting visual configuration...")
    
    try:
        parser = ArrayConfigParser("array.yaml")
        config = parser.parse()
        
        visual = config.visual_config
        
        # Check required visual properties
        assert 'electrode_size' in visual
        assert 'electrode_spacing' in visual
        assert 'colors' in visual
        
        # Check color configuration
        colors = visual['colors']
        required_colors = ['normal', 'active', 'independent', 'parallel', 'background']
        for color in required_colors:
            assert color in colors
            # Check that colors are valid hex values
            assert colors[color].startswith('#')
            assert len(colors[color]) == 7
        
        print("✓ Visual configuration validated")
        
        # Check settings
        settings = config.settings
        assert 'window_title' in settings
        assert 'click_interaction' in settings
        print("✓ Application settings validated")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def demonstrate_electrode_layout():
    """Demonstrate the electrode layout structure."""
    print("\nElectrode Layout Demonstration:")
    print("=" * 40)
    
    try:
        parser = ArrayConfigParser("array.yaml")
        all_electrodes = parser.get_all_electrodes()
        
        # Group by type for display
        by_type = {}
        for electrode in all_electrodes:
            if electrode.type not in by_type:
                by_type[electrode.type] = []
            by_type[electrode.type].append(electrode)
        
        # Display each type
        for electrode_type, electrodes in by_type.items():
            print(f"\n{electrode_type.upper()} ELECTRODES:")
            print("-" * 30)
            
            if electrode_type == 'channel':
                # Show channel matrix structure
                print("18×3 Channel Matrix (showing first few rows):")
                channels_by_row = {}
                for electrode in electrodes:
                    row = electrode.position[1] - 3  # Channel starts at y=3
                    if row not in channels_by_row:
                        channels_by_row[row] = []
                    channels_by_row[row].append(electrode)
                
                # Show first 3 rows
                for row in sorted(channels_by_row.keys())[:3]:
                    row_electrodes = sorted(channels_by_row[row], key=lambda e: e.position[0])
                    row_str = " ".join(f"{e.id:>3}" for e in row_electrodes)
                    print(f"Row {row:2d}: {row_str}")
                print(f"... (continues for {len(channels_by_row)} rows total)")
                
            else:
                # Show other electrode types
                for electrode in electrodes:
                    group_info = f" (Group: {electrode.group_id})" if electrode.group_id else ""
                    print(f"  {electrode.id}: Position {electrode.position}{group_info}")
        
        return True
        
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False


def main():
    """Run all core functionality tests."""
    print("=" * 60)
    print("Electrode Array Core Functionality Test Suite")
    print("=" * 60)
    
    tests = [
        ("Configuration Parsing", test_configuration_parsing),
        ("Electrode Retrieval", test_electrode_retrieval),
        ("Electrode Positions", test_electrode_positions),
        ("Parallel Electrode Logic", test_parallel_electrode_logic),
        ("Visual Configuration", test_visual_configuration),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} test failed")
    
    # Run demonstration
    demonstrate_electrode_layout()
    
    print("\n" + "=" * 60)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All core functionality tests passed!")
        print("\nThe electrode array system is ready for GUI integration.")
        print("Key features validated:")
        print("  ✓ YAML configuration parsing")
        print("  ✓ 18×3 channel electrode matrix")
        print("  ✓ Independent electrode support")
        print("  ✓ Parallel electrode group support")
        print("  ✓ Visual configuration")
        print("  ✓ Unique electrode positioning")
        return True
    else:
        print("❌ Some tests failed. Please check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)