import sqlite3
from datetime import datetime
import uuid


def get_db():
    return sqlite3.connect("") # Your database.db destination

def createExpense(user_id: str, category: str, amount: str, description: str, date: str):
    eid = str(uuid.uuid4())
    n = datetime.now()
    t = n.strftime("%Y-%m-%d %H:%M:%S")
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("""
            INSERT INTO expenses (expense_id, category_id, user_id, amount, description, date, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (eid, category, user_id, amount, description, date, t))
        conn.commit()
        conn.close()
        return {"Success": "Created"}

    except sqlite3.IntegrityError as e:
        return {"Error": f"Creation failed: {e}"}

    except Exception as e:
        return {"Error": str(e)}

def getExpenses(user_id: str):
    conn = get_db()
    c = conn.cursor()
    c.execute("""
        SELECT expense_id, user_id, category_id, amount, date, description
        FROM expenses
        WHERE user_id = ?
    """, (user_id,))

    rows = c.fetchall()
    conn.close()

    if not rows:
        return []

    expenses = []
    for row in rows:
        expense_id, user, category_id, amount, date, description = row
        expenses.append({
            "expense_id": expense_id,
            "user_id": user,
            "category_id": category_id,
            "amount": amount,
            "date": date,
            "description": description
        })

    return expenses


def deleteExpense(expense_id: str, user_id: str):
    try:
        conn = get_db()
        c = conn.cursor()

        c.execute(
            "DELETE FROM expenses WHERE expense_id = ? AND user_id = ?",
            (expense_id, user_id)
        )

        conn.commit()
        conn.close()

        return {"Success": "Expense deleted"}
    except sqlite3.IntegrityError as e:
        return {"Error": f"Creation failed: {e}"}

    except Exception as e:
        return {"Error": str(e)}

def getUserStats(user_id: str):
    conn = get_db()
    c = conn.cursor()

    c.execute(
        "SELECT amount FROM expenses WHERE user_id = ?",
        (user_id,)
    )
    rows = c.fetchall()
    conn.close()

    if not rows:
        return {
            "total_expenses": 0,
            "transactions": 0,
            "avg_transaction": 0
        }

    amounts = [float(row[0]) for row in rows]
    total = sum(amounts)
    count = len(amounts)
    avg = total / count if count else 0

    return {
        "total_expenses": round(total, 2),
        "transactions": count,
        "avg_transaction": round(avg, 2)
    }
