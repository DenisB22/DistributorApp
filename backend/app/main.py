from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.roles import router as roles_router
from app.cron.cleanup_blacklist import start_cron

app = FastAPI(
    title="Distributor API",
    description="API for distributor app",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)

start_cron()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Backend!"}



