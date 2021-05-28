from fastapi import FastAPI
from typing import Optional
from pydantic import BaseModel

from security import auth

class Item(BaseModel):
	name: str
	description: Optional[str] = None
	price: float
	tax: Optional[float] = None


app = FastAPI()
app.include_router(auth.router)

@app.get("/")
async def root():
	return {"message": "hello world"}


@app.get("/{number}")
async def number(number: int):
	return {"number" : number}

@app.post("/items/")
async def create_item(item: Item):
	return item