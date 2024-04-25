import uvicorn
import sqlite3
from fastapi import FastAPI, BackgroundTasks
from .config import MailBody
from .mailer import send_mail

app = FastAPI()

# SQLite database connection
conn = sqlite3.connect('database.db')
c = conn.cursor()

@app.get("/")
def index():
    return {"status": "fastapi mailserver is running"}

@app.post("/send-email")
def schedule_email(req: MailBody, tasks: BackgroundTasks):
    data = req.model_dump()
    tasks.add_task(send_mail, data)
    return {"status": 200, "message": "email has been scheduled"}


@app.get("/mark_interested/{email}")
async def mark_interested(email: str):
    try:
        # Update interested column in the database
        c.execute("UPDATE emails SET interested = 1 WHERE email = ?", (email,))
        conn.commit()
        return {"message": f"Email {email} marked as interested"}
    except Exception as e:
        return {"error": str(e)}
    
@app.put("/update_email/")
async def update_email(old_email: str, new_email: str):
    try:
        # Update email address in the database
        c.execute("UPDATE emails SET email = ? WHERE email = ?", (new_email, old_email,))
        conn.commit()
        return {"message": f"Email address updated from {old_email} to {new_email}"}
    except Exception as e:
        return {"error": str(e)}

def run_api():
    """Run API for sending emails.

    """
    uvicorn.run(app, host="127.0.0.1", port=5000,)
