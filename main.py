from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api_routers import employee, department, auth

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return {"message": "FastAPI is working"}


app.include_router(employee.router)
app.include_router(department.router)
app.include_router(auth.router)
