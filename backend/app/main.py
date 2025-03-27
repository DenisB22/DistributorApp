from fastapi import FastAPI
from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.roles import router as roles_router
from app.routes.microinvest.products import router as microinvest_products_router
from app.routes.microinvest.partners import router as microinvest_partners_router
from app.routes.microinvest.users import router as microinvest_users_router
from app.routes.microinvest.operations import router as microinvest_operations_router
from app.cron.cleanup_blacklist import start_cron

app = FastAPI(
    title="Distributor API",
    description="API for distributor app",
    version="1.0.0"
)


app.include_router(auth_router)
app.include_router(users_router)
app.include_router(roles_router)
app.include_router(microinvest_products_router)
app.include_router(microinvest_partners_router)
app.include_router(microinvest_users_router)
app.include_router(microinvest_operations_router)

start_cron()

@app.get("/")
def home():
    return {"message": "Welcome to FastAPI Backend!"}



