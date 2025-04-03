import tkinter as tk
from tkinter import ttk

def create_display():
    """Create a simple one-time display of the chat interface"""
    # Create root window
    root = tk.Tk()
    root.title("Support Chat System - Display Only")
    root.geometry("800x600")
    
    # Configure styles
    style = ttk.Style()
    style.configure("TButton", padding=6, relief="flat", background="#4a90e2")
    style.configure("TLabel", padding=6)
    style.configure("TEntry", padding=6)
    
    # Create main frame
    main_frame = ttk.Frame(root)
    main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
    
    # Create header
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 10))
    
    # Title
    title_label = ttk.Label(
        header_frame,
        text="Support Chat System",
        font=("Arial", 24, "bold")
    )
    title_label.pack(side=tk.LEFT)
    
    # User info
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
        command=root.quit
    )
    logout_button.pack(side=tk.LEFT, padx=5)
    
    # Create chat area
    chat_frame = ttk.Frame(main_frame)
    chat_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    # Sample messages
    messages = [
        "Welcome to the Support Chat System!",
        "This is a display-only version of the UI.",
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
    
    # Create footer
    footer_frame = ttk.Frame(main_frame)
    footer_frame.pack(fill=tk.X, pady=(10, 0))
    
    # Message input
    message_entry = ttk.Entry(footer_frame)
    message_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
    
    send_button = ttk.Button(
        footer_frame,
        text="Send",
        command=lambda: None
    )
    send_button.pack(side=tk.RIGHT)
    
    # Run the application
    root.mainloop()

if __name__ == "__main__":
    create_display() 