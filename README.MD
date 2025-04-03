# Support Chat System

A real-time chat application designed to facilitate communication between soldiers, evacuees, and psychologists.

## Features

- User authentication and registration
- Role-based access control (Soldiers, Evacuees, Psychologists)
- Real-time chat functionality
- Private and group chat rooms
- Message history and persistence
- User profiles and preferences
- Military-inspired design theme

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/support-chat.git
cd support-chat
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the application:
```bash
python -m Hackaton-project.main
```

2. Register a new user or log in with existing credentials:
   - Soldiers: Provide ID, name, and combat role
   - Evacuees: Provide ID, name, and evacuation details
   - Psychologists: Provide ID, name, and license number

3. Use the chat interface to:
   - Join chat rooms
   - Send and receive messages
   - View participant information
   - Access role-specific features

## Project Structure

- `main.py`: Application entry point
- `welcome_screen.py`: Login and registration interface
- `chat_interface.py`: Main chat interface
- `chat_manager.py`: Chat room and message management
- `user.py`: Base user class and types
- `soldier.py`: Soldier-specific functionality
- `evacuee.py`: Evacuee-specific functionality
- `psychologist.py`: Psychologist-specific functionality

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.