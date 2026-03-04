"""Main CLI for milkdropper."""

import sys
import argparse
from pathlib import Path

from .parser import scan_directory
from .analyzer import analyze_directory, print_analysis
from .prompts import collect_all_preferences
from .storage import storage, Preferences


def get_directories() -> tuple[Path, Path]:
    """Get example and new visualization directories."""
    # Assume we're running from project root
    project_root = Path(__file__).parent.parent.parent
    
    example_dir = project_root / "example_visualizations"
    new_dir = project_root / "new_visualizations"
    
    return example_dir, new_dir


def cmd_analyze(args):
    """Analyze presets in example_visualizations directory."""
    example_dir, new_dir = get_directories()
    
    print("="*60)
    print("MILKDROP NATURAL LANGUAGE VISUALIZER")
    print("="*60)
    print(f"\nScanning: {example_dir}")
    
    # First, analyze the files
    metadata = analyze_directory(example_dir)
    
    if metadata["count"] == 0:
        print(f"\nNo .milk files found in {example_dir}")
        print("Add some .milk files and try again!")
        return
    
    print_analysis(metadata)
    
    # Then prompt for preferences
    files = metadata["files"]
    prefs = collect_all_preferences(files)
    
    # Save preferences
    preferences = storage.get_default_preferences()
    preferences.liked_patterns = prefs.get("liked_patterns", [])
    preferences.disliked_patterns = prefs.get("disliked_patterns", [])
    preferences.preferred_resolution = prefs.get("preferred_resolution")
    preferences.preferred_aspect_ratio = prefs.get("preferred_aspect_ratio")
    preferences.liked_colors = prefs.get("liked_colors", [])
    preferences.disliked_colors = prefs.get("disliked_colors", [])
    preferences.liked_geometry = prefs.get("liked_geometry", [])
    preferences.disliked_geometry = prefs.get("disliked_geometry", [])
    preferences.favorite_file = prefs.get("favorite_file")
    preferences.least_favorite_file = prefs.get("least_favorite_file")
    preferences.notes = prefs.get("notes", "")
    
    storage.save_preferences(preferences)
    print(f"\nPreferences saved to: {storage.preferences_file}")


def cmd_preferences(args):
    """Show stored preferences."""
    prefs = storage.load_preferences()
    
    if not prefs:
        print("No preferences stored yet.")
        print("Run 'python -m milkdropper analyze' first.")
        return
    
    print("="*60)
    print("STORED PREFERENCES")
    print("="*60)
    
    if prefs.liked_patterns:
        print(f"\n✓ Liked files ({len(prefs.liked_patterns)}):")
        for f in prefs.liked_patterns:
            print(f"  - {f}")
    
    if prefs.disliked_patterns:
        print(f"\n✗ Disliked files ({len(prefs.disliked_patterns)}):")
        for f in prefs.disliked_patterns:
            print(f"  - {f}")
    
    if prefs.preferred_resolution:
        print(f"\n📐 Preferred resolution: {prefs.preferred_resolution}")
    
    if prefs.preferred_aspect_ratio:
        print(f"📐 Preferred aspect ratio: {prefs.preferred_aspect_ratio}")
    
    if prefs.liked_colors:
        print(f"\n🎨 Liked colors: {', '.join(prefs.liked_colors)}")
    
    if prefs.disliked_colors:
        print(f"🎨 Disliked colors: {', '.join(prefs.disliked_colors)}")
    
    if prefs.liked_geometry:
        print(f"🔷 Liked geometry: {', '.join(prefs.liked_geometry)}")
    
    if prefs.disliked_geometry:
        print(f"🔷 Disliked geometry: {', '.join(prefs.disliked_geometry)}")
    
    if prefs.favorite_file:
        print(f"\n⭐ Favorite: {prefs.favorite_file}")
    
    if prefs.least_favorite_file:
        print(f"👎 Least favorite: {prefs.least_favorite_file}")
    
    if prefs.notes:
        print(f"\n📝 Notes: {prefs.notes}")
    
    print(f"\nLast updated: {prefs.updated_at}")


def cmd_generate(args):
    """Generate a new preset based on preferences."""
    prefs = storage.load_preferences()
    
    if not prefs:
        print("No preferences stored.")
        print("Run 'python -m milkdropper analyze' first.")
        return
    
    prompt = args.prompt
    
    print("="*60)
    print("GENERATE NEW PRESET")
    print("="*60)
    print(f"\nYour request: {prompt}")
    print("\nBased on your preferences:")
    
    if prefs.liked_colors:
        print(f"  Colors: {', '.join(prefs.liked_colors)}")
    if prefs.liked_geometry:
        print(f"  Geometry: {', '.join(prefs.liked_geometry)}")
    if prefs.preferred_resolution:
        print(f"  Resolution: {prefs.preferred_resolution}")
    
    print("\n[This is a placeholder - generation not yet implemented]")
    print("The system would now generate a .milk file based on your preferences.")


def cmd_clear(args):
    """Clear stored preferences."""
    confirm = input("Clear all preferences? (y/N): ").strip().lower()
    
    if confirm == 'y':
        storage.clear_preferences()
        print("Preferences cleared.")
    else:
        print("Cancelled.")


def main():
    parser = argparse.ArgumentParser(
        description="Milkdrop Natural Language Visualizer"
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Commands")
    
    # analyze command
    subparsers.add_parser("analyze", help="Analyze presets and collect preferences")
    
    # preferences command
    subparsers.add_parser("preferences", help="Show stored preferences")
    
    # generate command
    gen_parser = subparsers.add_parser("generate", help="Generate new preset")
    gen_parser.add_argument("prompt", help="Description of what you want")
    
    # clear command
    subparsers.add_parser("clear", help="Clear stored preferences")
    
    args = parser.parse_args()
    
    if args.command == "analyze":
        cmd_analyze(args)
    elif args.command == "preferences":
        cmd_preferences(args)
    elif args.command == "generate":
        cmd_generate(args)
    elif args.command == "clear":
        cmd_clear(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
