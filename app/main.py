from fastapi import FastAPI
import model
from config import engine
from router import router
app = FastAPI()

model.Base.metadata.create_all(bind=engine)
app.include_router(router, prefix="/authentication",tags=["user"])
@app.get("/")
async def root():
    return {"message": "Hello World"}