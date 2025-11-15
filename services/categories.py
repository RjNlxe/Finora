import sqlite3
from datetime import datetime
import uuid

def get_db():
    return sqlite3.connect("") # Your database.db destination

def createCategory(user_id: str, name: str, description: str):
    cid = str(uuid.uuid4())
    n = datetime.now()
    t = n.strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            INSERT INTO categories (category_id, user_id, name, description, created_at)
            VALUES (?, ?, ?, ?, ?)
        """, (cid, user_id, name, description, t))
        conn.commit()
        conn.close()
        return {"Success": "Created"}

    except sqlite3.IntegrityError as e:
        return {"Error": f"Creation failed: {e}"}

    except Exception as e:
        return {"Error": str(e)}

def getCategories(user_id: str):
    conn = get_db()
    c = conn.cursor()
    c.execute(
        "SELECT category_id, user_id, name, description, created_at FROM categories WHERE user_id = ?",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()

    if not rows:
        return []

    categories = []
    for row in rows:
        category_id, user_id, name, description, created_at = row
        categories.append({
            "category_id": category_id,
            "user_id": user_id,
            "name": name,
            "description": description,
            "created_at": created_at
        })

    return categories
