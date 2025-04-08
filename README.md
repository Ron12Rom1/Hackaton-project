# Support Chat Application

A web application for providing support chat services between soldiers, evacuees, and psychologists.

## Features

- User authentication and authorization
- Role-based access control (Soldier, Evacuee, Psychologist)
- Secure chat functionality
- Real-time messaging
- User profile management

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
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

4. Set up environment variables:
Create a `.env` file in the root directory with the following content:
```
DATABASE_URL=sqlite:///./chat.db
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

## Running the Application

1. Start the development server:
```bash
uvicorn app:app --reload
```

2. Open your browser and navigate to:
```
http://localhost:8000
```

## API Documentation

Once the server is running, you can access the API documentation at:
```
http://localhost:8000/docs
```

## Project Structure

```
.
├── app.py              # Main application file
├── requirements.txt    # Project dependencies
├── .env               # Environment variables
├── static/            # Static files (CSS, JS, images)
├── templates/         # HTML templates
├── models/            # Database models
├── services/          # Business logic
└── api/               # API endpoints
```

## Security

- All passwords are hashed using bcrypt
- JWT tokens are used for authentication
- CORS is properly configured
- Environment variables are used for sensitive data

## Contributing

1. Fork the repository
2. Create a new branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License. 