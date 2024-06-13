from backend import *
import os

path_areas = os.path.join(os.path.dirname(__file__), "data_set", "Перечень площадок с АСУ ОДС, ДКР коорд 07.06.24.xlsx")
path_catalog_maf = os.path.join(os.path.dirname(__file__), "data_set", "Каталог 2024 23.05.2024", "Каталог 2024.xlsx")


pg = Playground(path_areas, path_catalog_maf)

id_area = 944054570
cost = 78239
man = 'Поставщик 6'
id_maf = pg.get_area_cost(id_area, cost, man)
print(id_maf)