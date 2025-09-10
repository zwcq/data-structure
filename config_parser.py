"""
Electrode Array Configuration Parser

This module provides functionality to parse array.yaml configuration files
and extract electrode layout information for visualization.
"""

import yaml
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Electrode:
    """Represents a single electrode with its properties."""
    id: str
    position: Tuple[int, int]
    type: str
    state: str = "normal"  # normal, active
    group_id: str = None  # For parallel electrodes


@dataclass
class ElectrodeGroup:
    """Represents a group of parallel electrodes."""
    group_id: str
    electrodes: List[Electrode]
    type: str = "parallel"


@dataclass
class ArrayConfig:
    """Contains the complete electrode array configuration."""
    independent_electrodes: List[Electrode]
    parallel_groups: List[ElectrodeGroup]
    channel_electrodes: List[Electrode]
    visual_config: Dict[str, Any]
    settings: Dict[str, Any]
    channel_config: Dict[str, Any]


class ArrayConfigParser:
    """Parser for array.yaml configuration files."""
    
    def __init__(self, config_path: str = "array.yaml"):
        """Initialize the parser with a configuration file path."""
        self.config_path = Path(config_path)
        self.config_data = None
        
    def load_config(self) -> Dict[str, Any]:
        """Load and parse the YAML configuration file."""
        if not self.config_path.exists():
            raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
            
        with open(self.config_path, 'r', encoding='utf-8') as file:
            self.config_data = yaml.safe_load(file)
            
        return self.config_data
    
    def parse(self) -> ArrayConfig:
        """Parse the configuration and return an ArrayConfig object."""
        if self.config_data is None:
            self.load_config()
            
        # Parse independent electrodes
        independent_electrodes = []
        reservoir_config = self.config_data.get('reservoir', {})
        
        for electrode_data in reservoir_config.get('independent_electrodes', []):
            electrode = Electrode(
                id=electrode_data['id'],
                position=tuple(electrode_data['position']),
                type=electrode_data['type']
            )
            independent_electrodes.append(electrode)
        
        # Parse parallel electrode groups
        parallel_groups = []
        for group_data in reservoir_config.get('parallel_electrodes', []):
            electrodes_in_group = []
            group_id = group_data['group_id']
            
            for electrode_data in group_data['electrodes']:
                electrode = Electrode(
                    id=electrode_data['id'],
                    position=tuple(electrode_data['position']),
                    type=group_data['type'],
                    group_id=group_id
                )
                electrodes_in_group.append(electrode)
            
            group = ElectrodeGroup(
                group_id=group_id,
                electrodes=electrodes_in_group,
                type=group_data['type']
            )
            parallel_groups.append(group)
        
        # Parse channel electrodes (18x3 matrix)
        channel_electrodes = []
        channel_config = self.config_data.get('channels', {})
        rows = channel_config.get('rows', 18)
        columns = channel_config.get('columns', 3)
        start_pos = channel_config.get('start_position', [0, 3])
        prefix = channel_config.get('electrode_prefix', 'C')
        
        electrode_id = 1
        for row in range(rows):
            for col in range(columns):
                electrode = Electrode(
                    id=f"{prefix}{electrode_id}",
                    position=(start_pos[0] + col, start_pos[1] + row),
                    type="channel"
                )
                channel_electrodes.append(electrode)
                electrode_id += 1
        
        # Get visual and settings configuration
        visual_config = self.config_data.get('visual', {})
        settings = self.config_data.get('settings', {})
        
        return ArrayConfig(
            independent_electrodes=independent_electrodes,
            parallel_groups=parallel_groups,
            channel_electrodes=channel_electrodes,
            visual_config=visual_config,
            settings=settings,
            channel_config=channel_config
        )
    
    def get_all_electrodes(self) -> List[Electrode]:
        """Get a flat list of all electrodes in the configuration."""
        config = self.parse()
        all_electrodes = []
        
        # Add independent electrodes
        all_electrodes.extend(config.independent_electrodes)
        
        # Add electrodes from parallel groups
        for group in config.parallel_groups:
            all_electrodes.extend(group.electrodes)
        
        # Add channel electrodes
        all_electrodes.extend(config.channel_electrodes)
        
        return all_electrodes
    
    def get_electrode_by_id(self, electrode_id: str) -> Electrode:
        """Get a specific electrode by its ID."""
        all_electrodes = self.get_all_electrodes()
        for electrode in all_electrodes:
            if electrode.id == electrode_id:
                return electrode
        raise ValueError(f"Electrode with ID '{electrode_id}' not found")
    
    def get_parallel_group_by_id(self, group_id: str) -> ElectrodeGroup:
        """Get a parallel electrode group by its ID."""
        config = self.parse()
        for group in config.parallel_groups:
            if group.group_id == group_id:
                return group
        raise ValueError(f"Parallel group with ID '{group_id}' not found")


if __name__ == "__main__":
    # Test the parser
    parser = ArrayConfigParser("array.yaml")
    try:
        config = parser.parse()
        print(f"Loaded configuration with:")
        print(f"  - {len(config.independent_electrodes)} independent electrodes")
        print(f"  - {len(config.parallel_groups)} parallel groups")
        print(f"  - {len(config.channel_electrodes)} channel electrodes")
        
        all_electrodes = parser.get_all_electrodes()
        print(f"  - Total: {len(all_electrodes)} electrodes")
        
    except FileNotFoundError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")