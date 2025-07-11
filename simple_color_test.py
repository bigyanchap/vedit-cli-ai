"""
Simple test to verify CustomTkinter color changes are visible
"""

import customtkinter as ctk

def main():
    # Create window
    root = ctk.CTk()
    root.title("Color Test")
    root.geometry("500x300")
    
    # Disable theme to prevent override
    # ctk.set_default_color_theme("dark-blue")
    
    # Create entry with bright blue text
    entry = ctk.CTkEntry(root, text_color="#00FFFF", font=("Arial", 16))
    entry.pack(pady=20)
    entry.insert(0, "This should be bright blue text")
    
    # Create label to show current color
    color_label = ctk.CTkLabel(root, text="Current color: #00FFFF", font=("Arial", 14))
    color_label.pack(pady=10)
    
    def change_to_red():
        entry.configure(text_color="red")
        color_label.configure(text="Current color: red")
        print("Changed to red")
    
    def change_to_blue():
        entry.configure(text_color="#00FFFF")
        color_label.configure(text="Current color: #00FFFF")
        print("Changed to blue")
    
    def change_to_green():
        entry.configure(text_color="green")
        color_label.configure(text="Current color: green")
        print("Changed to green")
    
    # Create buttons
    red_btn = ctk.CTkButton(root, text="Red", command=change_to_red)
    red_btn.pack(pady=5)
    
    blue_btn = ctk.CTkButton(root, text="Blue", command=change_to_blue)
    blue_btn.pack(pady=5)
    
    green_btn = ctk.CTkButton(root, text="Green", command=change_to_green)
    green_btn.pack(pady=5)
    
    # Instructions
    instructions = ctk.CTkLabel(root, text="Click buttons to change text color\nType in the entry to see if color changes", 
                               font=("Arial", 12))
    instructions.pack(pady=20)
    
    print("Starting color test...")
    print("Entry should be bright blue (#00FFFF)")
    
    root.mainloop()

if __name__ == "__main__":
    main() 