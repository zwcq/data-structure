"""
Test cases for the Electrode Array Visualization application.

This module contains unit tests for the configuration parser, electrode widget,
and main application functionality.
"""

import unittest
import tempfile
import os
from pathlib import Path
import yaml

from config_parser import ArrayConfigParser, Electrode, ElectrodeGroup, ArrayConfig


class TestArrayConfigParser(unittest.TestCase):
    """Test cases for the ArrayConfigParser class."""
    
    def setUp(self):
        """Set up test configuration data."""
        self.test_config = {
            'reservoir': {
                'independent_electrodes': [
                    {'id': 'R1', 'position': [0, 0], 'type': 'independent'},
                    {'id': 'R2', 'position': [1, 0], 'type': 'independent'}
                ],
                'parallel_electrodes': [
                    {
                        'group_id': 'P1',
                        'electrodes': [
                            {'id': 'P1_1', 'position': [0, 1]},
                            {'id': 'P1_2', 'position': [1, 1]}
                        ],
                        'type': 'parallel'
                    }
                ]
            },
            'channels': {
                'rows': 2,
                'columns': 2,
                'start_position': [0, 3],
                'electrode_prefix': 'C'
            },
            'visual': {
                'electrode_size': 30,
                'electrode_spacing': 40,
                'colors': {
                    'normal': '#E0E0E0',
                    'active': '#FF6B6B'
                }
            },
            'settings': {
                'window_title': 'Test Window',
                'click_interaction': True
            }
        }
        
        # Create temporary config file
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.yaml', delete=False)
        yaml.dump(self.test_config, self.temp_file)
        self.temp_file.close()
        self.config_path = self.temp_file.name
    
    def tearDown(self):
        """Clean up temporary files."""
        os.unlink(self.config_path)
    
    def test_load_config(self):
        """Test loading configuration from YAML file."""
        parser = ArrayConfigParser(self.config_path)
        config_data = parser.load_config()
        
        self.assertIsInstance(config_data, dict)
        self.assertIn('reservoir', config_data)
        self.assertIn('channels', config_data)
        self.assertIn('visual', config_data)
        self.assertIn('settings', config_data)
    
    def test_parse_independent_electrodes(self):
        """Test parsing independent electrodes."""
        parser = ArrayConfigParser(self.config_path)
        config = parser.parse()
        
        self.assertEqual(len(config.independent_electrodes), 2)
        
        electrode1 = config.independent_electrodes[0]
        self.assertEqual(electrode1.id, 'R1')
        self.assertEqual(electrode1.position, (0, 0))
        self.assertEqual(electrode1.type, 'independent')
    
    def test_parse_parallel_electrodes(self):
        """Test parsing parallel electrode groups."""
        parser = ArrayConfigParser(self.config_path)
        config = parser.parse()
        
        self.assertEqual(len(config.parallel_groups), 1)
        
        group = config.parallel_groups[0]
        self.assertEqual(group.group_id, 'P1')
        self.assertEqual(len(group.electrodes), 2)
        
        # Check that electrodes have the correct group_id
        for electrode in group.electrodes:
            self.assertEqual(electrode.group_id, 'P1')
            self.assertEqual(electrode.type, 'parallel')
    
    def test_parse_channel_electrodes(self):
        """Test parsing channel electrode matrix."""
        parser = ArrayConfigParser(self.config_path)
        config = parser.parse()
        
        # Should have 2x2 = 4 channel electrodes
        self.assertEqual(len(config.channel_electrodes), 4)
        
        # Check electrode IDs and positions
        expected_positions = [(0, 3), (1, 3), (0, 4), (1, 4)]
        expected_ids = ['C1', 'C2', 'C3', 'C4']
        
        for i, electrode in enumerate(config.channel_electrodes):
            self.assertEqual(electrode.id, expected_ids[i])
            self.assertEqual(electrode.position, expected_positions[i])
            self.assertEqual(electrode.type, 'channel')
    
    def test_get_all_electrodes(self):
        """Test getting all electrodes from the configuration."""
        parser = ArrayConfigParser(self.config_path)
        all_electrodes = parser.get_all_electrodes()
        
        # Should have 2 independent + 2 parallel + 4 channel = 8 electrodes
        self.assertEqual(len(all_electrodes), 8)
        
        # Check that all electrode types are present
        electrode_types = [electrode.type for electrode in all_electrodes]
        self.assertIn('independent', electrode_types)
        self.assertIn('parallel', electrode_types)
        self.assertIn('channel', electrode_types)
    
    def test_get_electrode_by_id(self):
        """Test retrieving a specific electrode by ID."""
        parser = ArrayConfigParser(self.config_path)
        
        # Test getting an independent electrode
        electrode = parser.get_electrode_by_id('R1')
        self.assertEqual(electrode.id, 'R1')
        self.assertEqual(electrode.type, 'independent')
        
        # Test getting a channel electrode
        electrode = parser.get_electrode_by_id('C1')
        self.assertEqual(electrode.id, 'C1')
        self.assertEqual(electrode.type, 'channel')
        
        # Test error for non-existent electrode
        with self.assertRaises(ValueError):
            parser.get_electrode_by_id('NONEXISTENT')
    
    def test_get_parallel_group_by_id(self):
        """Test retrieving a parallel electrode group by ID."""
        parser = ArrayConfigParser(self.config_path)
        
        group = parser.get_parallel_group_by_id('P1')
        self.assertEqual(group.group_id, 'P1')
        self.assertEqual(len(group.electrodes), 2)
        
        # Test error for non-existent group
        with self.assertRaises(ValueError):
            parser.get_parallel_group_by_id('NONEXISTENT')
    
    def test_file_not_found(self):
        """Test handling of missing configuration file."""
        parser = ArrayConfigParser('nonexistent.yaml')
        
        with self.assertRaises(FileNotFoundError):
            parser.load_config()


