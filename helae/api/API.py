from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import sqlite3
import uvicorn

app = FastAPI()
templates = Jinja2Templates(directory="templates")


# SQLite database connection
def get_db_connection():
    conn = sqlite3.connect('emails.db')
    conn.row_factory = sqlite3.Row
    return conn


# Endpoint to send emails
@app.post("/send_email/")
async def send_email(email: str = Form(...), message: str = Form(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO emails (email, message) VALUES (?, ?)", (email, message))
    conn.commit()
    conn.close()
    return {"message": "Email sent successfully"}


# Endpoint to mark link as clicked
@app.get("/mark_clicked/{email_id}")
async def mark_clicked(email_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("UPDATE emails SET clicked = 1 WHERE id = ?", (email_id,))
    conn.commit()
    conn.close()
    return {"message": "Link marked as clicked"}


# Endpoint to render HTML with list of emails
@app.get("/", response_class=HTMLResponse)
async def read_emails(request: Request):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM emails")
    emails = cursor.fetchall()
    conn.close()
    return templates.TemplateResponse("index.html", {"request": request, "emails": emails})

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)