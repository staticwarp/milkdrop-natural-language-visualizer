"""User preference prompts."""

from typing import List


def prompt_liked_files(files: List[str]) -> List[str]:
    """Ask which files user likes."""
    print("\n" + "="*60)
    print("PREFERENCE QUESTIONS")
    print("="*60)
    print(f"\nFound {len(files)} visualization files.\n")
    
    print("Question 1 of 9:")
    print("-" * 40)
    print("Which visualizations do you WANT MORE OF?")
    print("(Enter file numbers separated by commas, e.g., 1,3,5)")
    print("Or press Enter to skip.\n")
    
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f}")
    print()
    
    response = input("> ").strip()
    
    if not response:
        return []
    
    try:
        indices = [int(x.strip()) for x in response.split(",")]
        return [files[i-1] for i in indices if 1 <= i <= len(files)]
    except (ValueError, IndexError):
        print("Invalid input, skipping.")
        return []


def prompt_disliked_files(files: List[str], already_liked: List[str]) -> List[str]:
    """Ask which files user dislikes."""
    available = [f for f in files if f not in already_liked]
    
    print("\nQuestion 2 of 9:")
    print("-" * 40)
    print("Which visualizations do you NOT LIKE?")
    print("(Enter file numbers, e.g., 2,4,6)")
    print("Or press Enter to skip.\n")
    
    for i, f in enumerate(available, 1):
        print(f"  {i}. {f}")
    print()
    
    response = input("> ").strip()
    
    if not response:
        return []
    
    try:
        indices = [int(x.strip()) for x in response.split(",")]
        return [available[i-1] for i in indices if 1 <= i <= len(available)]
    except (ValueError, IndexError):
        print("Invalid input, skipping.")
        return []


def prompt_difference() -> str:
    """Ask what the perceived difference is."""
    print("\nQuestion 3 of 9:")
    print("-" * 40)
    print("What's the DIFFERENCE between the ones you like")
    print("and the ones you don't like?")
    print("(Describe in your own words)")
    print()
    
    response = input("> ").strip()
    return response


def prompt_resolution() -> str:
    """Ask about resolution preference."""
    print("\nQuestion 4 of 9:")
    print("-" * 40)
    print("Any RESOLUTION or ASPECT RATIO you're shooting for?")
    print("(e.g., '1920x1080', '16:9', '4:3', 'ultra-wide')")
    print("Or press Enter to skip.\n")
    
    response = input("> ").strip()
    return response


def prompt_colors() -> tuple[List[str], List[str]]:
    """Ask about color preferences."""
    print("\nQuestion 5 of 9:")
    print("-" * 40)
    print("What COLOR SCHEMES do you LIKE?")
    print("(e.g., 'neon', 'warm', 'cool', 'dark', 'saturated')")
    print("Enter comma-separated, or press Enter to skip.\n")
    
    liked = input("Liked colors > ").strip()
    liked_list = [x.strip() for x in liked.split(",") if x.strip()]
    
    print("\nWhat color schemes do you DISLIKE?")
    print("(Enter comma-separated, or press Enter to skip.\n")
    
    disliked = input("Disliked colors > ").strip()
    disliked_list = [x.strip() for x in disliked.split(",") if x.strip()]
    
    return liked_list, disliked_list


def prompt_geometry() -> tuple[List[str], List[str]]:
    """Ask about geometric preferences."""
    print("\nQuestion 6 of 9:")
    print("-" * 40)
    print("What GEOMETRIC DESIGNS do you like?")
    print("(e.g., 'level meters', 'lightning bolts', 'circles', 'lines', 'particles', 'waveform', 'spectrum')")
    print("Enter comma-separated, or press Enter to skip.\n")
    
    liked = input("Liked geometry > ").strip()
    liked_list = [x.strip() for x in liked.split(",") if x.strip()]
    
    print("\nWhat geometric designs do you DISLIKE?")
    print("Enter comma-separated, or press Enter to skip.\n")
    
    disliked = input("Disliked geometry > ").strip()
    disliked_list = [x.strip() for x in disliked.split(",") if x.strip()]
    
    return liked_list, disliked_list


def prompt_image_files() -> str:
    """Ask about image files."""
    print("\nQuestion 7 of 9:")
    print("-" * 40)
    print("Any IMAGE FILES you want me to implement?")
    print("(e.g., textures, custom shapes)")
    print("Or press Enter to skip.\n")
    
    response = input("> ").strip()
    return response


def prompt_favorite(files: List[str]) -> str:
    """Ask about favorite file."""
    print("\nQuestion 8 of 9:")
    print("-" * 40)
    print("Do you have a FAVORITE file in this directory?")
    print("(Enter file number, or press Enter to skip.)\n")
    
    for i, f in enumerate(files, 1):
        print(f"  {i}. {f}")
    print()
    
    response = input("> ").strip()
    
    if not response:
        return ""
    
    try:
        idx = int(response) - 1
        if 0 <= idx < len(files):
            return files[idx]
    except ValueError:
        pass
    
    return ""


def prompt_least_favorite(files: List[str], already_selected: List[str]) -> str:
    """Ask about least favorite file."""
    available = [f for f in files if f not in already_selected]
    
    print("\nQuestion 9 of 9:")
    print("-" * 40)
    print("Do you have a LEAST FAVORITE file?")
    print("(Enter file number, or press Enter to skip.)\n")
    
    for i, f in enumerate(available, 1):
        print(f"  {i}. {f}")
    print()
    
    response = input("> ").strip()
    
    if not response:
        return ""
    
    try:
        idx = int(response) - 1
        if 0 <= idx < len(available):
            return available[idx]
    except ValueError:
        pass
    
    return ""


def prompt_notes() -> str:
    """Ask for any additional notes."""
    print("\nAdditional Notes:")
    print("-" * 40)
    print("Any other preferences or notes?")
    print("(Press Enter to skip.)\n")
    
    response = input("> ").strip()
    return response


def collect_all_preferences(files: List[str]) -> dict:
    """Collect all preferences from user."""
    # Get liked files first
    liked_files = prompt_liked_files(files)
    disliked_files = prompt_disliked_files(files, liked_files)
    
    # Get difference insight
    difference = prompt_difference()
    
    # Resolution
    resolution = prompt_resolution()
    aspect_ratio = None
    if resolution and ":" in resolution:
        aspect_ratio = resolution
        resolution = None
    
    # Colors
    liked_colors, disliked_colors = prompt_colors()
    
    # Geometry
    liked_geometry, disliked_geometry = prompt_geometry()
    
    # Image files
    image_files = prompt_image_files()
    
    # Favorite
    favorite = prompt_favorite(files)
    selected_for_fav = [favorite] if favorite else []
    
    # Least favorite
    least_favorite = prompt_least_favorite(files, selected_for_fav)
    
    # Notes
    notes = prompt_notes()
    
    print("\n" + "="*60)
    print("PREFERENCES SAVED!")
    print("="*60)
    
    return {
        "liked_patterns": liked_files,
        "disliked_patterns": disliked_files,
        "difference_explanation": difference,
        "preferred_resolution": resolution,
        "preferred_aspect_ratio": aspect_ratio,
        "liked_colors": liked_colors,
        "disliked_colors": disliked_colors,
        "liked_geometry": liked_geometry,
        "disliked_geometry": disliked_geometry,
        "image_files": image_files,
        "favorite_file": favorite,
        "least_favorite_file": least_favorite,
        "notes": notes,
    }
