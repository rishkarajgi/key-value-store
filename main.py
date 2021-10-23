from fastapi import FastAPI, Request
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


@app.post("/store")
async def add(request: JSONStructure = None):
    store.put(request)
    return {"received_data": request}

@app.get("/store/")
async def root(key):
    value = store.get(key)
    return {"key": key, "value": value}

@app.get("/store/all")
async def root():
    if len(store.cache) == 0:
        store.read_file_to_cache()
    return store.cache

@app.put("/store")
async def root(request: JSONStructure = None):
    store.update(request)
    return store

@app.delete("/store/")
async def root(key):
    store.delete(key)
    return store.cache