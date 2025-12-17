from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, Dict
import json
from pathlib import Path

app = FastAPI(title="Items API", version="1.0.0")

path = Path('db/shopping_list.json')


class Item(BaseModel):
    name: str
    quantity: int


def load_database() -> Dict:
    try:
        with open(path, "r") as f:
            return json.load(f)
    except:
        with open(path, "w") as f:
            f.write('[]')
        return []


def save_database(data: Dict) -> None:
    with open(path, "w") as f:
        json.dump(data, f, indent=2)


@app.get("/items")
async def list_items():
    data = load_database()
    return data


@app.post("/items")
async def create_item(item: Item):
    data = load_database()
    id = len(data) + 1
    items = {'id': id, 'name': item.name, 'quantity': item.quantity}
    data.append(items)
    save_database(data)
    return f'data updated {data[-1]}'


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
