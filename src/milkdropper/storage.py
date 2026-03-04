"""Storage for preferences and metadata."""

import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict
from datetime import datetime


STORAGE_DIR = Path(__file__).parent.parent
PREFERENCES_FILE = STORAGE_DIR / "preferences.json"
METADATA_FILE = STORAGE_DIR / "metadata.json"


@dataclass
class Preference:
    """A single preference."""
    category: str  # like, dislike, resolution, color, geometry, etc.
    value: str
    source_file: Optional[str] = None  # Which file this came from
    notes: Optional[str] = None


@dataclass
class Preferences:
    """All user preferences."""
    liked_patterns: List[str]
    disliked_patterns: List[str]
    preferred_resolution: Optional[str]
    preferred_aspect_ratio: Optional[str]
    liked_colors: List[str]
    disliked_colors: List[str]
    liked_geometry: List[str]
    disliked_geometry: List[str]
    favorite_file: Optional[str]
    least_favorite_file: Optional[str]
    notes: str
    updated_at: str


class Storage:
    """Handle preferences and metadata storage."""
    
    def __init__(self):
        self.preferences_file = PREFERENCES_FILE
        self.metadata_file = METADATA_FILE
    
    def load_preferences(self) -> Optional[Preferences]:
        """Load preferences from file."""
        if not self.preferences_file.exists():
            return None
        
        try:
            with open(self.preferences_file) as f:
                data = json.load(f)
                return Preferences(**data)
        except (json.JSONDecodeError, TypeError):
            return None
    
    def save_preferences(self, prefs: Preferences):
        """Save preferences to file."""
        prefs.updated_at = datetime.utcnow().isoformat()
        with open(self.preferences_file, 'w') as f:
            json.dump(asdict(prefs), f, indent=2)
    
    def get_default_preferences(self) -> Preferences:
        """Get default empty preferences."""
        return Preferences(
            liked_patterns=[],
            disliked_patterns=[],
            preferred_resolution=None,
            preferred_aspect_ratio=None,
            liked_colors=[],
            disliked_colors=[],
            liked_geometry=[],
            disliked_geometry=[],
            favorite_file=None,
            least_favorite_file=None,
            notes="",
            updated_at=datetime.utcnow().isoformat()
        )
    
    def load_metadata(self) -> Dict[str, Any]:
        """Load file metadata."""
        if not self.metadata_file.exists():
            return {}
        
        try:
            with open(self.metadata_file) as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    
    def save_metadata(self, metadata: Dict[str, Any]):
        """Save file metadata."""
        with open(self.metadata_file, 'w') as f:
            json.dump(metadata, f, indent=2)
    
    def clear_preferences(self):
        """Clear stored preferences."""
        if self.preferences_file.exists():
            self.preferences_file.unlink()


# Global storage instance
storage = Storage()
