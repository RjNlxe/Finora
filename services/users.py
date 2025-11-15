import sqlite3
import bcrypt
from datetime import datetime
import uuid
from .jwthelper import create_jwt

def get_db():
    return sqlite3.connect("") # Your database.db destination

def userRegister(firstName: str, lastName: str, username: str, email: str, password: str):
    id = str(uuid.uuid4())
    n = datetime.now()
    t = n.strftime("%Y-%m-%d %H:%M:%S")
    pwb = password.encode('utf-8')
    p = bcrypt.hashpw(pwb, bcrypt.gensalt())

    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            INSERT INTO users (user_id, firstName, lastName, username, email, password, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (id, firstName, lastName, username, email, p, t))

        conn.commit()
        conn.close()
        return {"Success": "Registered"}

    except sqlite3.IntegrityError as e:
        return {"Error": f"Registration failed: {e}"}

    except Exception as e:
        return {"Error": str(e)}
def userLogin(email: str, password: str):
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("SELECT user_id, password FROM users WHERE email = ?", (email,))
        user = c.fetchone()
        conn.close()
        if not user:
            return {"Error": "User Not Found"}
        user_id, hashed_pw = user
        if bcrypt.checkpw(password.encode('utf-8'), hashed_pw):
            token = create_jwt(user_id)
            return {"token": token}
        else:
            return {"Error": "Invalid password"}
    except Exception as e:
        return {"Error": str(e)}

def userInfo(user_id: str):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT user_id, firstName, lastName, username, email FROM users WHERE user_id = ?",
        (user_id,)
    )
    result = c.fetchone()
    conn.close()

    if not result:
        return {"Error": "User not found"}

    user_id, firstName, lastName, username, email = result
    return {
        "user_id": user_id,
        "first_name": firstName,
        "last_name": lastName,
        "username": username,
        "email": email
    }
