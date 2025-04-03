import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk

class SimpleDisplay:
    """Simple display class that shows just the UI without functionality"""
    
    def __init__(self):
        """Initialize the simple display"""
        # Create root window
        self.root = tk.Tk()
        self.root.title("Support Chat System - Simple Display")
        self.root.geometry("800x600")
        
        # Configure styles
        self.style = ttk.Style()
        self.style.configure("TButton", padding=6, relief="flat", background="#4a90e2")
        self.style.configure("TLabel", padding=6)
        self.style.configure("TEntry", padding=6)
        
        # Create main frame
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
        
        # Create header
        self.create_header()
        
        # Create content area
        self.create_content()
        
        # Create footer
        self.create_footer()
    
    def create_header(self):
        """Create the header section"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=10)
        
        # Title
        title_label = ttk.Label(
            header_frame,
            text="Support Chat System",
            font=("Arial", 24, "bold")
        )
        title_label.pack(side=tk.LEFT)
        
        # User info (dummy)
        user_frame = ttk.Frame(header_frame)
        user_frame.pack(side=tk.RIGHT)
        
        user_label = ttk.Label(
            user_frame,
            text="User: John Doe",
            font=("Arial", 12)
        )
        user_label.pack(side=tk.LEFT, padx=5)
        
        logout_button = ttk.Button(
            user_frame,
            text="Logout",
            command=self.root.quit
        )
        logout_button.pack(side=tk.LEFT, padx=5)
    
    def create_content(self):
        """Create the main content area"""
        content_frame = ttk.Frame(self.main_frame)
        content_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
        
        # Chat area (dummy)
        chat_frame = ttk.Frame(content_frame)
        chat_frame.pack(fill=tk.BOTH, expand=True)
        
        # Sample messages
        messages = [
            "Welcome to the Support Chat System!",
            "This is a simple display of the UI.",
            "No actual functionality is implemented.",
            "You can see how the interface looks.",
            "Feel free to explore the design."
        ]
        
        for i, message in enumerate(messages):
            message_frame = ttk.Frame(chat_frame)
            message_frame.pack(fill=tk.X, pady=5)
            
            sender_label = ttk.Label(
                message_frame,
                text=f"User {i+1}:",
                font=("Arial", 10, "bold")
            )
            sender_label.pack(side=tk.LEFT, padx=5)
            
            message_label = ttk.Label(
                message_frame,
                text=message,
                wraplength=500
            )
            message_label.pack(side=tk.LEFT, padx=5)
    
    def create_footer(self):
        """Create the footer section"""
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.grid(row=2, column=0, sticky="ew", padx=10, pady=10)
        
        # Message input (dummy)
        message_entry = ttk.Entry(footer_frame)
        message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        
        send_button = ttk.Button(
            footer_frame,
            text="Send",
            command=lambda: None
        )
        send_button.pack(side=tk.RIGHT)
    
    def run(self):
        """Run the simple display"""
        self.root.mainloop()

def main():
    """Simple display entry point"""
    display = SimpleDisplay()
    display.run()

if __name__ == "__main__":
    main() 