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
<<<<<<< HEAD
            username TEXT NOT NULL,
=======
            username TEXT UNIQUE NOT NULL,
>>>>>>> d2baf43536eed9c03f038796a65f3cecdddb4643
            password TEXT NOT NULL,
            id_number TEXT UNIQUE NOT NULL,
            user_type TEXT NOT NULL
        )
    ''')
    
    # Create messages table
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender_id INTEGER NOT NULL,
            receiver_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (sender_id) REFERENCES users (id),
            FOREIGN KEY (receiver_id) REFERENCES users (id)
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
<<<<<<< HEAD
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
=======
async def register(
    username: str = Form(...),
    password: str = Form(...),
    confirm_password: str = Form(...),
    id_number: str = Form(...),
    user_type: str = Form(...)
):
    # Validate passwords match
    if password != confirm_password:
        return RedirectResponse(
            url="/register?error=הסיסמאות אינן תואמות",
            status_code=303
        )
    
    # Validate ID number (basic validation - 9 digits)
    if not id_number.isdigit() or len(id_number) != 9:
        return RedirectResponse(
            url="/register?error=תעודת זהות חייבת להכיל 9 ספרות",
            status_code=303
        )
    
    # Validate user type
    if user_type not in ["soldier", "evacuee", "psychologist"]:
        return RedirectResponse(
            url="/register?error=סוג משתמש לא חוקי",
            status_code=303
        )
    
    # Try to create the user
    try:
        conn = sqlite3.connect('chat.db')
        c = conn.cursor()
        
        # Check if ID number already exists
        c.execute('SELECT id FROM users WHERE id_number=?', (id_number,))
        if c.fetchone():
            conn.close()
            return RedirectResponse(
                url="/register?error=תעודת זהות כבר קיימת במערכת",
                status_code=303
            )
            
        c.execute(
            'INSERT INTO users (username, password, id_number, user_type) VALUES (?, ?, ?, ?)',
            (username, password, id_number, user_type)
        )
        conn.commit()
        conn.close()
        return RedirectResponse(url=f"/login/{user_type}", status_code=303)
    except sqlite3.IntegrityError:
        return RedirectResponse(
            url="/register?error=שם המשתמש כבר קיים במערכת",
            status_code=303
        )
    except Exception as e:
        return RedirectResponse(
            url="/register?error=אירעה שגיאה בהרשמה",
            status_code=303
        )
>>>>>>> d2baf43536eed9c03f038796a65f3cecdddb4643

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

<<<<<<< HEAD
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
=======
@app.get("/options/{user_type}")
async def options(request: Request, user_type: str):
    if user_type not in ['soldier', 'evacuee', 'psychologist']:
        return RedirectResponse(url='/')
    
    template = "soldier_options.html" if user_type == 'soldier' else "evacuee_options.html" if user_type == 'evacuee' else "psychologist_options.html"
    
    return TEMPLATES.TemplateResponse(
        template,
        {
            "request": request,
            "today": datetime.now().strftime('%Y-%m-%d')
>>>>>>> d2baf43536eed9c03f038796a65f3cecdddb4643
        }
    )

@app.get("/chat-bot", response_class=HTMLResponse)
async def chat_bot(request: Request):
    return TEMPLATES.TemplateResponse("chat.html", {
        "request": request,
        "user_type": "bot"
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
async def save_message(
    sender_id: int = Form(...),
    receiver_id: int = Form(...),
    content: str = Form(...)
):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    try:
        c.execute(
            'INSERT INTO messages (sender_id, receiver_id, content) VALUES (?, ?, ?)',
            (sender_id, receiver_id, content)
        )
        conn.commit()
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
    finally:
        conn.close()

@app.get("/api/messages/{user_id}")
async def get_messages(user_id: int):
    conn = sqlite3.connect('chat.db')
    c = conn.cursor()
    try:
        c.execute('''
            SELECT m.*, u1.username as sender_name, u2.username as receiver_name
            FROM messages m
            JOIN users u1 ON m.sender_id = u1.id
            JOIN users u2 ON m.receiver_id = u2.id
            WHERE m.sender_id = ? OR m.receiver_id = ?
            ORDER BY m.timestamp DESC
        ''', (user_id, user_id))
        messages = c.fetchall()
        return {"messages": messages}
    finally:
        conn.close()

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