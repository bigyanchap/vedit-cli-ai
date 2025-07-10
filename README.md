# VEdit CLI - Video Editor

A powerful Windows desktop CLI video editor application built with Python. VEdit CLI provides a command-line interface for video editing with support for multiple media formats, transitions, overlays, and advanced editing features.

## Features

### 🎬 Core Video Editing
- **Upload multiple media types**: Videos (MP4, AVI, MOV, MKV, WMV), Audio (MP3, WAV, AAC, FLAC), Images (JPG, PNG, BMP, GIF)
- **Clip manipulation**: Remove sections, trim clips, split videos
- **Advanced editing**: Remove beginning, middle, or end sections of clips
- **Batch processing**: Handle multiple clips simultaneously

### 🎭 Transitions & Effects
- **Smooth transitions**: Dissolve, cut, and custom transition effects
- **1-second dissolve**: Built-in slow dissolve transition
- **Customizable effects**: Fade in/out, pop in/fade out

### 🎨 Overlay System
- **Video overlays**: Overlay videos with fade effects and aspect ratio preservation
- **Photo overlays**: Add images with customizable timing and sizing
- **Text overlays**: White text with dark shadow, customizable size and position
- **GIF overlays**: Create videos from audio + GIF combinations
- **Smart sizing**: Maintains aspect ratio by default, configurable fill modes

### 🎵 Audio Features
- **Audio removal**: Remove audio from specific clips or all clips
- **Audio overdubbing**: Add background music or sound effects
- **Audio-video sync**: Perfect synchronization between audio and video

### 📁 Export & Project Management
- **MP4 export**: High-quality video export with H.264 codec
- **Project saving**: Save and load project files (.vedit format)
- **Custom output paths**: Export to any folder with timestamped filenames

### 🎯 Advanced Features
- **GIF video creation**: Convert audio + GIF to video
- **Split functionality**: Split videos at specific timestamps
- **Real-time preview**: See changes in the command output
- **Background processing**: Non-blocking export operations

## Installation

### Prerequisites
- Python 3.8 or higher
- Windows 10/11
- FFmpeg (will be installed automatically via imageio-ffmpeg)

### Quick Install
1. Clone or download this repository
2. Open Command Prompt in the project directory
3. Install dependencies:
```bash
pip install -r requirements.txt
```

### Manual Installation
If you prefer to install dependencies manually:
```bash
pip install moviepy==1.0.3
pip install Pillow==10.0.1
pip install customtkinter==5.2.0
pip install opencv-python==4.8.1.78
pip install numpy==1.24.3
pip install imageio==2.31.5
pip install imageio-ffmpeg==0.4.9
pip install pydub==0.25.1
```

## Usage

### Starting the Application
```bash
python vedit_cli.py
```

### Basic Workflow Example

1. **Upload media files**:
```
vedit> upload dialog
vedit> upload C:\Videos\clip1.mp4
vedit> upload C:\Audio\music.mp3
```

2. **Edit clips**:
```
vedit> video_1: remove(0:10, 0:30)
vedit> video_1: remove(1:45, 2:15)
vedit> video_1: trim(0:30, 1:30)
```

3. **Add overlays**:
```
vedit> overlay(photo_1, 0:00, 0:05, fade-in-out)
vedit> text("Welcome!", center, 48, white)
```

4. **Audio operations**:
```
vedit> audio remove
vedit> audio overdub music_1 0:00
```

5. **Export**:
```
vedit> merge_all(dissolve)
vedit> export(D:\MyVideos)
```

### Command Reference

#### Upload Commands
```
upload <file_path>          # Upload specific file
upload dialog               # Open file selection dialog
```

#### Clip Manipulation
```
clip_name: remove(start, end)  # Remove section from clip
clip_name: trim(start, end)    # Trim clip to section
split clip_name time           # Split clip at time
```

#### Merge & Export
```
merge_all                      # Set merge transition to dissolve (default)
merge_all(transition)          # Set merge transition (dissolve, cut)
export(output_path)            # Export to specified path
```

