import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, List, Optional, Union
import json
import os
from datetime import datetime
from user import User, UserType
from soldier import Soldier, CombatRole
from evacuee import Evacuee
from psychologist import Psychologist

class WelcomeScreen:
    """Welcome screen for the support chat application"""
    
    def __init__(self, root: tk.Tk, on_login: callable):
        """
        Initialize the welcome screen
        
        Args:
            root: Root window
            on_login: Callback function for successful login
        """
        self.root = root
        self.on_login = on_login
        
        # Configure window
        self.root.title("Support Chat - Welcome")
        self.root.geometry("800x600")
        self.root.configure(bg="#f0f0f0")
        
        # Load initial user data
        self.load_users_from_file()
        
        # Create main container
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Create UI elements
        self.create_header()
        self.create_content()
        self.create_footer()
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
    
    def load_users_from_file(self) -> None:
        """Load user data from JSON file"""
        users_file = os.path.join(os.path.dirname(__file__), "users.json")
        try:
            with open(users_file, "r") as f:
                self.users = json.load(f)
        except FileNotFoundError:
            # Initialize with default users if file doesn't exist
            self.users = {
                "soldiers": [
                    {
                        "id": "123456789",
                        "first_name": "John",
                        "last_name": "Smith",
                        "combat_role": "Infantry",
                        "unit": "101st Division",
                        "rank": "Sergeant"
                    },
                    {
                        "id": "987654321",
                        "first_name": "Mike",
                        "last_name": "Johnson",
                        "combat_role": "Armor",
                        "unit": "7th Brigade",
                        "rank": "Lieutenant"
                    }
                ],
                "evacuees": [
                    {
                        "id": "111222333",
                        "first_name": "Sarah",
                        "last_name": "Cohen",
                        "evacuated_from": "Tel Aviv",
                        "evacuated_to": "Jerusalem",
                        "family_size": 4
                    },
                    {
                        "id": "444555666",
                        "first_name": "David",
                        "last_name": "Levy",
                        "evacuated_from": "Haifa",
                        "evacuated_to": "Eilat",
                        "family_size": 3
                    }
                ],
                "psychologists": [
                    {
                        "id": "777888999",
                        "first_name": "Dr. Rachel",
                        "last_name": "Green",
                        "license": "PSY123456",
                        "specialization": "Trauma"
                    },
                    {
                        "id": "000111222",
                        "first_name": "Dr. James",
                        "last_name": "Wilson",
                        "license": "PSY789012",
                        "specialization": "Family Therapy"
                    }
                ]
            }
            self.save_users_to_file()
    
    def save_users_to_file(self) -> None:
        """Save user data to JSON file"""
        users_file = os.path.join(os.path.dirname(__file__), "users.json")
        with open(users_file, "w") as f:
            json.dump(self.users, f, indent=4)
    
    def create_header(self) -> None:
        """Create the header section"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Title
        title_label = ttk.Label(header_frame,
                              text="Support Chat System",
                              font=("Segoe UI", 24, "bold"))
        title_label.grid(row=0, column=0, sticky=tk.W)
        
        # Subtitle
        subtitle_label = ttk.Label(header_frame,
                                 text="Connect with support professionals",
                                 font=("Segoe UI", 12))
        subtitle_label.grid(row=1, column=0, sticky=tk.W)
    
    def create_content(self) -> None:
        """Create the main content section"""
        content_frame = ttk.Frame(self.main_frame)
        content_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Login section
        login_frame = ttk.LabelFrame(content_frame, text="Login", padding="10")
        login_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # User type selection
        ttk.Label(login_frame, text="User Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.user_type_var = tk.StringVar()
        user_type_combo = ttk.Combobox(login_frame,
                                     textvariable=self.user_type_var,
                                     values=["Soldier", "Evacuee", "Psychologist"],
                                     state="readonly")
        user_type_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # ID number
        ttk.Label(login_frame, text="ID Number:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.id_var = tk.StringVar()
        ttk.Entry(login_frame, textvariable=self.id_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # First name
        ttk.Label(login_frame, text="First Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.first_name_var = tk.StringVar()
        ttk.Entry(login_frame, textvariable=self.first_name_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Login button
        login_button = ttk.Button(login_frame,
                                text="Login",
                                command=self.do_login)
        login_button.grid(row=3, column=0, columnspan=2, pady=10)
        
        # Registration section
        register_frame = ttk.LabelFrame(content_frame, text="New User Registration", padding="10")
        register_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Registration fields
        ttk.Label(register_frame, text="User Type:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.reg_type_var = tk.StringVar()
        reg_type_combo = ttk.Combobox(register_frame,
                                    textvariable=self.reg_type_var,
                                    values=["Soldier", "Evacuee", "Psychologist"],
                                    state="readonly")
        reg_type_combo.grid(row=0, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(register_frame, text="ID Number:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.reg_id_var = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.reg_id_var).grid(row=1, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(register_frame, text="First Name:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.reg_first_name_var = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.reg_first_name_var).grid(row=2, column=1, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Label(register_frame, text="Last Name:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.reg_last_name_var = tk.StringVar()
        ttk.Entry(register_frame, textvariable=self.reg_last_name_var).grid(row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        
        # Register button
        register_button = ttk.Button(register_frame,
                                   text="Register",
                                   command=self.do_register)
        register_button.grid(row=4, column=0, columnspan=2, pady=10)
        
        # Configure grid weights
        content_frame.grid_columnconfigure(0, weight=1)
        login_frame.grid_columnconfigure(1, weight=1)
        register_frame.grid_columnconfigure(1, weight=1)
    
    def create_footer(self) -> None:
        """Create the footer section"""
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(20, 0))
        
        # Footer text
        footer_label = ttk.Label(footer_frame,
                               text="© 2024 Support Chat System. All rights reserved.",
                               font=("Segoe UI", 8))
        footer_label.grid(row=0, column=0, sticky=tk.W)
    
    def do_login(self) -> None:
        """Handle login attempt"""
        user_type = self.user_type_var.get().lower()
        user_id = self.id_var.get().strip()
        first_name = self.first_name_var.get().strip()
        
        if not all([user_type, user_id, first_name]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Find user in database
        user_list = self.users.get(user_type, [])
        user = next((u for u in user_list if u["id"] == user_id and u["first_name"] == first_name), None)
        
        if not user:
            messagebox.showerror("Error", "Invalid credentials")
            return
        
        # Create appropriate user object
        if user_type == "soldier":
            user_obj = Soldier(
                user_id=user["id"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                combat_role=CombatRole(user["combat_role"]),
                unit=user.get("unit", ""),
                rank=user.get("rank", "")
            )
        elif user_type == "evacuee":
            user_obj = Evacuee(
                user_id=user["id"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                evacuated_from=user["evacuated_from"],
                evacuated_to=user["evacuated_to"]
            )
        else:  # psychologist
            user_obj = Psychologist(
                user_id=user["id"],
                first_name=user["first_name"],
                last_name=user["last_name"],
                license_number=user["license"],
                specializations=[user["specialization"]]
            )
        
        # Call login callback
        self.on_login(user_obj)
    
    def do_register(self) -> None:
        """Handle user registration"""
        user_type = self.reg_type_var.get().lower()
        user_id = self.reg_id_var.get().strip()
        first_name = self.reg_first_name_var.get().strip()
        last_name = self.reg_last_name_var.get().strip()
        
        if not all([user_type, user_id, first_name, last_name]):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        # Check if user already exists
        user_list = self.users.get(user_type, [])
        if any(u["id"] == user_id for u in user_list):
            messagebox.showerror("Error", "User ID already exists")
            return
        
        # Create new user entry
        new_user = {
            "id": user_id,
            "first_name": first_name,
            "last_name": last_name
        }
        
        # Add type-specific fields
        if user_type == "soldier":
            new_user.update({
                "combat_role": "Infantry",
                "unit": "",
                "rank": ""
            })
        elif user_type == "evacuee":
            new_user.update({
                "evacuated_from": "",
                "evacuated_to": "",
                "family_size": 1
            })
        else:  # psychologist
            new_user.update({
                "license": "",
                "specialization": ""
            })
        
        # Add to database
        if user_type not in self.users:
            self.users[user_type] = []
        self.users[user_type].append(new_user)
        
        # Save to file
        self.save_users_to_file()
        
        messagebox.showinfo("Success", "Registration successful")
        
        # Clear fields
        self.reg_type_var.set("")
        self.reg_id_var.set("")
        self.reg_first_name_var.set("")
        self.reg_last_name_var.set("")
    
    def show(self) -> None:
        """Show the welcome screen"""
        self.main_frame.grid()
    
    def hide(self) -> None:
        """Hide the welcome screen"""
        self.main_frame.grid_remove() 