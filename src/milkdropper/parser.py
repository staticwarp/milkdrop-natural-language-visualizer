"""Parser for Milkdrop .milk preset files."""

import re
from pathlib import Path
from typing import Dict, List, Any, Optional
from dataclasses import dataclass


@dataclass
class MilkPreset:
    """Represents a parsed Milkdrop preset."""
    filename: str
    path: str
    sections: Dict[str, Dict[str, str]]
    raw_content: str


class MilkParser:
    """Parser for Milkdrop .milk files."""
    
    # Patterns to extract key attributes
    ATTRIBUTE_PATTERNS = {
        # Wave colors
        'wave_r': r'wave_r\s*=\s*([\d.]+)',
        'wave_g': r'wave_g\s*=\s*([\d.]+)',
        'wave_b': r'wave_b\s*=\s*([\d.]+)',
        # Shape colors
        'shape_r': r'shape_r\s*=\s*([\d.]+)',
        'shape_g': r'shape_g\s*=\s*([\d.]+)',
        'shape_b': r'shape_b\s*=\s*([\d.]+)',
        # Motion
        'wave_x': r'wave_x\s*=\s*([\d.]+)',
        'wave_y': r'wave_y\s*=\s*([\d.]+)',
        # Rotation
        'wave_rot': r'wave_rot\s*=\s*([\d.]+)',
        'wave_mystery': r'wave_mystery\s*=\s*([\d.]+)',
        # Per-frame
        'wave_per_frame1': r'wave_per_frame1\s*=\s*([^\n]+)',
        'wave_per_frame2': r'wave_per_frame2\s*=\s*([^\n]+)',
        # Theme
        'bright': r'bright\s*=\s*([\d.]+)',
        'contrast': r'contrast\s*=\s*([\d.]+)',
        'gamma': r'gamma\s*=\s*([\d.]+)',
        'saturation': r'saturation\s*=\s*([\d.]+)',
        # Video
        'fps': r'fps\s*=\s*(\d+)',
        'texsize': r'texsize\s*=\s*(\d+)',
        # Decay
        'decay': r'decay\s*=\s*([\d.]+)',
    }
    
    def __init__(self):
        self.current_file = None
    
    def parse_file(self, filepath: Path) -> Optional[MilkPreset]:
        """Parse a single .milk file."""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {filepath}: {e}")
            return None
        
        sections = self._parse_sections(content)
        
        return MilkPreset(
            filename=filepath.name,
            path=str(filepath),
            sections=sections,
            raw_content=content
        )
    
    def _parse_sections(self, content: str) -> Dict[str, Dict[str, str]]:
        """Parse content into sections."""
        sections = {}
        current_section = "default"
        sections[current_section] = {}
        
        for line in content.split('\n'):
            line = line.strip()
            
            # Check for section header
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                sections[current_section] = {}
                continue
            
            # Parse key=value
            if '=' in line:
                key, value = line.split('=', 1)
                sections[current_section][key.strip()] = value.strip()
        
        return sections
    
    def extract_attributes(self, preset: MilkPreset) -> Dict[str, Any]:
        """Extract key attributes from parsed preset."""
        attrs = {
            "filename": preset.filename,
            "path": preset.path,
        }
        
        # Merge all sections for searching
        all_values = {}
        for section in preset.sections.values():
            all_values.update(section)
        
        # Extract key attributes
        for attr, pattern in self.ATTRIBUTE_PATTERNS.items():
            match = re.search(pattern, preset.raw_content, re.IGNORECASE)
            if match:
                attrs[attr] = match.group(1)
        
        # Determine resolution from texsize
        if 'texsize' in attrs:
            try:
                texsize = int(attrs['texsize'])
                # Common sizes: 512, 1024, 2048, 4096
                # Usually square, so 2048 = 2048x2048
                attrs['resolution'] = f"{texsize}x{texsize}"
                attrs['aspect_ratio'] = self._guess_aspect_ratio(texsize)
            except ValueError:
                pass
        
        # Extract colors
        colors = self._extract_colors(preset)
        if colors:
            attrs['colors'] = colors
        
        # Determine motion type
        attrs['motion_type'] = self._guess_motion_type(preset)
        
        # Determine theme
        attrs['theme'] = self._guess_theme(preset)
        
        return attrs
    
    def _extract_colors(self, preset: MilkPreset) -> List[str]:
        """Extract color info from preset."""
        colors = []
        
        # Get wave colors
        try:
            r = float(preset.sections.get('wave', {}).get('wave_r', 0))
            g = float(preset.sections.get('wave', {}).get('wave_g', 0))
            b = float(preset.sections.get('wave', {}).get('wave_b', 0))
            
            # Determine color
            if r > 0.8 and g < 0.3 and b < 0.3:
                colors.append("red")
            elif r < 0.3 and g > 0.8 and b < 0.3:
                colors.append("green")
            elif r < 0.3 and g < 0.3 and b > 0.8:
                colors.append("blue")
            elif r > 0.8 and g > 0.8 and b < 0.3:
                colors.append("yellow")
            elif r > 0.8 and g > 0.5 and b > 0.8:
                colors.append("pink")
            elif r > 0.3 and g > 0.8 and b > 0.8:
                colors.append("cyan")
            elif r > 0.5 and g > 0.5 and b > 0.5:
                colors.append("white")
            elif r < 0.2 and g < 0.2 and b < 0.2:
                colors.append("dark")
            else:
                colors.append("mixed")
        except (ValueError, TypeError):
            pass
        
        return colors
    
    def _guess_aspect_ratio(self, texsize: int) -> str:
        """Guess aspect ratio from texsize."""
        # Common: 2048 = 1:1, could be cropped
        if texsize <= 512:
            return "1:1"
        return "1:1 (assumed)"
    
    def _guess_motion_type(self, preset: MilkPreset) -> str:
        """Guess the motion type."""
        content = preset.raw_content.lower()
        
        if 'sine' in content:
            return "wave"
        elif 'radial' in content:
            return "radial"
        elif 'point' in content:
            return "particles"
        elif 'mirror' in content:
            return "mirrored"
        else:
            return "standard"
    
    def _guess_theme(self, preset: MilkPreset) -> str:
        """Guess the visual theme."""
        content = preset.raw_content.lower()
        
        if 'star' in content or 'particle' in content:
            return "particles"
        elif 'circle' in content or 'spiral' in content:
            return "geometric"
        elif 'water' in content or 'ocean' in content:
            return "nature"
        elif 'neon' in content:
            return "neon"
        else:
            return "abstract"


def scan_directory(directory: Path) -> List[Path]:
    """Scan directory for .milk files."""
    milk_files = []
    
    if not directory.exists():
        print(f"Directory not found: {directory}")
        return milk_files
    
    for f in directory.iterdir():
        if f.is_file() and f.suffix.lower() in ('.milk', '.txt'):
            milk_files.append(f)
    
    return sorted(milk_files)
