"""
VEdit CLI - Installation Test

This script tests if all dependencies are properly installed
and the application can be imported successfully.

Usage: python test_installation.py
"""

import sys
import importlib

def test_import(module_name, package_name=None):
    """Test if a module can be imported"""
    try:
        if package_name:
            module = importlib.import_module(module_name, package_name)
        else:
            module = importlib.import_module(module_name)
        print(f"✅ {module_name} - OK")
        return True
    except ImportError as e:
        print(f"❌ {module_name} - FAILED: {e}")
        return False
    except Exception as e:
        print(f"⚠️  {module_name} - WARNING: {e}")
        return True

def test_moviepy():
    """Test MoviePy specific functionality"""
    try:
        from moviepy.editor import VideoFileClip, AudioFileClip, ImageClip
        from moviepy.video.fx import resize
        print("✅ MoviePy core modules - OK")
        return True
    except ImportError as e:
        print(f"❌ MoviePy core modules - FAILED: {e}")
        return False

def test_gui_modules():
    """Test GUI-related modules"""
    try:
        import tkinter as tk
        import customtkinter as ctk
        from PIL import Image, ImageDraw, ImageFont
        print("✅ GUI modules - OK")
        return True
    except ImportError as e:
        print(f"❌ GUI modules - FAILED: {e}")
        return False

def test_video_processing():
    """Test video processing modules"""
    try:
        import cv2
        import numpy as np
        import imageio
        print("✅ Video processing modules - OK")
        return True
    except ImportError as e:
        print(f"❌ Video processing modules - FAILED: {e}")
        return False

def test_audio_processing():
    """Test audio processing modules"""
    try:
        from pydub import AudioSegment
        print("✅ Audio processing modules - OK")
        return True
    except ImportError as e:
        print(f"❌ Audio processing modules - FAILED: {e}")
        return False

def test_vedit_cli():
    """Test if VEdit CLI can be imported"""
    try:
        from vedit_cli import VideoEditorCLI
        print("✅ VEdit CLI - OK")
        return True
    except ImportError as e:
        print(f"❌ VEdit CLI - FAILED: {e}")
        return False
    except Exception as e:
        print(f"⚠️  VEdit CLI - WARNING: {e}")
        return True

def main():
    """Run all tests"""
    print("VEdit CLI - Installation Test")
    print("=" * 40)
    print()
    
    tests = [
        ("Python version", lambda: sys.version_info >= (3, 8)),
        ("MoviePy", test_moviepy),
        ("GUI modules", test_gui_modules),
        ("Video processing", test_video_processing),
        ("Audio processing", test_audio_processing),
        ("VEdit CLI", test_vedit_cli)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"Testing {test_name}...")
        if test_func():
            passed += 1
        print()
    
    print("=" * 40)
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! VEdit CLI is ready to use.")
        print("\nTo start the application:")
        print("1. Run: python vedit_cli.py")
        print("2. Or double-click: install_and_run.bat")
    else:
        print("❌ Some tests failed. Please check the installation.")
        print("\nTo fix installation issues:")
        print("1. Run: pip install -r requirements.txt")
        print("2. Or double-click: install_and_run.bat")
    
    print("\nFor more help, check the README.md file.")

if __name__ == "__main__":
    main() 