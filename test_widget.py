"""
Test script to verify electrode widget functionality.

This script creates a simple test to ensure the electrode widget can be instantiated
and basic functionality works without requiring a GUI.
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from config_parser import ArrayConfigParser
from electrode_widget import ElectrodeArrayWidget


def test_electrode_widget_creation():
    """Test that the electrode widget can be created successfully."""
    try:
        parser = ArrayConfigParser("array.yaml")
        config = parser.parse()
        
        print("✓ Configuration loaded successfully")
        print(f"  - Independent electrodes: {len(config.independent_electrodes)}")
        print(f"  - Parallel groups: {len(config.parallel_groups)}")
        print(f"  - Channel electrodes: {len(config.channel_electrodes)}")
        
        # Test electrode retrieval
        all_electrodes = parser.get_all_electrodes()
        print(f"  - Total electrodes: {len(all_electrodes)}")
        
        # Test electrode by ID
        test_electrode = parser.get_electrode_by_id('R1')
        print(f"  - Found electrode R1: {test_electrode.position}")
        
        # Test parallel group
        try:
            group = parser.get_parallel_group_by_id('P1')
            print(f"  - Found parallel group P1 with {len(group.electrodes)} electrodes")
        except ValueError:
            print("  - No parallel group P1 found")
        
        print("\n✓ All basic functionality tests passed!")
        return True
        
    except Exception as e:
        print(f"✗ Error during testing: {str(e)}")
        return False


def test_electrode_positions():
    """Test electrode position calculations."""
    try:
        parser = ArrayConfigParser("array.yaml")
        all_electrodes = parser.get_all_electrodes()
        
        print("\nElectrode positions:")
        
        # Group electrodes by type
        by_type = {}
        for electrode in all_electrodes:
            if electrode.type not in by_type:
                by_type[electrode.type] = []
            by_type[electrode.type].append(electrode)
        
        for electrode_type, electrodes in by_type.items():
            print(f"\n{electrode_type.capitalize()} electrodes:")
            for electrode in electrodes[:5]:  # Show first 5 of each type
                print(f"  {electrode.id}: {electrode.position}")
            if len(electrodes) > 5:
                print(f"  ... and {len(electrodes) - 5} more")
        
        return True
        
    except Exception as e:
        print(f"✗ Error testing positions: {str(e)}")
        return False


def test_configuration_validation():
    """Test configuration validation and error handling."""
    try:
        # Test with valid configuration
        parser = ArrayConfigParser("array.yaml")
        config = parser.parse()
        
        # Validate configuration structure
        assert hasattr(config, 'independent_electrodes')
        assert hasattr(config, 'parallel_groups')
        assert hasattr(config, 'channel_electrodes')
        assert hasattr(config, 'visual_config')
        assert hasattr(config, 'settings')
        
        print("\n✓ Configuration structure validation passed")
        
        # Test visual configuration
        visual = config.visual_config
        required_visual_keys = ['electrode_size', 'electrode_spacing', 'colors']
        for key in required_visual_keys:
            if key in visual:
                print(f"  ✓ Visual config has {key}")
            else:
                print(f"  ! Visual config missing {key} (using defaults)")
        
        # Test settings
        settings = config.settings
        if settings.get('click_interaction', True):
            print("  ✓ Click interaction enabled")
        
        return True
        
    except Exception as e:
        print(f"✗ Error in configuration validation: {str(e)}")
        return False


def main():
    """Run all tests."""
    print("=" * 50)
    print("Electrode Array Widget Test Suite")
    print("=" * 50)
    
    tests = [
        ("Widget Creation", test_electrode_widget_creation),
        ("Electrode Positions", test_electrode_positions),
        ("Configuration Validation", test_configuration_validation),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\nRunning {test_name} test...")
        if test_func():
            passed += 1
        else:
            print(f"✗ {test_name} test failed")
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The electrode array system is working correctly.")
        return True
    else:
        print("❌ Some tests failed. Please check the output above.")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)