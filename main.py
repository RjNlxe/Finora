from typing import Optional
from fastapi import FastAPI, Request, HTTPException
from services.users import userRegister, userLogin, userInfo
from services.categories import createCategory, getCategories
from services.expanses import createExpense, getExpenses, deleteExpense, getUserStats
from services.jwthelper import verify_jwt
from functools import wraps
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=[""], # Add here your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def requires_auth(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        request: Optional[Request] = kwargs.get("request") or next((a for a in args if isinstance(a, Request)), None)
        if request is None:
            raise HTTPException(status_code=400, detail="Request object not found")

        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            raise HTTPException(status_code=401, detail="Missing or invalid token")

        token = auth_header.split(" ")[1]
        decoded = verify_jwt(token)
        if not decoded:
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        request.state.user = decoded  # attach user to request
        return await func(*args, **kwargs)

    return wrapper



@app.get("/")
def read_root():
    return {"Hello": "World!"}

@app.post("/api/user/register")
async def register(request: Request):
    data = await request.json()

    firstName = data["first_name"]
    lastName = data["last_name"]
    username = data["username"]
    email = data["email"]
    password = data["password"]
    
    result = userRegister(
        firstName=firstName,
        lastName=lastName,
        username=username,
        email=email,
        password=password
    )

    return result

@app.post("/api/user/login")
async def login(request: Request):
    data = await request.json()
    email = data["email"]
    password = data["password"]
    result = userLogin(
        email=email,
        password=password
    )
    return result

@app.get("/api/user")
@requires_auth
async def userinfo(request: Request):
    user = request.state.user  # get it from the decorator
    return userInfo(user["user_id"])

@app.post("/api/category/create")
@requires_auth
async def create(request: Request):
    data = await request.json()
    user = request.state.user
    userid = user["user_id"]
    name = data["name"]
    description = data["description"]
    result = createCategory(
        user_id=userid,
        name=name,
        description=description
    )
    return result

@app.get("/api/category/list")
@requires_auth
async def list(request: Request):
    user = request.state.user
    return getCategories(user["user_id"])

@app.post("/api/expense/create")
@requires_auth
async def createExp(request: Request):
    data = await request.json()
    user = request.state.user
    userid = user["user_id"]
    amount = data["amount"]
    category_id = data["category_id"]
    description = data["description"]
    date = data["date"]
    result = createExpense(
        user_id=userid,
        category=category_id,
        amount=amount,
        description=description,
        date=date
    )
    return result

@app.get("/api/expense/list")
@requires_auth
async def listExp(request: Request):
    user = request.state.user
    return getExpenses(user["user_id"])

@app.delete("/api/expense/delete/{expense_id}")
@requires_auth
async def deleteExp(request: Request, expense_id: str):
    user = request.state.user
    return deleteExpense(
        expense_id=expense_id,
        user_id=user["user_id"]
    )

@app.get("/api/user/stats")
@requires_auth
async def userStats(request: Request):
    user = request.state.user
    return getUserStats(user["user_id"])


