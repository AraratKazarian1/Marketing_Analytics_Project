import uvicorn
import sqlite3
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from combogenius.api.config import HOST, USERNAME, PASSWORD, PORT, MailBody
from fastapi import FastAPI
from .config import MailBody
from .mailer import send_email
from .html_template import generate_html_template

app = FastAPI()

# SQLite database connection
conn = sqlite3.connect('database.db')
c = conn.cursor()

@app.get("/")
def index():
    return {"status": "fastapi mailserver is running"}

@app.post("/send_email/")
async def send_email(recipient:str, subject: str, discount: int, custom_html: str = None):
    # Database Connection
    conn = sqlite3.connect('database.db')
    c = conn.cursor()
    c.execute("SELECT email FROM companies")
    emails = c.fetchall()

    # Generate Combos
    combos = [
        {"name": "Deluxe Burger Combo", "code": "12345", "price": 10},
        {"name": "Family Pizza Combo", "code": "67890", "price": 20}
    ]

    # Generate HTML Template
    html_content = generate_html_template(combos, discount, custom_html)
    send_email(recipient, subject, html_content)

    return {"message": "Emails sent successfully"}

@app.get("/mark_interested/{email}")
async def mark_interested(email: str):
    try:
        # Update interested column in the database
        c.execute("UPDATE companies SET clicked = 1 WHERE email = ?", (email,))
        conn.commit()
        return {"message": f"Email {email} marked as interested"}
    except Exception as e:
        return {"error": str(e)}
    
def run_api():
    """Run API for sending emails."""
    uvicorn.run(app, host="127.0.0.1", port=5000,)
