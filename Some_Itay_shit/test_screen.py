import tkinter as tk
from tkinter import ttk
from welcome_screen import WelcomeScreen
from chat_interface import (
    ChatInterface,
    SoldierChatInterface,
    EvacueeChatInterface,
    PsychologistChatInterface
)
from chat_manager import ChatManager
from user import User, UserType
from soldier import Soldier, CombatRole
from evacuee import Evacuee
from psychologist import Psychologist

class TestScreen:
    """Test screen for viewing the main application window"""
    
    def __init__(self):
        """Initialize the test screen"""
        # Create root window
        self.root = tk.Tk()
        self.root.title("Support Chat System - Test Screen")
        self.root.geometry("800x600")
        
        # Initialize managers
        self.chat_manager = ChatManager()
        
        # Create welcome screen
        self.welcome_screen = WelcomeScreen(self.root, self.on_login)
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
        if hasattr(self, 'chat_interface'):
            self.chat_interface.hide()
            delattr(self, 'chat_interface')
        
        # Show welcome screen
        self.welcome_screen.show()
    
    def run(self) -> None:
        """Run the test screen"""
        self.root.mainloop()

def main():
    """Test screen entry point"""
    test_screen = TestScreen()
    test_screen.run()

if __name__ == "__main__":
    main() 