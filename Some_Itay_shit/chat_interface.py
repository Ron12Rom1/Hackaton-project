import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from typing import Dict, List, Optional, Union, Callable
from datetime import datetime
import os
from PIL import Image, ImageTk
from chat_manager import ChatManager, ChatRoom
from user import User, UserType
from soldier import Soldier, CombatRole
from evacuee import Evacuee
from psychologist import Psychologist

class ChatInterface:
    """Class representing the chat interface"""
    
    def __init__(self,
                 root: tk.Tk,
                 chat_manager: ChatManager,
                 current_user: User,
                 on_logout: Callable[[], None]):
        """
        Initialize the chat interface
        
        Args:
            root: Root window
            chat_manager: ChatManager instance
            current_user: Currently logged in user
            on_logout: Callback function for logout
        """
        self.root = root
        self.chat_manager = chat_manager
        self.current_user = current_user
        self.on_logout = on_logout
        
        # Configure styles
        self.configure_styles()
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create header
        self.create_header()
        
        # Create chat area
        self.create_chat_area()
        
        # Create input area
        self.create_input_area()
        
        # Initialize state
        self.current_room: Optional[ChatRoom] = None
        self.current_dm_user: Optional[User] = None
        self.message_update_job: Optional[str] = None
        
        # Load user's rooms
        self.load_user_rooms()
        
        # Start message updates
        self.start_message_updates()
    
    def configure_styles(self) -> None:
        """Configure custom styles for the interface"""
        style = ttk.Style()
        
        # Configure colors
        style.configure("Chat.TFrame", background="#f0f0f0")
        style.configure("Header.TFrame", background="#1a4d2e")
        style.configure("Input.TFrame", background="#ffffff")
        
        # Configure fonts
        style.configure("Header.TLabel",
                       font=("Segoe UI", 12, "bold"),
                       foreground="white",
                       background="#1a4d2e")
        
        style.configure("Message.TLabel",
                       font=("Segoe UI", 10),
                       background="#f0f0f0")
        
        style.configure("Time.TLabel",
                       font=("Segoe UI", 8),
                       foreground="#666666",
                       background="#f0f0f0")
        
        # Configure buttons
        style.configure("Chat.TButton",
                       font=("Segoe UI", 10),
                       padding=5)
        
        style.map("Chat.TButton",
                 background=[("active", "#2a6d3e"), ("pressed", "#0d3d1a")],
                 foreground=[("active", "white"), ("pressed", "white")])
    
    def create_header(self) -> None:
        """Create the header section"""
        header_frame = ttk.Frame(self.main_frame, style="Header.TFrame")
        header_frame.grid(row=0, column=0, columnspan=2, sticky=(tk.W, tk.E))
        
        # User info
        user_frame = ttk.Frame(header_frame, style="Header.TFrame")
        user_frame.grid(row=0, column=0, sticky=tk.W, padx=10, pady=5)
        
        ttk.Label(user_frame,
                 text=f"Welcome, {self.current_user.full_name}",
                 style="Header.TLabel").grid(row=0, column=0, sticky=tk.W)
        
        ttk.Label(user_frame,
                 text=f"Type: {self.current_user.user_type.value}",
                 style="Header.TLabel").grid(row=1, column=0, sticky=tk.W)
        
        # Room selection
        room_frame = ttk.Frame(header_frame, style="Header.TFrame")
        room_frame.grid(row=0, column=1, sticky=tk.E, padx=10, pady=5)
        
        ttk.Label(room_frame,
                 text="Select Room:",
                 style="Header.TLabel").grid(row=0, column=0, sticky=tk.E)
        
        self.room_var = tk.StringVar()
        self.room_combo = ttk.Combobox(room_frame,
                                     textvariable=self.room_var,
                                     state="readonly",
                                     width=30)
        self.room_combo.grid(row=0, column=1, padx=5)
        self.room_combo.bind('<<ComboboxSelected>>', self.on_room_selected)
        
        # Logout button
        logout_button = ttk.Button(header_frame,
                                 text="Logout",
                                 command=self.on_logout,
                                 style="Chat.TButton")
        logout_button.grid(row=0, column=2, padx=10, pady=5)
    
    def create_chat_area(self) -> None:
        """Create the chat message display area"""
        chat_frame = ttk.Frame(self.main_frame, style="Chat.TFrame")
        chat_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Chat display
        self.chat_display = scrolledtext.ScrolledText(chat_frame,
                                                    wrap=tk.WORD,
                                                    width=60,
                                                    height=20)
        self.chat_display.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        self.chat_display.config(state=tk.DISABLED)
        
        # Configure grid weights
        chat_frame.grid_columnconfigure(0, weight=1)
        chat_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(1, weight=1)
    
    def create_input_area(self) -> None:
        """Create the message input area"""
        input_frame = ttk.Frame(self.main_frame, style="Input.TFrame")
        input_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        
        # Message input
        self.message_var = tk.StringVar()
        self.message_entry = ttk.Entry(input_frame,
                                     textvariable=self.message_var,
                                     width=50)
        self.message_entry.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5)
        self.message_entry.bind('<Return>', lambda e: self.send_message())
        
        # Send button
        send_button = ttk.Button(input_frame,
                               text="Send",
                               command=self.send_message,
                               style="Chat.TButton")
        send_button.grid(row=0, column=1, padx=5)
        
        # Configure grid weights
        input_frame.grid_columnconfigure(0, weight=1)
    
    def load_user_rooms(self) -> None:
        """Load and display available chat rooms"""
        rooms = self.chat_manager.get_user_rooms(self.current_user)
        room_names = [room.name for room in rooms]
        self.room_combo['values'] = room_names
        
        if room_names:
            self.room_combo.set(room_names[0])
            self.on_room_selected(None)
    
    def on_room_selected(self, event: Optional[tk.Event]) -> None:
        """
        Handle room selection
        
        Args:
            event: Optional event that triggered the selection
        """
        room_name = self.room_var.get()
        rooms = self.chat_manager.get_user_rooms(self.current_user)
        
        for room in rooms:
            if room.name == room_name:
                self.current_room = room
                self.current_dm_user = None
                self.update_chat_display()
                break
    
    def send_message(self) -> None:
        """Send a message in the current chat"""
        content = self.message_var.get().strip()
        if not content:
            return
        
        if self.current_room:
            # Send to room
            self.current_room.add_message(self.current_user, content)
        elif self.current_dm_user:
            # Send direct message
            self.chat_manager.send_direct_message(self.current_user,
                                                self.current_dm_user,
                                                content)
        
        self.message_var.set("")
        self.update_chat_display()
    
    def update_chat_display(self) -> None:
        """Update the chat display with current messages"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        
        if self.current_room:
            # Display room messages
            for message in self.current_room.messages:
                self.display_message(message)
        elif self.current_dm_user:
            # Display direct messages
            messages = self.chat_manager.get_direct_messages(self.current_user,
                                                          self.current_dm_user)
            for message in messages:
                self.display_message(message)
        
        self.chat_display.config(state=tk.DISABLED)
        self.chat_display.see(tk.END)
    
    def display_message(self, message: Dict[str, Union[str, datetime, Dict]]) -> None:
        """
        Display a single message in the chat
        
        Args:
            message: Message to display
        """
        # Format timestamp
        timestamp = message["timestamp"]
        if isinstance(timestamp, str):
            timestamp = datetime.fromisoformat(timestamp)
        time_str = timestamp.strftime("%H:%M")
        
        # Format sender name
        sender_name = message["sender_name"]
        if message["sender_id"] == self.current_user.user_id:
            sender_name = "You"
        
        # Add message to display
        self.chat_display.insert(tk.END, f"{sender_name} ({time_str}):\n", "sender")
        self.chat_display.insert(tk.END, f"{message['content']}\n\n", "message")
    
    def start_message_updates(self) -> None:
        """Start periodic message updates"""
        self.update_chat_display()
        self.message_update_job = self.root.after(5000, self.start_message_updates)
    
    def stop_message_updates(self) -> None:
        """Stop periodic message updates"""
        if self.message_update_job:
            self.root.after_cancel(self.message_update_job)
            self.message_update_job = None
    
    def show(self) -> None:
        """Show the chat interface"""
        self.main_frame.grid()
        self.start_message_updates()
    
    def hide(self) -> None:
        """Hide the chat interface"""
        self.stop_message_updates()
        self.main_frame.grid_remove()

class SoldierChatInterface(ChatInterface):
    """Class representing the soldier-specific chat interface"""
    
    def __init__(self,
                 root: tk.Tk,
                 chat_manager: ChatManager,
                 soldier: Soldier,
                 on_logout: Callable[[], None]):
        """
        Initialize the soldier chat interface
        
        Args:
            root: Root window
            chat_manager: ChatManager instance
            soldier: Currently logged in soldier
            on_logout: Callback function for logout
        """
        super().__init__(root, chat_manager, soldier, on_logout)
        self.setup_soldier_specific_controls()
    
    def setup_soldier_specific_controls(self) -> None:
        """Setup soldier-specific controls"""
        # Add combat role filter
        filter_frame = ttk.Frame(self.main_frame, style="Chat.TFrame")
        filter_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(filter_frame,
                 text="Filter by Combat Role:",
                 style="Message.TLabel").grid(row=0, column=0, padx=5)
        
        self.role_filter = ttk.Combobox(filter_frame,
                                      values=[role.value for role in CombatRole],
                                      state="readonly",
                                      width=20)
        self.role_filter.grid(row=0, column=1, padx=5)
        self.role_filter.set("All Roles")
        self.role_filter.bind('<<ComboboxSelected>>', self.filter_by_role)
    
    def filter_by_role(self, event: Optional[tk.Event]) -> None:
        """
        Filter messages by combat role
        
        Args:
            event: Optional event that triggered the filter
        """
        selected_role = self.role_filter.get()
        if selected_role != "All Roles":
            # TODO: Implement role-based filtering
            pass
        self.update_chat_display()

class EvacueeChatInterface(ChatInterface):
    """Class representing the evacuee-specific chat interface"""
    
    def __init__(self,
                 root: tk.Tk,
                 chat_manager: ChatManager,
                 evacuee: Evacuee,
                 on_logout: Callable[[], None]):
        """
        Initialize the evacuee chat interface
        
        Args:
            root: Root window
            chat_manager: ChatManager instance
            evacuee: Currently logged in evacuee
            on_logout: Callback function for logout
        """
        super().__init__(root, chat_manager, evacuee, on_logout)
        self.setup_evacuee_specific_controls()
    
    def setup_evacuee_specific_controls(self) -> None:
        """Setup evacuee-specific controls"""
        # Add location filter
        filter_frame = ttk.Frame(self.main_frame, style="Chat.TFrame")
        filter_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(filter_frame,
                 text="Filter by Location:",
                 style="Message.TLabel").grid(row=0, column=0, padx=5)
        
        self.location_filter = ttk.Combobox(filter_frame,
                                          state="readonly",
                                          width=20)
        self.location_filter.grid(row=0, column=1, padx=5)
        self.location_filter.set("All Locations")
        self.location_filter.bind('<<ComboboxSelected>>', self.filter_by_location)
    
    def filter_by_location(self, event: Optional[tk.Event]) -> None:
        """
        Filter messages by location
        
        Args:
            event: Optional event that triggered the filter
        """
        selected_location = self.location_filter.get()
        if selected_location != "All Locations":
            # TODO: Implement location-based filtering
            pass
        self.update_chat_display()

class PsychologistChatInterface(ChatInterface):
    """Class representing the psychologist-specific chat interface"""
    
    def __init__(self,
                 root: tk.Tk,
                 chat_manager: ChatManager,
                 psychologist: Psychologist,
                 on_logout: Callable[[], None]):
        """
        Initialize the psychologist chat interface
        
        Args:
            root: Root window
            chat_manager: ChatManager instance
            psychologist: Currently logged in psychologist
            on_logout: Callback function for logout
        """
        super().__init__(root, chat_manager, psychologist, on_logout)
        self.setup_psychologist_specific_controls()
    
    def setup_psychologist_specific_controls(self) -> None:
        """Setup psychologist-specific controls"""
        # Add patient selection
        patient_frame = ttk.Frame(self.main_frame, style="Chat.TFrame")
        patient_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(patient_frame,
                 text="Select Patient:",
                 style="Message.TLabel").grid(row=0, column=0, padx=5)
        
        self.patient_var = tk.StringVar()
        self.patient_combo = ttk.Combobox(patient_frame,
                                        textvariable=self.patient_var,
                                        state="readonly",
                                        width=30)
        self.patient_combo.grid(row=0, column=1, padx=5)
        self.patient_combo.bind('<<ComboboxSelected>>', self.select_patient)
        
        # Load patients
        self.load_patients()
    
    def load_patients(self) -> None:
        """Load and display available patients"""
        # TODO: Implement patient loading
        pass
    
    def select_patient(self, event: Optional[tk.Event]) -> None:
        """
        Handle patient selection
        
        Args:
            event: Optional event that triggered the selection
        """
        selected_patient = self.patient_var.get()
        if selected_patient:
            # TODO: Implement patient selection logic
            pass
        self.update_chat_display() 