from typing import Optional

from fastapi import FastAPI
from pydantic import BaseModel
from core import KVCache


class DataModel(BaseModel):
    key: str
    value: dict

app = FastAPI()

JSONObject = Dict[AnyStr, Any]
JSONArray = List[Any]
JSONStructure = Union[JSONArray, JSONObject]


@app.post("/")
async def put(data: [DataModel]):
    return data

@app.get(
    "/", response_description="List all data", response_model=List[DataModel]
)
async def list_data():
    data = await db["data"].find().to_list(1000)
    return data