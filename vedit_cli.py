import os
import sys
import re
import json
import threading
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import customtkinter as ctk
from moviepy.editor import *
from moviepy.video.fx import resize
from PIL import Image, ImageDraw, ImageFont
import numpy as np
import cv2

class VideoEditorCLI:
    def __init__(self):
        self.clips = {}
        self.audio_clips = {}
        self.photo_clips = {}
        self.current_project = None
        self.output_path = None
        self.transition_type = "dissolve"
        self.overlay_clips = []
        self.text_overlays = []
        self.audio_overdubs = []
        
        # Initialize GUI
        self.setup_gui()
        
    def setup_gui(self):
        """Setup the GUI with Eclipse Gray background and white foreground"""
        self.root = ctk.CTk()
        self.root.title("VEdit CLI - Video Editor")
        self.root.geometry("1600x900")
        
        # Set Eclipse Gray background
        self.root.configure(bg="#2B2B2B")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("dark-blue")
        
        # Main frame
        main_frame = ctk.CTkFrame(self.root, fg_color="#2B2B2B")
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Title
        title_label = ctk.CTkLabel(main_frame, text="VEdit CLI - Video Editor", 
                                  font=("Consolas", 24, "bold"), text_color="white")
        title_label.pack(pady=(0, 20))
        
        # Content area with preview
        content_frame = ctk.CTkFrame(main_frame, fg_color="#2B2B2B")
        content_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Left side - Output display
        left_frame = ctk.CTkFrame(content_frame, fg_color="#1E1E1E")
        left_frame.pack(side="left", fill="both", expand=True, padx=(0, 5))
        
        # Output text widget
        self.output_text = ctk.CTkTextbox(left_frame, font=("Consolas", 12), 
                                         fg_color="#1E1E1E", text_color="white")
        self.output_text.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Right side - Preview panel
        right_frame = ctk.CTkFrame(content_frame, fg_color="#1E1E1E", width=400)
        right_frame.pack(side="right", fill="y", padx=(5, 0))
        right_frame.pack_propagate(False)
        
        # Preview title
        preview_title = ctk.CTkLabel(right_frame, text="🎬 PREVIEW", 
                                    font=("Consolas", 16, "bold"), text_color="cyan")
        preview_title.pack(pady=(10, 5))
        
        # Preview area
        self.preview_frame = ctk.CTkFrame(right_frame, fg_color="#0F0F0F", height=300)
        self.preview_frame.pack(fill="both", expand=True, padx=10, pady=(0, 10))
        
        # Preview placeholder
        self.preview_label = ctk.CTkLabel(self.preview_frame, 
                                         text="No video loaded\n\nUpload a video to see preview", 
                                         font=("Consolas", 12), text_color="gray",
                                         justify="center")
        self.preview_label.pack(expand=True)
        
        # Project info
        info_frame = ctk.CTkFrame(right_frame, fg_color="#2B2B2B")
        info_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.project_info = ctk.CTkLabel(info_frame, text="📁 Project: New", 
                                        font=("Consolas", 10), text_color="white")
        self.project_info.pack(pady=5)
        
        self.clips_info = ctk.CTkLabel(info_frame, text="🎬 Clips: 0 | 🎵 Audio: 0 | 🖼️ Photos: 0", 
                                      font=("Consolas", 10), text_color="white")
        self.clips_info.pack(pady=5)
        
        # Tutorial button
        tutorial_frame = ctk.CTkFrame(right_frame, fg_color="#2B2B2B")
        tutorial_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        self.tutorial_btn = ctk.CTkButton(tutorial_frame, text="📚 TUTORIAL", 
                                         font=("Consolas", 14, "bold"),
                                         fg_color="#4CAF50", hover_color="#45a049",
                                         command=self.show_tutorial, height=40)
        self.tutorial_btn.pack(pady=5)
        
        # Bottom command area
        bottom_frame = ctk.CTkFrame(main_frame, fg_color="#2B2B2B")
        bottom_frame.pack(fill="x", padx=10, pady=(0, 10))
        
        # Suggestions area
        self.suggestions_frame = ctk.CTkFrame(bottom_frame, fg_color="#1E1E1E", height=60)
        self.suggestions_frame.pack(fill="x", pady=(0, 5))
        
        self.suggestions_label = ctk.CTkLabel(self.suggestions_frame, 
                                             text="💡 Tip: Type 'help' for available commands", 
                                             font=("Consolas", 11), text_color="#888888")
        self.suggestions_label.pack(expand=True)
        
        # Command input frame
        input_frame = ctk.CTkFrame(bottom_frame, fg_color="#3B3B3B")
        input_frame.pack(fill="x")
        
        # Command prompt
        self.prompt_label = ctk.CTkLabel(input_frame, text="vedit> ", 
                                        font=("Consolas", 14), text_color="green")
        self.prompt_label.pack(side="left", padx=(10, 5))
        
        # Command entry
        self.command_entry = ctk.CTkEntry(input_frame, font=("Consolas", 14), 
                                         fg_color="#1E1E1E", text_color="green",
                                         border_color="green", height=35)
        self.command_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        self.command_entry.bind("<Return>", self.execute_command)
        self.command_entry.bind("<KeyRelease>", self.on_key_release)
        self.command_entry.focus()
        
        # Status bar
        self.status_label = ctk.CTkLabel(main_frame, text="Ready", 
                                        font=("Consolas", 10), text_color="gray")
        self.status_label.pack(side="bottom", pady=5)
        
        # Initialize suggestions
        self.suggestions = [
            "💡 Tip: Type 'help' for available commands",
            "💡 Tip: Use 'upload dialog' to easily select files",
            "💡 Tip: Times can be in MM:SS or SS format",
            "💡 Tip: Click TUTORIAL button for interactive help",
            "💡 Tip: Use 'list' to see all loaded clips",
            "💡 Tip: Use 'clear' to clear the output",
            "💡 Tip: Type 'upload' followed by file path",
            "💡 Tip: Use 'video_1: remove(0:10, 0:30)' to edit clips",
            "💡 Tip: Add overlays with 'overlay(source, from, to, effect)'",
            "💡 Tip: Add text with 'text(\"Hello\", center, 48, white)'",
            "💡 Tip: Control overlay size with 'overlay_settings fill_mode fit'",
            "💡 Tip: Remove audio with 'audio remove'",
            "💡 Tip: Export with 'export(C:\\MyVideos)'",
            "💡 Tip: Use 'merge_all' to set dissolve transition (default)",
            "💡 Tip: Save projects with 'project save'",
            "💡 Tip: Create GIF videos with 'gif audio_1 animation.gif'"
        ]
        self.current_suggestion = 0
        self.suggestion_visible = True
        
        # Start suggestion animation
        self.animate_suggestions()
        
        # Welcome message
        self.log("VEdit CLI - Video Editor v1.0")
        self.log("Type 'help' for available commands or click TUTORIAL button")
        self.log("=" * 60)
        
    def log(self, message, color="white"):
        """Log message to output with timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.output_text.insert("end", f"[{timestamp}] {message}\n")
        self.output_text.see("end")
        self.root.update_idletasks()
        
    def animate_suggestions(self):
        """Animate suggestions with slow fade in/out"""
        if self.suggestion_visible:
            # Fade out current suggestion
            self.fade_out_suggestion()
        else:
            # Show next suggestion and fade in
            self.current_suggestion = (self.current_suggestion + 1) % len(self.suggestions)
            self.suggestions_label.configure(text=self.suggestions[self.current_suggestion])
            self.fade_in_suggestion()
            
    def fade_in_suggestion(self):
        """Fade in the current suggestion"""
        if not hasattr(self, 'fade_step'):
            self.fade_step = 0
            
        if self.fade_step >= 8:  # 8 steps to full opacity
            self.suggestion_visible = True
            self.fade_step = 0
            # Schedule next animation
            self.root.after(4000, self.animate_suggestions)  # 4 seconds visible
        else:
            # Use predefined color steps
            colors = ["#000000", "#111111", "#222222", "#333333", "#444444", "#555555", "#666666", "#777777", "#888888"]
            self.suggestions_label.configure(text_color=colors[self.fade_step])
            self.fade_step += 1
            self.root.after(150, self.fade_in_suggestion)  # 150ms intervals
            
    def fade_out_suggestion(self):
        """Fade out the current suggestion"""
        if not hasattr(self, 'fade_step'):
            self.fade_step = 8
            
        if self.fade_step <= 0:  # 8 steps to full transparency
            self.suggestion_visible = False
            self.fade_step = 8
            # Schedule next animation
            self.root.after(2000, self.animate_suggestions)  # 2 seconds hidden
        else:
            # Use predefined color steps
            colors = ["#000000", "#111111", "#222222", "#333333", "#444444", "#555555", "#666666", "#777777", "#888888"]
            self.suggestions_label.configure(text_color=colors[self.fade_step])
            self.fade_step -= 1
            self.root.after(150, self.fade_out_suggestion)  # 150ms intervals
            
    def on_key_release(self, event=None):
        """Handle key release events for real-time feedback"""
        # Update project info when typing
        self.update_project_info()
        
    def update_project_info(self):
        """Update the project information display"""
        clips_count = len(self.clips)
        audio_count = len(self.audio_clips)
        photos_count = len(self.photo_clips)
        
        self.clips_info.configure(text=f"🎬 Clips: {clips_count} | 🎵 Audio: {audio_count} | 🖼️ Photos: {photos_count}")
        
    def update_preview(self, clip_name=None):
        """Update the preview panel"""
        if clip_name and clip_name in self.clips:
            clip = self.clips[clip_name]
            duration = clip.duration
            size = f"{clip.w}x{clip.h}"
            fps = clip.fps if hasattr(clip, 'fps') else "Unknown"
            
            preview_text = f"🎬 {clip_name}\n\n"
            preview_text += f"Duration: {duration:.2f}s\n"
            preview_text += f"Size: {size}\n"
            preview_text += f"FPS: {fps}\n"
            
            if clip.audio:
                preview_text += "Audio: Yes\n"
            else:
                preview_text += "Audio: No\n"
                
            self.preview_label.configure(text=preview_text, text_color="white")
        else:
            total_clips = len(self.clips) + len(self.photo_clips)
            if total_clips > 0:
                preview_text = f"📁 Project loaded\n\n"
                preview_text += f"Total clips: {total_clips}\n"
                preview_text += f"Audio files: {len(self.audio_clips)}\n"
                preview_text += f"Overlays: {len(self.overlay_clips)}\n"
                preview_text += f"Text overlays: {len(self.text_overlays)}"
                self.preview_label.configure(text=preview_text, text_color="cyan")
            else:
                self.preview_label.configure(text="No video loaded\n\nUpload a video to see preview", text_color="gray")
        
    def execute_command(self, event=None):
        """Execute the entered command"""
        command = self.command_entry.get().strip()
        if not command:
            return
            
        # Change command color to bright green when executed
        self.command_entry.configure(text_color="#00FF00")
        self.root.after(100, lambda: self.command_entry.configure(text_color="green"))
        
        self.log(f"vedit> {command}", "green")
        self.command_entry.delete(0, "end")
        
        try:
            self.parse_and_execute(command)
        except Exception as e:
            self.log(f"Error: {str(e)}", "red")
            
    def parse_and_execute(self, command):
        """Parse and execute the command"""
        command = command.lower().strip()
        
        # Upload commands
        if command.startswith("upload"):
            self.handle_upload(command)
        # Clip manipulation commands
        elif ":" in command and ("remove" in command or "trim" in command):
            self.handle_clip_manipulation(command)
        # Merge commands
        elif command.startswith("merge"):
            self.handle_merge(command)
        # Export commands
        elif command.startswith("export"):
            self.handle_export(command)
        # Overlay commands
        elif command.startswith("overlay"):
            self.handle_overlay(command)
        # Text overlay commands
        elif command.startswith("text"):
            self.handle_text_overlay(command)
        # Audio commands
        elif command.startswith("audio"):
            self.handle_audio(command)
        # Split commands
        elif command.startswith("split"):
            self.handle_split(command)
        # GIF overlay commands
        elif command.startswith("gif"):
            self.handle_gif_overlay(command)
        # Help commands
        elif command in ["help", "h", "?"]:
            self.show_help()
        # Clear commands
        elif command in ["clear", "cls"]:
            self.output_text.delete("1.0", "end")
        # List commands
        elif command in ["list", "ls"]:
            self.list_clips()
        # Project commands
        elif command.startswith("project"):
            self.handle_project(command)
        # Overlay settings commands
        elif command.startswith("overlay_settings"):
            self.handle_overlay_settings(command)
        else:
            self.log(f"Unknown command: {command}", "red")
            
    def handle_upload(self, command):
        """Handle upload commands"""
        # Extract file path from command
        match = re.search(r'upload\s+(.+)', command)
        if not match:
            self.log("Usage: upload <file_path>", "yellow")
            return
            
        file_path = match.group(1).strip()
        
        # Open file dialog if path is not provided
        if file_path == "dialog":
            file_path = filedialog.askopenfilename(
                title="Select video/audio/photo file",
                filetypes=[
                    ("Video files", "*.mp4 *.avi *.mov *.mkv *.wmv"),
                    ("Audio files", "*.mp3 *.wav *.aac *.flac"),
                    ("Image files", "*.jpg *.jpeg *.png *.bmp *.gif"),
                    ("All files", "*.*")
                ]
            )
            
        if not file_path or not os.path.exists(file_path):
            self.log(f"File not found: {file_path}", "red")
            return
            
        try:
            file_ext = Path(file_path).suffix.lower()
            
            if file_ext in ['.mp4', '.avi', '.mov', '.mkv', '.wmv']:
                # Video file
                clip = VideoFileClip(file_path)
                clip_name = f"video_{len(self.clips) + 1}"
                self.clips[clip_name] = clip
                self.log(f"Uploaded video: {clip_name} ({clip.duration:.2f}s)")
                self.update_preview(clip_name)
                self.update_project_info()
                
            elif file_ext in ['.mp3', '.wav', '.aac', '.flac']:
                # Audio file
                audio = AudioFileClip(file_path)
                audio_name = f"audio_{len(self.audio_clips) + 1}"
                self.audio_clips[audio_name] = audio
                self.log(f"Uploaded audio: {audio_name} ({audio.duration:.2f}s)")
                self.update_project_info()
                
            elif file_ext in ['.jpg', '.jpeg', '.png', '.bmp', '.gif']:
                # Image file
                if file_ext == '.gif':
                    clip = VideoFileClip(file_path)
                else:
                    # Convert image to video clip
                    img = Image.open(file_path)
                    # Create a 3-second video from image
                    clip = ImageClip(file_path, duration=3)
                    
                photo_name = f"photo_{len(self.photo_clips) + 1}"
                self.photo_clips[photo_name] = clip
                self.log(f"Uploaded photo: {photo_name} ({clip.duration:.2f}s)")
                self.update_project_info()
                
        except Exception as e:
            self.log(f"Error uploading file: {str(e)}", "red")
            
    def handle_clip_manipulation(self, command):
        """Handle clip manipulation commands like remove and trim"""
        # Parse clip name and operation
        match = re.search(r'(\w+):\s*(remove|trim)\s*\(([^)]+)\)', command)
        if not match:
            self.log("Usage: clip_name: remove(start_time, end_time)", "yellow")
            return
            
        clip_name, operation, time_range = match.groups()
        
        # Find the clip
        clip = None
        if clip_name in self.clips:
            clip = self.clips[clip_name]
        elif clip_name in self.photo_clips:
            clip = self.photo_clips[clip_name]
        else:
            self.log(f"Clip '{clip_name}' not found", "red")
            return
            
        # Parse time range
        times = time_range.split(',')
        if len(times) != 2:
            self.log("Time range must be in format: start_time, end_time", "yellow")
            return
            
        try:
            start_time = self.parse_time(times[0].strip())
            end_time = self.parse_time(times[1].strip())
            
            if operation == "remove":
                # Remove the specified section
                if start_time == 0:
                    # Remove from beginning
                    new_clip = clip.subclip(end_time, clip.duration)
                elif end_time >= clip.duration:
                    # Remove from end
                    new_clip = clip.subclip(0, start_time)
                else:
                    # Remove middle section
                    part1 = clip.subclip(0, start_time)
                    part2 = clip.subclip(end_time, clip.duration)
                    new_clip = concatenate_videoclips([part1, part2])
                    
            elif operation == "trim":
                # Trim to specified range
                new_clip = clip.subclip(start_time, end_time)
                
            # Update the clip
            if clip_name in self.clips:
                self.clips[clip_name] = new_clip
            else:
                self.photo_clips[clip_name] = new_clip
                
            self.log(f"Modified {clip_name}: {operation}({start_time:.2f}s, {end_time:.2f}s)")
            
        except Exception as e:
            self.log(f"Error processing clip: {str(e)}", "red")
            
    def parse_time(self, time_str):
        """Parse time string (MM:SS or SS format) to seconds"""
        if ':' in time_str:
            parts = time_str.split(':')
            if len(parts) == 2:
                return int(parts[0]) * 60 + float(parts[1])
            elif len(parts) == 3:
                return int(parts[0]) * 3600 + int(parts[1]) * 60 + float(parts[2])
        return float(time_str)
        
    def handle_merge(self, command):
        """Handle merge commands"""
        # Check if merge_all() is called without parameters (default to dissolve)
        if command.strip() == "merge_all()":
            self.transition_type = "dissolve"
            self.log("Merge transition set to: dissolve (default)")
            return
            
        # Check if merge_all is called without parentheses (default to dissolve)
        if command.strip() == "merge_all":
            self.transition_type = "dissolve"
            self.log("Merge transition set to: dissolve (default)")
            return
            
        # Parse merge_all(transition_type)
        match = re.search(r'merge_all\s*\((\w+)\)', command)
        if match:
            transition = match.group(1)
            self.transition_type = transition
            self.log(f"Merge transition set to: {transition}")
        else:
            self.log("Usage: merge_all or merge_all(transition_type)", "yellow")
            
    def handle_export(self, command):
        """Handle export commands"""
        match = re.search(r'export\s*\(([^)]+)\)', command)
        if not match:
            self.log("Usage: export(output_path)", "yellow")
            return
            
        output_path = match.group(1).strip()
        
        # Create output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)
        
        self.output_path = output_path
        self.log(f"Export path set to: {output_path}")
        
        # Start export process in background
        threading.Thread(target=self.export_project, daemon=True).start()
        
    def export_project(self):
        """Export the project to video file"""
        try:
            self.status_label.configure(text="Exporting...")
            self.log("Starting export process...", "cyan")
            
            if not self.clips and not self.photo_clips:
                self.log("No clips to export", "red")
                return
                
            # Combine all clips
            all_clips = list(self.clips.values()) + list(self.photo_clips.values())
            
            if len(all_clips) == 1:
                final_video = all_clips[0]
            else:
                # Apply transitions
                if self.transition_type == "dissolve":
                    final_video = concatenate_videoclips(all_clips, method="compose")
                else:
                    final_video = concatenate_videoclips(all_clips)
                    
            # Apply overlays
            final_video = self.apply_overlays(final_video)
            
            # Apply text overlays
            final_video = self.apply_text_overlays(final_video)
            
            # Apply audio overdubs
            final_video = self.apply_audio_overdubs(final_video)
            
            # Generate output filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            output_file = os.path.join(self.output_path, f"vedit_export_{timestamp}.mp4")
            
            # Export
            self.log(f"Exporting to: {output_file}")
            final_video.write_videofile(output_file, 
                                      codec='libx264', 
                                      audio_codec='aac',
                                      temp_audiofile='temp-audio.m4a',
                                      remove_temp=True)
            
            self.log(f"Export completed: {output_file}", "green")
            self.status_label.configure(text="Export completed")
            
        except Exception as e:
            self.log(f"Export error: {str(e)}", "red")
            self.status_label.configure(text="Export failed")
            
    def handle_overlay(self, command):
        """Handle overlay commands"""
        # Parse overlay command: overlay(source, from_time, to_time, effect)
        match = re.search(r'overlay\s*\(([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)', command)
        if not match:
            self.log("Usage: overlay(source, from_time, to_time, effect)", "yellow")
            return
            
        source, from_time, to_time, effect = match.groups()
        
        try:
            from_time = self.parse_time(from_time.strip())
            to_time = self.parse_time(to_time.strip())
            
            # Find source clip
            source_clip = None
            if source in self.clips:
                source_clip = self.clips[source]
            elif source in self.photo_clips:
                source_clip = self.photo_clips[source]
            else:
                self.log(f"Source '{source}' not found", "red")
                return
                
            overlay_info = {
                'clip': source_clip,
                'from_time': from_time,
                'to_time': to_time,
                'effect': effect.strip()
            }
            
            self.overlay_clips.append(overlay_info)
            self.log(f"Overlay added: {source} ({from_time:.2f}s - {to_time:.2f}s) with {effect}")
            
        except Exception as e:
            self.log(f"Error adding overlay: {str(e)}", "red")
            
    def apply_overlays(self, base_video):
        """Apply overlays to the base video"""
        if not self.overlay_clips:
            return base_video
            
        for overlay in self.overlay_clips:
            try:
                clip = overlay['clip']
                from_time = overlay['from_time']
                to_time = overlay['to_time']
                effect = overlay['effect']
                
                # Trim overlay clip to duration
                duration = to_time - from_time
                overlay_clip = clip.subclip(0, min(duration, clip.duration))
                
                # Resize overlay based on configuration
                from config import CONFIG
                overlay_config = CONFIG['video']
                
                # Log original overlay size for debugging
                original_size = f"{overlay_clip.w}x{overlay_clip.h}"
                base_size = f"{base_video.w}x{base_video.h}"
                
                if overlay_config['overlay_fill_mode'] == 'stretch':
                    # Stretch to fill entire screen (original behavior)
                    overlay_clip = overlay_clip.resize(width=base_video.w, height=base_video.h)
                    self.log(f"Overlay resized (stretch): {original_size} -> {base_size}")
                else:
                    # Fit while maintaining aspect ratio (default)
                    max_size_percent = overlay_config['overlay_max_size_percent'] / 100.0
                    max_width = int(base_video.w * max_size_percent)
                    max_height = int(base_video.h * max_size_percent)
                    
                    # Calculate aspect ratios
                    base_aspect = base_video.w / base_video.h
                    overlay_aspect = overlay_clip.w / overlay_clip.h
                    
                    # Resize to fit within bounds while maintaining aspect ratio
                    if overlay_aspect > base_aspect:
                        # Overlay is wider - resize by width first
                        overlay_clip = overlay_clip.resize(width=max_width)
                        if overlay_clip.h > max_height:
                            overlay_clip = overlay_clip.resize(height=max_height)
                    else:
                        # Overlay is taller - resize by height first
                        overlay_clip = overlay_clip.resize(height=max_height)
                        if overlay_clip.w > max_width:
                            overlay_clip = overlay_clip.resize(width=max_width)
                    
                    # Log final size for debugging
                    final_size = f"{overlay_clip.w}x{overlay_clip.h}"
                    self.log(f"Overlay resized (fit): {original_size} -> {final_size} (max: {max_width}x{max_height})")
                
                # Apply effects
                if effect == "fade-in-out":
                    overlay_clip = overlay_clip.fadein(0.5).fadeout(0.5)
                elif effect == "pop-in-fade-out":
                    overlay_clip = overlay_clip.fadeout(0.5)
                    
                # Composite overlay
                base_video = CompositeVideoClip([
                    base_video,
                    overlay_clip.set_position('center').set_start(from_time)
                ])
                
            except Exception as e:
                self.log(f"Error applying overlay: {str(e)}", "red")
                
        return base_video
        
    def handle_text_overlay(self, command):
        """Handle text overlay commands"""
        # Parse text command: text("text", position, size, color)
        match = re.search(r'text\s*\(([^,]+),\s*([^,]+),\s*([^,]+),\s*([^)]+)\)', command)
        if not match:
            self.log("Usage: text(\"text\", position, size, color)", "yellow")
            return
            
        text, position, size, color = match.groups()
        text = text.strip('"')
        
        text_info = {
            'text': text,
            'position': position.strip(),
            'size': int(size.strip()),
            'color': color.strip()
        }
        
        self.text_overlays.append(text_info)
        self.log(f"Text overlay added: \"{text}\" at {position}")
        
    def apply_text_overlays(self, video):
        """Apply text overlays to video"""
        if not self.text_overlays:
            return video
            
        clips = [video]
        
        for text_info in self.text_overlays:
            try:
                # Create text clip
                txt_clip = TextClip(text_info['text'], 
                                  fontsize=text_info['size'],
                                  color=text_info['color'],
                                  bg_color='white',
                                  stroke_color='black',
                                  stroke_width=2)
                                  
                # Position text
                if text_info['position'] == 'center':
                    txt_clip = txt_clip.set_position('center')
                elif text_info['position'] == 'top':
                    txt_clip = txt_clip.set_position(('center', 50))
                elif text_info['position'] == 'bottom':
                    txt_clip = txt_clip.set_position(('center', video.h - 100))
                else:
                    txt_clip = txt_clip.set_position(text_info['position'])
                    
                # Set duration
                txt_clip = txt_clip.set_duration(video.duration)
                
                clips.append(txt_clip)
                
            except Exception as e:
                self.log(f"Error applying text overlay: {str(e)}", "red")
                
        return CompositeVideoClip(clips)
        
    def handle_audio(self, command):
        """Handle audio commands"""
        if command.startswith("audio remove"):
            # Remove audio from all clips
            for name, clip in self.clips.items():
                self.clips[name] = clip.without_audio()
            for name, clip in self.photo_clips.items():
                self.photo_clips[name] = clip.without_audio()
            self.log("Audio removed from all clips")
            
        elif command.startswith("audio overdub"):
            # Parse overdub command
            match = re.search(r'audio overdub\s+(\w+)\s+(\d+:\d+)', command)
            if match:
                audio_name, start_time = match.groups()
                if audio_name in self.audio_clips:
                    start_time = self.parse_time(start_time)
                    self.audio_overdubs.append({
                        'audio': self.audio_clips[audio_name],
                        'start_time': start_time
                    })
                    self.log(f"Audio overdub added: {audio_name} at {start_time:.2f}s")
                else:
                    self.log(f"Audio '{audio_name}' not found", "red")
            else:
                self.log("Usage: audio overdub audio_name start_time", "yellow")
                
    def apply_audio_overdubs(self, video):
        """Apply audio overdubs to video"""
        if not self.audio_overdubs:
            return video
            
        audio_tracks = [video.audio] if video.audio else []
        
        for overdub in self.audio_overdubs:
            try:
                audio = overdub['audio']
                start_time = overdub['start_time']
                
                # Set start time for audio
                audio = audio.set_start(start_time)
                audio_tracks.append(audio)
                
            except Exception as e:
                self.log(f"Error applying audio overdub: {str(e)}", "red")
                
        if len(audio_tracks) > 1:
            # Mix audio tracks
            final_audio = CompositeAudioClip(audio_tracks)
            return video.set_audio(final_audio)
            
        return video
        
    def handle_split(self, command):
        """Handle split commands"""
        match = re.search(r'split\s+(\w+)\s+(\d+:\d+)', command)
        if not match:
            self.log("Usage: split clip_name time", "yellow")
            return
            
        clip_name, split_time = match.groups()
        split_time = self.parse_time(split_time)
        
        # Find clip
        clip = None
        if clip_name in self.clips:
            clip = self.clips[clip_name]
            del self.clips[clip_name]
        elif clip_name in self.photo_clips:
            clip = self.photo_clips[clip_name]
            del self.photo_clips[clip_name]
        else:
            self.log(f"Clip '{clip_name}' not found", "red")
            return
            
        # Split clip
        part1 = clip.subclip(0, split_time)
        part2 = clip.subclip(split_time, clip.duration)
        
        # Add split parts
        self.clips[f"{clip_name}_part1"] = part1
        self.clips[f"{clip_name}_part2"] = part2
        
        self.log(f"Split {clip_name} at {split_time:.2f}s into {clip_name}_part1 and {clip_name}_part2")
        
    def handle_overlay_settings(self, command):
        """Handle overlay settings commands"""
        from config import CONFIG
        
        if command.startswith("overlay_settings show"):
            # Show current settings
            settings = CONFIG['video']
            self.log("Current overlay settings:", "cyan")
            self.log(f"  Fill mode: {settings['overlay_fill_mode']}")
            self.log(f"  Maintain aspect ratio: {settings['overlay_maintain_aspect_ratio']}")
            self.log(f"  Max size: {settings['overlay_max_size_percent']}%")
            
        elif command.startswith("overlay_settings fill_mode"):
            # Change fill mode
            match = re.search(r'overlay_settings fill_mode\s+(\w+)', command)
            if match:
                mode = match.group(1).lower()
                if mode in ['fit', 'stretch']:
                    CONFIG['video']['overlay_fill_mode'] = mode
                    self.log(f"Overlay fill mode set to: {mode}", "green")
                else:
                    self.log("Invalid mode. Use 'fit' or 'stretch'", "red")
            else:
                self.log("Usage: overlay_settings fill_mode [fit|stretch]", "yellow")
                
        elif command.startswith("overlay_settings max_size"):
            # Change max size percentage
            match = re.search(r'overlay_settings max_size\s+(\d+)', command)
            if match:
                size = int(match.group(1))
                if 1 <= size <= 200:
                    CONFIG['video']['overlay_max_size_percent'] = size
                    self.log(f"Overlay max size set to: {size}%", "green")
                else:
                    self.log("Size must be between 1 and 200", "red")
            else:
                self.log("Usage: overlay_settings max_size <1-200>", "yellow")
        else:
            self.log("Usage:", "yellow")
            self.log("  overlay_settings show")
            self.log("  overlay_settings fill_mode [fit|stretch]")
            self.log("  overlay_settings max_size <1-200>")
        
    def handle_gif_overlay(self, command):
        """Handle GIF overlay on audio commands"""
        match = re.search(r'gif\s+(\w+)\s+(\w+)', command)
        if not match:
            self.log("Usage: gif audio_name gif_path", "yellow")
            return
            
        audio_name, gif_path = match.groups()
        
        if audio_name not in self.audio_clips:
            self.log(f"Audio '{audio_name}' not found", "red")
            return
            
        if not os.path.exists(gif_path):
            self.log(f"GIF file not found: {gif_path}", "red")
            return
            
        try:
            audio = self.audio_clips[audio_name]
            gif_clip = VideoFileClip(gif_path)
            
            # Loop GIF to match audio duration
            if gif_clip.duration < audio.duration:
                loops_needed = int(audio.duration / gif_clip.duration) + 1
                gif_clip = concatenate_videoclips([gif_clip] * loops_needed)
                
            # Trim to audio duration
            gif_clip = gif_clip.subclip(0, audio.duration)
            
            # Set audio
            video_with_audio = gif_clip.set_audio(audio)
            
            # Add to clips
            clip_name = f"gif_video_{len(self.clips) + 1}"
            self.clips[clip_name] = video_with_audio
            
            self.log(f"Created GIF video: {clip_name} ({audio.duration:.2f}s)")
            
        except Exception as e:
            self.log(f"Error creating GIF video: {str(e)}", "red")
            
    def handle_project(self, command):
        """Handle project commands"""
        if command == "project save":
            self.save_project()
        elif command == "project load":
            self.load_project()
        elif command == "project new":
            self.new_project()
        else:
            self.log("Usage: project [save|load|new]", "yellow")
            
    def save_project(self):
        """Save current project"""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".vedit",
            filetypes=[("VEdit project", "*.vedit")]
        )
        if file_path:
            # Save project data (simplified for demo)
            project_data = {
                'clips_count': len(self.clips),
                'audio_count': len(self.audio_clips),
                'photos_count': len(self.photo_clips),
                'overlays_count': len(self.overlay_clips),
                'text_overlays_count': len(self.text_overlays)
            }
            
            with open(file_path, 'w') as f:
                json.dump(project_data, f)
                
            self.log(f"Project saved: {file_path}")
            
    def load_project(self):
        """Load project"""
        file_path = filedialog.askopenfilename(
            filetypes=[("VEdit project", "*.vedit")]
        )
        if file_path:
            # Load project data (simplified for demo)
            with open(file_path, 'r') as f:
                project_data = json.load(f)
                
            self.log(f"Project loaded: {file_path}")
            self.log(f"Contains: {project_data['clips_count']} clips, "
                    f"{project_data['audio_count']} audio files, "
                    f"{project_data['photos_count']} photos")
                    
    def new_project(self):
        """Start new project"""
        self.clips.clear()
        self.audio_clips.clear()
        self.photo_clips.clear()
        self.overlay_clips.clear()
        self.text_overlays.clear()
        self.audio_overdubs.clear()
        self.log("New project started")
        
    def list_clips(self):
        """List all loaded clips"""
        if not self.clips and not self.audio_clips and not self.photo_clips:
            self.log("No clips loaded")
            self.update_preview()
            return
            
        self.log("=== LOADED CLIPS ===", "cyan")
        
        if self.clips:
            self.log("Video clips:", "yellow")
            for name, clip in self.clips.items():
                self.log(f"  {name}: {clip.duration:.2f}s")
                
        if self.audio_clips:
            self.log("Audio clips:", "yellow")
            for name, audio in self.audio_clips.items():
                self.log(f"  {name}: {audio.duration:.2f}s")
                
        if self.photo_clips:
            self.log("Photo clips:", "yellow")
            for name, photo in self.photo_clips.items():
                self.log(f"  {name}: {photo.duration:.2f}s")
                
        # Update preview with first video clip if available
        if self.clips:
            first_clip = list(self.clips.keys())[0]
            self.update_preview(first_clip)
        else:
            self.update_preview()
                
    def show_help(self):
        """Show help information"""
        help_text = """
