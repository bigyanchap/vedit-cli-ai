"""
VEdit CLI Configuration

This file contains configuration settings for the VEdit CLI application.
You can modify these settings to customize the application behavior.
"""

# UI Configuration
UI_CONFIG = {
    # Color scheme
    'background_color': '#2B2B2B',      # Eclipse Gray
    'foreground_color': 'white',
    'command_color': 'green',
    'command_executed_color': '#00FF00', # Bright green
    'error_color': 'red',
    'warning_color': 'yellow',
    'success_color': 'green',
    'info_color': 'cyan',
    
    # Window settings
    'window_width': 1200,
    'window_height': 800,
    'window_title': 'VEdit CLI - Video Editor',
    
    # Font settings
    'title_font': ('Consolas', 24, 'bold'),
    'command_font': ('Consolas', 14),
    'output_font': ('Consolas', 12),
    'status_font': ('Consolas', 10),
    'tutorial_font': ('Consolas', 16, 'bold'),
    
    # Tutorial button
    'tutorial_button_color': '#4CAF50',
    'tutorial_button_hover_color': '#45a049',
    'tutorial_button_height': 50
}

# Video Processing Configuration
VIDEO_CONFIG = {
    # Export settings
    'default_codec': 'libx264',
    'default_audio_codec': 'aac',
    'default_fps': 30,
    'default_bitrate': '8000k',
    'temp_audio_file': 'temp-audio.m4a',
    'remove_temp_files': True,
    
    # Image to video settings
    'default_image_duration': 3.0,  # seconds
    
    # Transition settings
    'default_transition': 'dissolve',
    'transition_duration': 1.0,     # seconds
    
    # Overlay settings
    'default_fade_duration': 0.5,   # seconds
    'default_text_stroke_width': 2,
    'default_text_bg_color': 'white',
    'default_text_stroke_color': 'black',
    'overlay_maintain_aspect_ratio': True,  # Maintain aspect ratio when resizing overlays
    'overlay_fill_mode': 'fit',  # 'fit' (maintain aspect ratio) or 'stretch' (fill entire screen)
    'overlay_max_size_percent': 100,  # Maximum size as percentage of base video
    
    # GIF settings
    'gif_loop_duration': 3.0,       # seconds per loop
}

# File Configuration
FILE_CONFIG = {
    # Supported file formats
    'video_formats': ['.mp4', '.avi', '.mov', '.mkv', '.wmv', '.flv', '.webm'],
    'audio_formats': ['.mp3', '.wav', '.aac', '.flac', '.ogg', '.m4a'],
    'image_formats': ['.jpg', '.jpeg', '.png', '.bmp', '.gif', '.tiff', '.webp'],
    
    # Project file settings
    'project_extension': '.vedit',
    'project_file_types': [('VEdit project', '*.vedit')],
    
    # Export settings
    'default_export_format': 'mp4',
    'export_filename_template': 'vedit_export_{timestamp}',
    'timestamp_format': '%Y%m%d_%H%M%S'
}

# Performance Configuration
PERFORMANCE_CONFIG = {
    # Memory management
    'max_clip_duration': 3600,      # 1 hour in seconds
    'max_concurrent_clips': 10,
    'cleanup_interval': 300,        # 5 minutes in seconds
    
    # Processing settings
    'use_multithreading': True,
    'max_threads': 4,
    'chunk_size': 1024 * 1024,      # 1MB chunks
    
    # Cache settings
    'enable_cache': True,
    'cache_directory': 'cache',
    'max_cache_size': 1024 * 1024 * 1024  # 1GB
}

# Command Configuration
COMMAND_CONFIG = {
    # Command aliases
    'aliases': {
        'h': 'help',
        '?': 'help',
        'cls': 'clear',
        'ls': 'list',
        'q': 'quit',
        'exit': 'quit'
    },
    
    # Command history
    'max_history': 100,
    'history_file': '.vedit_history',
    
    # Auto-completion
    'enable_autocomplete': True,
    'autocomplete_commands': [
        'upload', 'remove', 'trim', 'split', 'overlay', 'text',
        'overlay_settings', 'audio', 'gif', 'merge_all', 'export', 'project', 'help',
        'clear', 'list', 'quit'
    ]
}

# Error Handling Configuration
ERROR_CONFIG = {
    # Error reporting
    'log_errors': True,
    'error_log_file': 'vedit_errors.log',
    'show_error_details': True,
    
    # Recovery settings
    'auto_save_interval': 300,      # 5 minutes
    'backup_project_files': True,
    'max_backup_files': 5
}

# Tutorial Configuration
TUTORIAL_CONFIG = {
    'tutorial_window_width': 800,
    'tutorial_window_height': 600,
    'tutorial_title': 'VEdit CLI Tutorial',
    
    # Tutorial content sections
    'sections': [
        'Getting Started',
        'Uploading Media',
        'Editing Clips',
        'Adding Overlays',
        'Audio Operations',
        'Exporting Projects',
        'Advanced Features'
    ]
}

# Default values for new projects
DEFAULT_PROJECT = {
    'name': 'Untitled Project',
    'transition_type': 'dissolve',
    'output_path': None,
    'clips': {},
    'audio_clips': {},
    'photo_clips': {},
    'overlays': [],
    'text_overlays': [],
    'audio_overdubs': []
}

# All configuration combined
CONFIG = {
    'ui': UI_CONFIG,
    'video': VIDEO_CONFIG,
    'file': FILE_CONFIG,
    'performance': PERFORMANCE_CONFIG,
    'command': COMMAND_CONFIG,
    'error': ERROR_CONFIG,
    'tutorial': TUTORIAL_CONFIG,
    'default_project': DEFAULT_PROJECT
} 