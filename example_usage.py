"""
Example usage of the Electrode Array Visualization system.

This script demonstrates how to use the various components of the
electrode array system programmatically.
"""

import sys
from pathlib import Path

# Import our modules
from config_parser import ArrayConfigParser, Electrode, ElectrodeGroup

# Try to import the widget, but handle gracefully if in headless environment
try:
    from electrode_widget import ElectrodeArrayWidget
    WIDGET_AVAILABLE = True
except ImportError:
    WIDGET_AVAILABLE = False
    print("Note: GUI widget not available in this environment (headless mode)")


def example_configuration_parsing():
    """Example: Parse electrode configuration from YAML."""
    print("=== Configuration Parsing Example ===")
    
    # Create parser instance
    parser = ArrayConfigParser("array.yaml")
    
    # Parse the configuration
    config = parser.parse()
    
    print(f"Loaded configuration with:")
    print(f"  • {len(config.independent_electrodes)} independent electrodes")
    print(f"  • {len(config.parallel_groups)} parallel groups")
    print(f"  • {len(config.channel_electrodes)} channel electrodes")
    
    # Access specific electrodes
    r1 = parser.get_electrode_by_id('R1')
    print(f"\nElectrode R1: {r1.type} at position {r1.position}")
    
    # Access parallel groups
    p1_group = parser.get_parallel_group_by_id('P1')
    print(f"Parallel group P1 has {len(p1_group.electrodes)} electrodes")
    
    return config


def example_electrode_manipulation():
    """Example: Manipulate electrode states programmatically."""
    print("\n=== Electrode State Manipulation Example ===")
    
    parser = ArrayConfigParser("array.yaml")
    all_electrodes = parser.get_all_electrodes()
    
    # Create a simple state tracker
    electrode_states = {e.id: 'normal' for e in all_electrodes}
    
    print("Initial states: All electrodes are 'normal'")
    
    # Activate some electrodes
    electrode_states['R1'] = 'active'
    electrode_states['C10'] = 'active'
    
    # For parallel groups, activate all electrodes in the group
    p1_group = parser.get_parallel_group_by_id('P1')
    for electrode in p1_group.electrodes:
        electrode_states[electrode.id] = 'active'
    
    # Count active electrodes
    active_count = sum(1 for state in electrode_states.values() if state == 'active')
    print(f"\nActivated {active_count} electrodes")
    
    # Show which electrodes are active
    active_electrodes = [id for id, state in electrode_states.items() if state == 'active']
    print(f"Active electrodes: {', '.join(active_electrodes)}")
    
    return electrode_states


def example_visual_configuration():
    """Example: Access and modify visual configuration."""
    print("\n=== Visual Configuration Example ===")
    
    parser = ArrayConfigParser("array.yaml")
    config = parser.parse()
    
    # Access visual configuration
    visual = config.visual_config
    print(f"Current electrode size: {visual.get('electrode_size', 30)}px")
    print(f"Current spacing: {visual.get('electrode_spacing', 40)}px")
    
    # Access color scheme
    colors = visual.get('colors', {})
    print("\nColor scheme:")
    for color_name, color_value in colors.items():
        print(f"  {color_name}: {color_value}")
    
    # Demonstrate how you could modify colors programmatically
    modified_colors = colors.copy()
    modified_colors['active'] = '#FF0000'  # Bright red for active
    modified_colors['independent'] = '#00FF00'  # Bright green for independent
    
    print("\nModified colors:")
    print(f"  active: {modified_colors['active']}")
    print(f"  independent: {modified_colors['independent']}")
    
    return visual


def example_custom_electrode_layout():
    """Example: Create a custom electrode layout programmatically."""
    print("\n=== Custom Electrode Layout Example ===")
    
    # Create custom electrodes
    custom_electrodes = [
        Electrode(id='CUSTOM1', position=(0, 0), type='custom'),
        Electrode(id='CUSTOM2', position=(1, 0), type='custom'),
        Electrode(id='CUSTOM3', position=(0, 1), type='custom'),
        Electrode(id='CUSTOM4', position=(1, 1), type='custom'),
    ]
    
    print(f"Created {len(custom_electrodes)} custom electrodes")
    
    # Create a custom parallel group
    custom_group = ElectrodeGroup(
        group_id='CUSTOM_GROUP',
        electrodes=[custom_electrodes[0], custom_electrodes[1]],
        type='parallel'
    )
    
    print(f"Created custom parallel group with {len(custom_group.electrodes)} electrodes")
    
    # Show electrode positions
    print("Custom electrode positions:")
    for electrode in custom_electrodes:
        print(f"  {electrode.id}: {electrode.position}")
    
    return custom_electrodes


def example_integration_test():
    """Example: Integration test showing complete workflow."""
    print("\n=== Integration Test Example ===")
    
    try:
        # 1. Load configuration
        parser = ArrayConfigParser("array.yaml")
        config = parser.parse()
        print("✓ Configuration loaded successfully")
        
        # 2. Validate electrode counts
        total_expected = 4 + 4 + 54  # independent + parallel + channel
        total_actual = len(parser.get_all_electrodes())
        assert total_actual == total_expected
        print(f"✓ Electrode count validated: {total_actual} electrodes")
        
        # 3. Test electrode retrieval
        test_ids = ['R1', 'P1_1', 'C1', 'C54']
        for electrode_id in test_ids:
            electrode = parser.get_electrode_by_id(electrode_id)
            assert electrode.id == electrode_id
        print("✓ Electrode retrieval working")
        
        # 4. Test parallel group functionality
        p1_group = parser.get_parallel_group_by_id('P1')
        assert len(p1_group.electrodes) == 2
        print("✓ Parallel group functionality working")
        
        # 5. Test visual configuration
        visual = config.visual_config
        assert 'colors' in visual
        assert 'electrode_size' in visual
        print("✓ Visual configuration accessible")
        
        print("\n🎉 All integration tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Integration test failed: {str(e)}")
        return False


def example_application_usage():
    """Example: How to use the application in different ways."""
    print("\n=== Application Usage Examples ===")
    
    print("1. Run the main GUI application:")
    print("   python main.py")
    print("   python main.py custom_config.yaml")
    
    print("\n2. Run tests:")
    print("   python test_electrode_array.py")
    print("   python test_core.py")
    
    print("\n3. Parse configuration programmatically:")
    print("   from config_parser import ArrayConfigParser")
    print("   parser = ArrayConfigParser('array.yaml')")
    print("   config = parser.parse()")
    
    print("\n4. Create custom electrodes:")
    print("   from config_parser import Electrode")
    print("   electrode = Electrode(id='E1', position=(0, 0), type='custom')")
    
    print("\n5. Access electrode information:")
    print("   electrode = parser.get_electrode_by_id('R1')")
    print("   group = parser.get_parallel_group_by_id('P1')")


def main():
    """Run all examples."""
    print("Electrode Array System - Usage Examples")
    print("=" * 50)
    
    # Check if configuration file exists
    if not Path("array.yaml").exists():
        print("Error: array.yaml configuration file not found!")
        print("Please ensure the configuration file exists.")
        return False
    
    try:
        # Run examples
        example_configuration_parsing()
        example_electrode_manipulation()
        example_visual_configuration()
        example_custom_electrode_layout()
        integration_success = example_integration_test()
        example_application_usage()
        
        print("\n" + "=" * 50)
        if integration_success:
            print("✅ All examples completed successfully!")
            print("The electrode array system is ready for use.")
        else:
            print("❌ Some examples failed. Check the output above.")
        
        return integration_success
        
    except Exception as e:
        print(f"\n❌ Error running examples: {str(e)}")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)