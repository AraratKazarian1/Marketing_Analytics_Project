from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
import sqlite3
import uuid

app = FastAPI()

# Create a connection to SQLite database
conn = sqlite3.connect('poster.db')
cursor = conn.cursor()

# Create a table to store emails and their interested status
cursor.execute('''CREATE TABLE IF NOT EXISTS emails (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE,
                    interested INTEGER DEFAULT 0
                )''')
conn.commit()


# Define Pydantic model for email
class Email(BaseModel):
    email: str


# API endpoint to send posters to a list of emails
@app.post("/send_posters/")
async def send_posters(emails: list[Email]):
    try:
        for email_obj in emails:
            email = email_obj.email
            cursor.execute('INSERT INTO emails (email) VALUES (?)', (email,))
            conn.commit()
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Email already exists")


# API endpoint to mark email as interested
@app.put("/mark_interested/")
async def mark_interested(email: str = Query(..., min_length=1)):
    cursor.execute('UPDATE emails SET interested = 1 WHERE email = ?', (email,))
    conn.commit()
    return {"message": "Email marked as interested"}


# API endpoint to get all emails and their interested status
@app.get("/emails/")
async def get_emails():
    cursor.execute('SELECT email, interested FROM emails')
    emails = cursor.fetchall()
    emails_data = [{"email": email, "interested": interested} for email, interested in emails]
    return emails_data


# API endpoint to handle when user clicks "interested" in the email
@app.get("/interested/")
async def mark_interested_from_email(email_id: str):
    cursor.execute('UPDATE emails SET interested = 1 WHERE id = ?', (email_id,))
    conn.commit()
    return {"message": "Email marked as interested"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