class TestElectrodeDataStructures(unittest.TestCase):
    """Test cases for electrode data structures."""
    
    def test_electrode_creation(self):
        """Test creating Electrode objects."""
        electrode = Electrode(id='E1', position=(0, 0), type='test')
        
        self.assertEqual(electrode.id, 'E1')
        self.assertEqual(electrode.position, (0, 0))
        self.assertEqual(electrode.type, 'test')
        self.assertEqual(electrode.state, 'normal')  # Default state
        self.assertIsNone(electrode.group_id)  # Default group_id
    
    def test_electrode_group_creation(self):
        """Test creating ElectrodeGroup objects."""
        electrodes = [
            Electrode(id='E1', position=(0, 0), type='parallel', group_id='G1'),
            Electrode(id='E2', position=(1, 0), type='parallel', group_id='G1')
        ]
        
        group = ElectrodeGroup(group_id='G1', electrodes=electrodes)
        
        self.assertEqual(group.group_id, 'G1')
        self.assertEqual(len(group.electrodes), 2)
        self.assertEqual(group.type, 'parallel')  # Default type


class TestApplicationIntegration(unittest.TestCase):
    """Integration tests for the complete application."""
    
    def test_real_config_parsing(self):
        """Test parsing the actual array.yaml configuration."""
        config_path = Path(__file__).parent / 'array.yaml'
        
        if config_path.exists():
            parser = ArrayConfigParser(str(config_path))
            config = parser.parse()
            
            # Test that configuration loads without errors
            self.assertIsInstance(config, ArrayConfig)
            self.assertGreater(len(config.channel_electrodes), 0)
            
            # Test that we have the expected 18x3 = 54 channel electrodes
            self.assertEqual(len(config.channel_electrodes), 54)
            
            # Test electrode ID format
            channel_ids = [e.id for e in config.channel_electrodes]
            self.assertIn('C1', channel_ids)
            self.assertIn('C54', channel_ids)
    
    def test_electrode_positions_unique(self):
        """Test that all electrode positions are unique."""
        config_path = Path(__file__).parent / 'array.yaml'
        
        if config_path.exists():
            parser = ArrayConfigParser(str(config_path))
            all_electrodes = parser.get_all_electrodes()
            
            positions = [electrode.position for electrode in all_electrodes]
            unique_positions = set(positions)
            
            # All positions should be unique
            self.assertEqual(len(positions), len(unique_positions))


def run_tests():
    """Run all test cases."""
    # Create a test suite
    test_suite = unittest.TestSuite()
    
    # Add test cases
    test_classes = [
        TestArrayConfigParser,
        TestElectrodeDataStructures,
        TestApplicationIntegration
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run the tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_tests()
    exit(0 if success else 1)