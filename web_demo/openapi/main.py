from typing import Union

from fastapi import FastAPI

app = FastAPI()


@app.get("http://127.0.0.1:5500/web_demo/main_page.html")
def read_root():
    return {"Hello": "World"}


@app.get("http://127.0.0.1:5500/web_demo/main_page.html/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}