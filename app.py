from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from pathlib import Path
import sqlite3
import uvicorn
import webbrowser
import threading
import time
import json
from datetime import datetime
import asyncio
from typing import List, Dict

# Initialize FastAPI app
app = FastAPI()

# Setup paths
BASE_DIR = Path(__file__).resolve().parent
TEMPLATES = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Create necessary directories
(BASE_DIR / "static").mkdir(exist_ok=True)
(BASE_DIR / "templates").mkdir(exist_ok=True)

# Database setup
def init_db():
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    
    # Create users table if not exists
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            password TEXT NOT NULL,
            id_number TEXT UNIQUE NOT NULL,
            user_type TEXT NOT NULL
        )
    ''')
    
    # Create messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id TEXT NOT NULL,
            receiver_id TEXT NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Create meetings table
    c.execute('''
        CREATE TABLE IF NOT EXISTS meetings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            psychologist_id INTEGER NOT NULL,
            patient_id INTEGER NOT NULL,
            meeting_date DATE NOT NULL,
            meeting_time TIME NOT NULL,
            status TEXT DEFAULT 'scheduled',
            FOREIGN KEY (psychologist_id) REFERENCES users (id),
            FOREIGN KEY (patient_id) REFERENCES users (id)
        )
    ''')
    
    conn.commit()
    conn.close()

# Initialize database
init_db()

# Routes
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return TEMPLATES.TemplateResponse("index.html", {"request": request})

@app.get("/register", response_class=HTMLResponse)
async def register_page(request: Request, error: str = None):
    return TEMPLATES.TemplateResponse("register.html", {
        "request": request,
        "error": error
    })

@app.post("/register")
async def register(request: Request):
    form = await request.form()
    username = form.get("username")
    password = form.get("password")
    id_number = form.get("id_number")
    user_type = form.get("user_type")
    
    if not all([username, password, id_number, user_type]):
        return {"error": "All fields are required"}
    
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    
    # Check if ID number already exists
    c.execute('SELECT id FROM users WHERE id_number=?', (id_number,))
    if c.fetchone():
        conn.close()
        return {"error": "ID number already registered"}
    
    # Insert new user
    c.execute('INSERT INTO users (username, password, id_number, user_type) VALUES (?, ?, ?, ?)',
             (username, password, id_number, user_type))
    conn.commit()
    user_id = c.lastrowid
    conn.close()
    
    # Create response with redirect
    response = RedirectResponse(url=f"/options/{user_type}?user_id={user_id}&is_new_user=true", status_code=303)
    response.set_cookie(key="user_id", value=str(user_id), max_age=86400)  # 24 hours
    return response

@app.get("/login/{user_type}", response_class=HTMLResponse)
async def login_page(request: Request, user_type: str):
    if user_type not in ["soldier", "evacuee", "psychologist"]:
        return RedirectResponse(url="/")
    return TEMPLATES.TemplateResponse(f"login.html", {
        "request": request,
        "user_type": user_type
    })

@app.post("/login")
async def login(
    username: str = Form(...),
    password: str = Form(...),
    id_number: str = Form(...),
    user_type: str = Form(...)
):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    c.execute(
        'SELECT * FROM users WHERE username=? AND id_number=? AND user_type=?',
        (username, id_number, user_type)
    )
    user = c.fetchone()
    conn.close()
    
    if user and user[2] == password:  # In production, use proper password hashing
        if user_type in ["soldier", "evacuee", "psychologist"]:
            return RedirectResponse(url=f"/options/{user_type}", status_code=303)
        else:
            return RedirectResponse(url=f"/chat/{user_type}", status_code=303)
    return RedirectResponse(url=f"/login/{user_type}?error=1", status_code=303)

@app.get("/options/{user_type}", response_class=HTMLResponse)
async def options(
    request: Request,
    user_type: str,
    user_id: str = None,
    is_new_user: bool = False
):
    # Get user_id from URL or cookie
    if not user_id:
        user_id = request.cookies.get("user_id")
    
    user_info = None
    if user_id:
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        c.execute('SELECT username FROM users WHERE id=?', (user_id,))
        result = c.fetchone()
        if result:
            user_info = {"username": result[0]}
        conn.close()
    
    # Determine which template to use based on user_type
    template_name = f"{user_type}_options.html"
    
    return TEMPLATES.TemplateResponse(
        template_name,
        {
            "request": request,
            "user_id": user_id,
            "user_info": user_info,
            "is_new_user": is_new_user
        }
    )

@app.get("/chat-bot", response_class=HTMLResponse)
async def chat_bot(request: Request):
    return TEMPLATES.TemplateResponse("chat.html", {
        "request": request,
        "user_type": "bot",
        "user_id": request.cookies.get("user_id"),
        "receiver_id": "bot"  # Special ID for the bot
    })

@app.get("/chat/{user_type}", response_class=HTMLResponse)
async def chat(request: Request, user_type: str):
    # Get user ID from session or query parameters
    user_id = request.query_params.get('user_id')
    receiver_id = request.query_params.get('receiver_id')
    
    if not user_id:
        return RedirectResponse(url='/')
    
    return TEMPLATES.TemplateResponse("chat.html", {
        "request": request,
        "user_type": user_type,
        "user_id": user_id,
        "receiver_id": receiver_id
    })

# Message handling
@app.post("/api/messages")
async def send_message(
    sender_id: str = Form(...),
    receiver_id: str = Form(...),
    content: str = Form(...)
):
    try:
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        
        # Store the message
        c.execute(
            'INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)',
            (str(sender_id), str(receiver_id), content)
        )
        
        conn.commit()
        conn.close()
        return {"status": "success"}
    except Exception as e:
        print(f"Error sending message: {str(e)}")  # Add logging
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

@app.get("/api/messages/{user_id}")
async def get_messages(user_id: str):
    try:
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        
        # Get only messages sent by the user (for bot chat)
        c.execute('''
            SELECT sender_id, receiver_id, content, timestamp 
            FROM messages 
            WHERE sender_id = ?
            ORDER BY timestamp ASC
        ''', (str(user_id),))
        
        messages = []
        for row in c.fetchall():
            messages.append({
                "sender_id": row[0],
                "receiver_id": row[1],
                "content": row[2],
                "timestamp": row[3]
            })
        
        conn.close()
        return {"messages": messages}
    except Exception as e:
        print(f"Error getting messages: {str(e)}")  # Add logging
        return JSONResponse(
            status_code=500,
            content={"status": "error", "message": str(e)}
        )

# Meeting handling
@app.post("/api/meetings")
async def schedule_meeting(
    psychologist_id: int = Form(...),
    patient_id: int = Form(...),
    meeting_date: str = Form(...),
    meeting_time: str = Form(...)
):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO meetings (psychologist_id, patient_id, meeting_date, meeting_time) VALUES (?, ?, ?, ?)',
            (psychologist_id, patient_id, meeting_date, meeting_time)
        )
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

@app.get("/api/meetings/{user_id}")
async def get_meetings(user_id: int):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    try:
        c.execute('''
            SELECT m.*, 
                   u1.username as psychologist_name,
                   u2.username as patient_name
            FROM meetings m
            JOIN users u1 ON m.psychologist_id = u1.id
            JOIN users u2 ON m.patient_id = u2.id
            WHERE m.psychologist_id = ? OR m.patient_id = ?
            ORDER BY m.meeting_date, m.meeting_time
        ''', (user_id, user_id))
        meetings = c.fetchall()
        return {"meetings": meetings}
    finally:
        conn.close()

@app.get("/recover/username", response_class=HTMLResponse)
async def recover_username_page(request: Request, error: str = None):
    return TEMPLATES.TemplateResponse("recover_username.html", {
        "request": request,
        "error": error
    })

@app.post("/recover/username")
async def recover_username(
    id_number: str = Form(...),
    user_type: str = Form(...)
):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    try:
        c.execute(
            'SELECT username FROM users WHERE id_number=? AND user_type=?',
            (id_number, user_type)
        )
        result = c.fetchone()
        if result:
            return TEMPLATES.TemplateResponse("recover_username.html", {
                "request": Request,
                "success": f"שם המשתמש שלך הוא: {result[0]}"
            })
        else:
            return TEMPLATES.TemplateResponse("recover_username.html", {
                "request": Request,
                "error": "לא נמצא משתמש עם פרטים אלו"
            })
    finally:
        conn.close()

@app.get("/recover/password", response_class=HTMLResponse)
async def recover_password_page(request: Request, error: str = None, success: str = None):
    return TEMPLATES.TemplateResponse("recover_password.html", {
        "request": request,
        "error": error,
        "success": success
    })

@app.post("/recover/password")
async def recover_password(
    username: str = Form(...),
    id_number: str = Form(...),
    user_type: str = Form(...),
    new_password: str = Form(...),
    confirm_password: str = Form(...)
):
    if new_password != confirm_password:
        return TEMPLATES.TemplateResponse("recover_password.html", {
            "request": Request,
            "error": "הסיסמאות אינן תואמות"
        })
    
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    try:
        c.execute(
            'SELECT id FROM users WHERE username=? AND id_number=? AND user_type=?',
            (username, id_number, user_type)
        )
        result = c.fetchone()
        if result:
            c.execute(
                'UPDATE users SET password=? WHERE id=?',
                (new_password, result[0])
            )
            conn.commit()
            return TEMPLATES.TemplateResponse("recover_password.html", {
                "request": Request,
                "success": "הסיסמה שונתה בהצלחה"
            })
        else:
            return TEMPLATES.TemplateResponse("recover_password.html", {
                "request": Request,
                "error": "לא נמצא משתמש עם פרטים אלו"
            })
    finally:
        conn.close()

def open_browser():
    time.sleep(1.5)  # Wait a bit for the server to start
    webbrowser.open('http://localhost:8000')

if __name__ == "__main__":
    # Start the browser in a new thread
    threading.Thread(target=open_browser, daemon=True).start()
    # Start the FastAPI application
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)