from fastapi import FastAPI, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse
from pathlib import Path
import sqlite3
import uvicorn
import webbrowser
import threading
import time

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
    
    # Drop existing table if exists
    c.execute('DROP TABLE IF EXISTS users')
    
    # Create new table with id_number
    c.execute('''
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            id_number TEXT UNIQUE NOT NULL,
            user_type TEXT NOT NULL
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
        return RedirectResponse(url=f"/chat/{user_type}", status_code=303)
    return RedirectResponse(url=f"/login/{user_type}?error=1", status_code=303)

@app.get("/chat/{user_type}", response_class=HTMLResponse)
async def chat(request: Request, user_type: str):
    return TEMPLATES.TemplateResponse("chat.html", {
        "request": request,
        "user_type": user_type
    })

def open_browser():
    time.sleep(1.5)  # Wait a bit for the server to start
    webbrowser.open('http://localhost:8000')

if __name__ == "__main__":
    # Start the browser in a new thread
    threading.Thread(target=open_browser, daemon=True).start()
    # Start the FastAPI application
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True) 