=== VEdit CLI Help ===

UPLOAD COMMANDS:
  upload <file_path>          - Upload video/audio/photo file
  upload dialog               - Open file dialog to select file

CLIP MANIPULATION:
  clip_name: remove(start, end)  - Remove section from clip
  clip_name: trim(start, end)    - Trim clip to section
  split clip_name time           - Split clip at time

MERGE & EXPORT:
  merge_all                      - Set merge transition to dissolve (default)
  merge_all(transition)          - Set merge transition (dissolve, cut)
  export(output_path)            - Export to specified path

OVERLAY COMMANDS:
  overlay(source, from, to, effect)  - Overlay video/photo
  text("text", position, size, color) - Add text overlay
  overlay_settings show               - Show overlay settings
  overlay_settings fill_mode [fit|stretch] - Set overlay fill mode
  overlay_settings max_size <1-200>  - Set overlay max size percentage

AUDIO COMMANDS:
  audio remove                   - Remove audio from all clips
  audio overdub audio_name time  - Overdub audio at time

SPECIAL FEATURES:
  gif audio_name gif_path        - Create video from audio + GIF
  project [save|load|new]        - Project management

TIPS:
• Use 'list' to see all loaded clips
• Use 'help' for command reference
• Times can be MM:SS or SS format
• All commands are case-insensitive
        """
        self.log(help_text, "cyan")
        
    def show_tutorial(self):
        """Show interactive tutorial"""
        tutorial_window = ctk.CTkToplevel(self.root)
        tutorial_window.title("VEdit CLI Tutorial")
        tutorial_window.geometry("800x600")
        tutorial_window.configure(bg="#2B2B2B")
        
        # Tutorial content
        tutorial_text = """
