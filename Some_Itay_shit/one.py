import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from enum import Enum

class UserType(Enum):
    SOLDIER = "חייל"
    EVACUEE = "מפונה"
    PSYCHOLOGIST = "פסיכולוג"

class CombatRole(Enum):
    FIGHTER = "לוחם"
    DRIVER = "נהג"
    MEDIC = "חובש"
    OTHER = "אחר"

class User:
    def __init__(self, name: str, user_type: UserType):
        self.name = name
        self.user_type = user_type
        self.current_chat: Optional['ChatRoom'] = None

class Soldier(User):
    def __init__(self, name: str, combat_role: CombatRole):
        super().__init__(name, UserType.SOLDIER)
        self.combat_role = combat_role

class Evacuee(User):
    def __init__(self, name: str, evacuated_from: str, evacuated_to: str):
        super().__init__(name, UserType.EVACUEE)
        self.evacuated_from = evacuated_from
        self.evacuated_to = evacuated_to

class Psychologist(User):
    def __init__(self, name: str):
        super().__init__(name, UserType.PSYCHOLOGIST)
        self.current_patient: Optional[User] = None

class ChatRoom:
    def __init__(self, room_type: UserType):
        self.room_type = room_type
        self.participants: List[User] = []
        self.max_participants = 5

    def add_participant(self, user: User) -> bool:
        if len(self.participants) < self.max_participants:
            self.participants.append(user)
            user.current_chat = self
            return True
        return False

    def remove_participant(self, user: User):
        if user in self.participants:
            self.participants.remove(user)
            user.current_chat = None

class ChatApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("מערכת צ'אט תמיכה")
        self.root.geometry("800x600")
        
        # Initialize data structures
        self.soldiers: List[Soldier] = []
        self.evacuees: List[Evacuee] = []
        self.psychologists: List[Psychologist] = []
        self.chat_rooms: List[ChatRoom] = []
        
        self.setup_gui()

    def setup_gui(self):
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Login section
        ttk.Label(main_frame, text="התחברות למערכת").grid(row=0, column=0, columnspan=2, pady=10)
        
        # User type selection
        ttk.Label(main_frame, text="סוג משתמש:").grid(row=1, column=0)
        self.user_type_var = tk.StringVar()
        user_type_combo = ttk.Combobox(main_frame, textvariable=self.user_type_var)
        user_type_combo['values'] = [user_type.value for user_type in UserType]
        user_type_combo.grid(row=1, column=1)

        # Name entry
        ttk.Label(main_frame, text="שם:").grid(row=2, column=0)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var).grid(row=2, column=1)

        # Login button
        ttk.Button(main_frame, text="התחבר", command=self.login).grid(row=3, column=0, columnspan=2, pady=10)

    def login(self):
        name = self.name_var.get()
        user_type = self.user_type_var.get()
        
        if not name or not user_type:
            messagebox.showerror("שגיאה", "נא למלא את כל השדות")
            return

        # Create appropriate user object based on type
        if user_type == UserType.SOLDIER.value:
            # TODO: Add combat role selection
            user = Soldier(name, CombatRole.FIGHTER)
            self.soldiers.append(user)
        elif user_type == UserType.EVACUEE.value:
            # TODO: Add evacuated from/to selection
            user = Evacuee(name, "תל אביב", "ירושלים")
            self.evacuees.append(user)
        elif user_type == UserType.PSYCHOLOGIST.value:
            user = Psychologist(name)
            self.psychologists.append(user)

        # TODO: Show appropriate chat interface based on user type
        messagebox.showinfo("התחברות", f"ברוך הבא {name}!")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ChatApp()
    app.run()
