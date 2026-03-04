"""Analyze presets and extract metadata."""

from pathlib import Path
from typing import List, Dict, Any
from .parser import MilkParser, scan_directory
from .storage import storage


def analyze_directory(directory: Path) -> Dict[str, Any]:
    """Analyze all .milk files in a directory."""
    parser = MilkParser()
    files = scan_directory(directory)
    
    if not files:
        return {"files": [], "count": 0}
    
    metadata = {}
    
    print(f"Found {len(files)} files, analyzing...")
    
    for i, filepath in enumerate(files, 1):
        print(f"  [{i}/{len(files)}] Parsing {filepath.name}...")
        
        preset = parser.parse_file(filepath)
        if preset:
            attrs = parser.extract_attributes(preset)
            metadata[filepath.name] = attrs
    
    return {
        "files": [f.name for f in files],
        "count": len(files),
        "metadata": metadata,
        "directory": str(directory)
    }


def print_analysis(metadata: Dict[str, Any]):
    """Print analysis results."""
    print("\n" + "="*60)
    print("ANALYSIS COMPLETE")
    print("="*60)
    
    print(f"\nFound {metadata['count']} preset files")
    print(f"Directory: {metadata['directory']}")
    
    # Group by resolution
    resolutions = {}
    colors = {}
    themes = {}
    
    for name, attrs in metadata.get("metadata", {}).items():
        # Resolution
        res = attrs.get("resolution", "unknown")
        resolutions[res] = resolutions.get(res, 0) + 1
        
        # Colors
        for color in attrs.get("colors", []):
            colors[color] = colors.get(color, 0) + 1
        
        # Theme
        theme = attrs.get("theme", "unknown")
        themes[theme] = themes.get(theme, 0) + 1
    
    if resolutions:
        print("\nResolutions:")
        for res, count in sorted(resolutions.items(), key=lambda x: -x[1]):
            print(f"  {res}: {count}")
    
    if colors:
        print("\nColors:")
        for color, count in sorted(colors.items(), key=lambda x: -x[1])[:10]:
            print(f"  {color}: {count}")
    
    if themes:
        print("\nThemes:")
        for theme, count in sorted(themes.items(), key=lambda x: -x[1]):
            print(f"  {theme}: {count}")
    
    # Save metadata
    storage.save_metadata(metadata.get("metadata", {}))
    print(f"\nMetadata saved to: {storage.metadata_file}")
