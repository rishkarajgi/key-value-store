from fastapi import FastAPI, Request, HTTPException
from core.cache import KVStore
from pydantic import BaseModel
from typing import Optional, Dict, Any, AnyStr, List, Union


app = FastAPI()

# Initialize in-memory store object
store = KVStore()

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


@app.get("/health-check")
async def get():
    return {
            "message": "Hello World!"
        }

@app.post("/store")
async def add(request: JSONStructure = None):
    store.put(request)
    return store

@app.get("/store")
async def get(key):
    code, message = store.get(key)
    if code == 404:
        raise HTTPException(status_code=404, detail="Key not found!")
    return { key: message }

@app.get("/store/all")
async def get_all():
    store.read_file_to_cache()
    return store.cache

@app.put("/store")
async def update(request: JSONStructure = None):
    code, message = store.update(request)
    if (code == 404):
        raise HTTPException(status_code=404, detail="Key not found! Please add, then update")
    return store

@app.delete("/store")
async def delete(key):
    code, message = store.delete(key)
    if code == 404:
        raise HTTPException(status_code=404, detail="Key not found!")
    return {"message": message}

@app.delete("/store/flush")
async def flush():
    store.flush_file()
    return {
            "message": "Cache cleared", 
            "cache": store.cache
        }