🎬 VEdit CLI Tutorial

This tutorial will guide you through creating a video project step by step.

STEP 1: Upload Media
-------------------
Type: upload dialog
This opens a file browser to select your video/audio/photo files.

STEP 2: Edit Clips
-----------------
Example commands:
  video_1: remove(0:10, 0:30)    # Remove first 20 seconds
  video_1: remove(1:45, 2:15)    # Remove middle section
  video_1: trim(0:30, 1:30)      # Keep only 30s to 1m30s

STEP 3: Add Overlays
-------------------
Example commands:
  overlay(photo_1, 0:00, 0:05, fade-in-out)
  text("Hello World", center, 48, white)

STEP 4: Audio Operations
-----------------------
Example commands:
  audio remove                   # Remove all audio
  audio overdub music_1 0:00     # Add music from start

STEP 5: Merge & Export
---------------------
Example commands:
  merge_all(dissolve)            # Set transition
  export(C:\\MyVideos)           # Export to folder

ADVANCED FEATURES:
• Create GIF videos: gif audio_1 animation.gif
• Split clips: split video_1 1:30
• Project management: project save/load/new

TIPS:
• Use 'list' to see all loaded clips
• Use 'help' for command reference
• Times can be MM:SS or SS format
• All commands are case-insensitive
        """
        
        text_widget = ctk.CTkTextbox(tutorial_window, font=("Consolas", 12),
                                    fg_color="#1E1E1E", text_color="white")
        text_widget.pack(fill="both", expand=True, padx=10, pady=10)
        text_widget.insert("1.0", tutorial_text)
        
    def run(self):
        """Start the application"""
        self.root.mainloop()

if __name__ == "__main__":
    app = VideoEditorCLI()
    app.run() 