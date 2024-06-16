
import os

from fastapi import FastAPI, Request, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import xml.etree.ElementTree as ET



path_areas = os.path.join(os.path.dirname(__file__), "data_set", "Перечень площадок с АСУ ОДС, ДКР коорд 07.06.24.xlsx")
path_catalog_maf = os.path.join(os.path.dirname(__file__), "data_set", "Каталог 2024 23.05.2024", "Каталог 2024.xlsx")
from backend import *
pg = Playground(path_areas, path_catalog_maf)



app = FastAPI()

origins = [
    "*",
    # "http://localhost:8080",
    # "http://127.0.0.1:8080"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



class MAF(BaseModel):
    ID: str
    Cost: float
    Name: str
    Provider: str
    ImagePath: str



@app.get("/")
async def read_root():
    return {"Hello": "World"}


#region Test
@app.get("/test/with_values")
async def update_item(item_id: int, another_item: int):
    print({"item_id": item_id, "another_item" : another_item})
    return {"item_id": item_id, "another_item" : another_item}

@app.get("/test/image")
async def responce_image():
    image_path = os.path.join(os.path.dirname(__file__), "data_set", "Каталог 2024 23.05.2024", "картинки 2024", "0aabbaaa-1741-40ab-b4a5-a4e4a546e1b8.png")
    return FileResponse(image_path)
#endregion


@app.get("/upload_mafs")
async def upload_mafs():
    result = pg.upload_mafs()
    return result
  
@app.get("/get_maf_image")
async def get_maf_image(img_name : str):
    img_path = os.path.join(os.path.dirname(__file__), "data_set", "Каталог 2024 23.05.2024", "картинки 2024", img_name)
    return FileResponse(img_path)

@app.get("/get_areas")
async def get_areas():
    """
    Надо вернуть список всех площадок с в формате
    return {"list" : [{"ID0" : address0}, {"ID1" : address1},..]} 
    """
    result = pg.get_areas()
    return result

@app.get("/get_manufacturer")
async def get_manufacturer():
    """
    Надо вернуть список всех производителей в формате
    return {"list" : [manufacturer0, manufacturer1,..]} 
    """
    result = pg.get_manufacturer()
    return result

@app.get("/generate_maf_for_id_cost_manuf")
async def generate_maf_for_id_cost_manuf(cost : float, manufacturer : str, id_area : int):
    """
    Надо вернуть список ID-шников МАФов
    """

    id_maf = pg.get_area_cost(id_area, cost, manufacturer)
    return {"list" : id_maf}






if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

