"""
VEdit CLI - Example Workflow Script

This script demonstrates how to use all the features of VEdit CLI
through a complete video editing workflow.

Usage: python example_workflow.py
"""

import os
import sys
from pathlib import Path

# Add the current directory to Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from vedit_cli import VideoEditorCLI

def create_example_project():
    """Create a complete example project demonstrating all features"""
    
    print("🎬 VEdit CLI - Example Workflow")
    print("=" * 50)
    
    # Initialize the editor
    editor = VideoEditorCLI()
    
    # Example commands that would be typed in the CLI
    example_commands = [
        # 1. Upload media files
        "upload dialog",  # This will open file dialog
        "upload C:\\SampleVideos\\intro.mp4",
        "upload C:\\SampleAudio\\background_music.mp3",
        "upload C:\\SampleImages\\logo.png",
        
        # 2. Edit video clips
        "video_1: remove(0:05, 0:15)",  # Remove first 10 seconds
        "video_1: remove(1:45, 2:15)",  # Remove middle section
        "video_1: trim(0:30, 1:30)",    # Keep only 30s to 1m30s
        
        # 3. Split a clip
        "split video_1 0:45",
        
        # 4. Add overlays
        "overlay(photo_1, 0:00, 0:10, fade-in-out)",
        "overlay(photo_1, 1:30, 1:40, pop-in-fade-out)",
        
        # 5. Add text overlays
        "text(\"Welcome to My Video!\", center, 48, white)",
        "text(\"Created with VEdit CLI\", bottom, 24, white)",
        
        # 6. Audio operations
        "audio remove",                    # Remove all audio
        "audio overdub audio_1 0:00",      # Add background music
        
        # 7. Create GIF video from audio
        "gif audio_1 animation.gif",
        
        # 8. Set merge transition
        "merge_all(dissolve)",
        
        # 9. Export the project
        "export(C:\\VideoProjects\\Final)",
        
        # 10. Project management
        "project save",
        "project new",
        "project load",
        
        # 11. Utility commands
        "list",
        "help",
        "clear"
    ]
    
    print("\n📋 Example Commands:")
    print("-" * 30)
    
    for i, cmd in enumerate(example_commands, 1):
        print(f"{i:2d}. {cmd}")
    
    print("\n🎯 Key Features Demonstrated:")
    print("-" * 30)
    print("✅ Upload videos, audio, and images")
    print("✅ Remove sections from clips")
    print("✅ Trim clips to specific ranges")
    print("✅ Split clips at timestamps")
    print("✅ Add video/photo overlays with effects")
    print("✅ Add text overlays with positioning")
    print("✅ Remove and overdub audio")
    print("✅ Create videos from audio + GIF")
    print("✅ Merge clips with transitions")
    print("✅ Export to MP4 format")
    print("✅ Save and load projects")
    print("✅ List clips and get help")
    
    print("\n🚀 To run the actual application:")
    print("1. Double-click 'install_and_run.bat' for first-time setup")
    print("2. Or run 'python vedit_cli.py' if dependencies are installed")
    print("3. Type the commands above in the CLI interface")
    
    print("\n💡 Tips:")
    print("- Use 'upload dialog' to easily select files")
    print("- Times can be in MM:SS or SS format")
    print("- Click the TUTORIAL button for interactive help")
    print("- Use 'help' command for full command reference")
    
    return editor

def demonstrate_time_formats():
    """Demonstrate different time formats"""
    print("\n⏰ Time Format Examples:")
    print("-" * 25)
    
    time_examples = [
        ("0:30", "30 seconds"),
        ("1:30", "1 minute 30 seconds"),
        ("2:45", "2 minutes 45 seconds"),
        ("1:30:45", "1 hour 30 minutes 45 seconds"),
        ("90", "90 seconds"),
        ("120", "2 minutes")
    ]
    
    for time_str, description in time_examples:
        print(f"  {time_str:8} = {description}")

def demonstrate_effects():
    """Demonstrate available effects"""
    print("\n🎭 Available Effects:")
    print("-" * 20)
    
    effects = [
        ("fade-in-out", "Smooth fade in and out"),
        ("pop-in-fade-out", "Instant appear, fade out"),
        ("dissolve", "Smooth transition between clips"),
        ("cut", "Instant transition")
    ]
    
    for effect, description in effects:
        print(f"  {effect:15} = {description}")

def demonstrate_positions():
    """Demonstrate text positioning options"""
    print("\n📍 Text Position Options:")
    print("-" * 25)
    
    positions = [
        ("center", "Center of video"),
        ("top", "Top center"),
        ("bottom", "Bottom center"),
        ("(100, 100)", "Custom coordinates")
    ]
    
    for pos, description in positions:
        print(f"  {pos:12} = {description}")

if __name__ == "__main__":
    print("VEdit CLI - Complete Example Workflow")
    print("=" * 50)
    
    # Create example project
    editor = create_example_project()
    
    # Demonstrate features
    demonstrate_time_formats()
    demonstrate_effects()
    demonstrate_positions()
    
    print("\n" + "=" * 50)
    print("🎬 Ready to start editing! Run the application and try these commands.")
    print("For more help, check the README.md file or use the built-in tutorial.") 