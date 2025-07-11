"""
Debug script to test color changes in VEdit CLI
"""

import tkinter as tk
import customtkinter as ctk

def test_color_change():
    """Test color change functionality"""
    
    # Create a simple test window
    root = ctk.CTk()
    root.title("Color Test")
    root.geometry("400x200")
    
    # Create an entry widget
    entry = ctk.CTkEntry(root, text_color="cyan", font=("Consolas", 14))
    entry.pack(pady=20)
    entry.insert(0, "Type here to see cyan text")
    
    def change_color():
        """Change color to test"""
        current_color = entry.cget("text_color")
        print(f"Current color: {current_color}")
        
        if current_color == "cyan":
            entry.configure(text_color="red")
            print("Changed to red")
        else:
            entry.configure(text_color="cyan")
            print("Changed to cyan")
    
    # Add a button to test color change
    button = ctk.CTkButton(root, text="Change Color", command=change_color)
    button.pack(pady=10)
    
    # Add a label to show current color
    label = ctk.CTkLabel(root, text="Current: cyan")
    label.pack(pady=10)
    
    def update_label():
        color = entry.cget("text_color")
        label.configure(text=f"Current: {color}")
        root.after(100, update_label)
    
    update_label()
    
    root.mainloop()

if __name__ == "__main__":
    test_color_change() 