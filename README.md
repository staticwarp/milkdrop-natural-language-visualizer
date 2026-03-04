# Milkdrop Natural Language Visualizer

A tool to analyze Milkdrop visualization presets and help you find/create visualizations based on natural language preferences.

## What This Does

1. **Analyzes** Milkdrop .milk preset files
2. **Extracts** attributes: resolution, colors, geometric elements, motion
3. **Learns** your preferences through conversation
4. **Generates** new presets based on what you like

## Quick Start

```bash
# Install
pip install -r requirements.txt

# Analyze a directory of presets
python -m milkdropper analyze

# Answer the preference questions when prompted!

# Later, check your preferences
python -m milkdropper preferences

# Generate a new preset based on preferences
python -m milkdropper generate "neon colors with fast motion"
```

## Directory Structure

```
milkdropper/
├── example_visualizations/   # Put your .milk files here to analyze
├── new_visualizations/       # Generated presets go here
├── preferences.json         # Your preferences (auto-generated)
├── metadata.json            # Parsed file metadata (auto-generated)
└── src/
    └── milkdropper/
        ├── __init__.py
        ├── cli.py
        ├── parser.py
        ├── analyzer.py
        ├── prompts.py
        └── storage.py
```

## Commands

| Command | Description |
|---------|-------------|
| `analyze` | Scan example_visualizations/ and prompt for preferences |
| `preferences` | Show stored preferences |
| `generate <prompt>` | Create new preset based on prompt + preferences |
| `clear` | Clear stored preferences |

## How It Works

1. **First run:** Put .milk files in `example_visualizations/`
2. Run `python -m milkdropper analyze`
3. **Answer the preference questions:**
   - Which visualizations do you want more of?
   - Which ones do you NOT like?
   - What's the difference between ones you like and don't like?
   - Any resolution/aspect ratio preference?
   - Any color schemes you want?
   - Geometric designs you like?
   - Favorite file?
   - Least favorite file?
4. **Use preferences** to generate new visualizations!

## Example .milk File

Milkdrop preset files are text files with key=value pairs:

```
[preset]
name = My Cool Viz
fps = 60
texsize = 2048

[wave]
r = 1
g = 1
b = 1
```

The parser extracts these into analyzable metadata.

## Requirements

- Python 3.9+
- No external dependencies for basic parsing
