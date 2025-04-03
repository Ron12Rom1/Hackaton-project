import tkinter as tk
from typing import Optional
from welcome_screen import WelcomeScreen
from chat_interface import (
    ChatInterface,
    SoldierChatInterface,
    EvacueeChatInterface,
    PsychologistChatInterface
)
from chat_manager import ChatManager
from user import User, UserType
from soldier import Soldier
from evacuee import Evacuee
from psychologist import Psychologist

class SupportChatApp:
    """Main application class for the Support Chat System"""
    
    def __init__(self):
        """Initialize the application"""
        # Create root window
        self.root = tk.Tk()
        self.root.title("Support Chat System")
        self.root.geometry("800x600")
        
        # Initialize managers
        self.chat_manager = ChatManager()
        
        # Initialize screens
        self.welcome_screen = WelcomeScreen(self.root, self.on_login)
        self.chat_interface: Optional[ChatInterface] = None
        
        # Show welcome screen
        self.welcome_screen.show()
        
        # Configure grid weights
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_rowconfigure(0, weight=1)
    
    def on_login(self, user: User) -> None:
        """
        Handle successful login
        
        Args:
            user: Logged in user
        """
        # Hide welcome screen
        self.welcome_screen.hide()
        
        # Create appropriate chat interface
        if isinstance(user, Soldier):
            self.chat_interface = SoldierChatInterface(
                self.root,
                self.chat_manager,
                user,
                self.on_logout
            )
        elif isinstance(user, Evacuee):
            self.chat_interface = EvacueeChatInterface(
                self.root,
                self.chat_manager,
                user,
                self.on_logout
            )
        elif isinstance(user, Psychologist):
            self.chat_interface = PsychologistChatInterface(
                self.root,
                self.chat_manager,
                user,
                self.on_logout
            )
        else:
            self.chat_interface = ChatInterface(
                self.root,
                self.chat_manager,
                user,
                self.on_logout
            )
        
        # Show chat interface
        self.chat_interface.show()
    
    def on_logout(self) -> None:
        """Handle logout"""
        if self.chat_interface:
            self.chat_interface.hide()
            self.chat_interface = None
        
        # Clear and show welcome screen
        self.welcome_screen.show()
    
    def run(self) -> None:
        """Run the application"""
        self.root.mainloop()

def main():
    """Application entry point"""
    app = SupportChatApp()
    app.run()

if __name__ == "__main__":
    main() 