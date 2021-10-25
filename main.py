from fastapi import FastAPI, Request, HTTPException
from core.cache import KVStore
from pydantic import BaseModel
from typing import Optional, Dict, Any, AnyStr, List, Union

app = FastAPI()

store = KVStore()


class Key(BaseModel):
    key: str

class Item(BaseModel):
    key: str
    value: Dict

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]



@app.get("/health-check")
async def get():
    return {
            "msg": "Hello World"
        }

@app.post("/store")
async def add(request: JSONStructure = None):
    store.put(request)
    return store

@app.get("/store")
async def get(key):
    value = store.get(key)
    if value == -1:
        raise HTTPException(status_code=404, detail="No data found!")
    return {"key": key, "value": value}

@app.get("/store/all")
async def get_all():
    if len(store.cache) == 0:
        store.read_file_to_cache()
    return store.cache

@app.put("/store")
async def update(request: JSONStructure = None):
    store.update(request)
    return store

@app.delete("/store")
async def delete(key):
    store.delete(key)
    return store.cache

@app.delete("/store/flush")
async def flush():
    store.flush_file()
    return {
            "message": "Cache cleared", 
            "cache": store.cache
        }