#### Overlay Commands
```
overlay(source, from, to, effect)  # Overlay video/photo
text("text", position, size, color) # Add text overlay
overlay_settings show               # Show overlay settings
overlay_settings fill_mode [fit|stretch] # Set overlay fill mode
overlay_settings max_size <1-200>  # Set overlay max size percentage
```

#### Audio Commands
```
audio remove                   # Remove audio from all clips
audio overdub audio_name time  # Overdub audio at time
```

#### Special Features
```
gif audio_name gif_path        # Create video from audio + GIF
project [save|load|new]        # Project management
```

#### Utility Commands
```
help, h, ?                     # Show help
clear, cls                     # Clear output
list, ls                       # List all clips
```

### Time Format Examples
- `1:30` = 1 minute 30 seconds
- `90` = 90 seconds
- `1:30:45` = 1 hour 30 minutes 45 seconds

### Effect Types
- `fade-in-out`: Smooth fade in and out
- `pop-in-fade-out`: Instant appear, fade out
- `dissolve`: Smooth transition between clips
- `cut`: Instant transition

### Overlay Sizing Options
- `fit`: Maintain aspect ratio (default) - overlays fit within base video bounds
- `stretch`: Fill entire screen (original behavior) - overlays stretch to match base video
- `max_size`: Control maximum overlay size as percentage of base video (1-200%)

## UI Features

### Color Scheme
- **Background**: Eclipse Gray (#2B2B2B) - Almost black
- **Foreground**: White text
- **Commands**: Green when typing, bright green when executed
- **Status**: Color-coded messages (green for success, red for errors, yellow for warnings)

### Interface Elements
- **Command Line**: Green prompt with real-time command execution
- **Output Display**: Scrollable text area with timestamps
- **Tutorial Button**: Prominent green button for learning
- **Status Bar**: Real-time status updates

## Advanced Examples

### Complex Video Project
```
# Upload multiple files
vedit> upload dialog
vedit> upload dialog
vedit> upload dialog

# Edit clips
vedit> video_1: remove(0:05, 0:15)
vedit> video_2: trim(0:30, 2:00)
vedit> split video_3 1:45

# Add overlays
vedit> overlay(photo_1, 0:00, 0:10, fade-in-out)
vedit> text("My Video", center, 60, white)
vedit> overlay(photo_2, 1:30, 1:40, pop-in-fade-out)

# Audio operations
vedit> audio remove
vedit> audio overdub music_1 0:00

# Create GIF video
vedit> gif audio_2 animation.gif

# Export
vedit> merge_all(dissolve)
vedit> export(C:\VideoProjects\Final)
```

### Audio-Only Project
```
# Upload audio and GIF
vedit> upload music.mp3
vedit> upload animation.gif

# Create video from audio + GIF
vedit> gif audio_1 animation.gif

# Add text overlay
vedit> text("Music Video", center, 48, white)

# Export
vedit> export(D:\MusicVideos)
```

## Troubleshooting

### Common Issues

1. **FFmpeg not found**: The application will automatically install FFmpeg via imageio-ffmpeg
2. **Memory issues**: Close other applications when processing large videos
3. **Export fails**: Ensure the output directory exists and has write permissions
4. **File not found**: Use absolute paths or ensure files are in the correct location
5. **Overlays covering whole screen**: Use `overlay_settings fill_mode fit` to maintain aspect ratio
6. **Overlay distortion**: Check overlay settings with `overlay_settings show` and adjust max_size if needed

### Performance Tips
- Use smaller video files for testing
- Close unnecessary applications during export
- Use SSD storage for better performance
- Process videos in smaller chunks if memory is limited

## System Requirements

- **OS**: Windows 10/11
- **Python**: 3.8 or higher
- **RAM**: 4GB minimum, 8GB recommended
- **Storage**: 2GB free space for dependencies
- **Graphics**: Any modern graphics card (for video processing)

## License

This project is open source and available under the MIT License.

## Contributing

Contributions are welcome! Please feel free to submit pull requests or open issues for bugs and feature requests.

## Support

For support and questions:
1. Check the built-in tutorial (click the TUTORIAL button)
2. Use the `help` command in the application
3. Review the examples in this README
4. Open an issue on the project repository

---

**VEdit CLI** - Making video editing accessible through the command line! 🎬✨ 