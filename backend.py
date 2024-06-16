import pandas as pd
import xml.etree.ElementTree as ET
import os


class Playground:
    __private_square = 0

    def __init__(self, path_to_areas, path_to_catalog_maf):
        # self.df = pd.read_excel('Перечень площадок с АСУ ОДС, ДКР коорд 07.06.24.xlsx')
        # self.dfe = pd.read_excel('Каталог 2024.xlsx')

        self.df = pd.read_excel(path_to_areas)
        self.dfe = pd.read_excel(path_to_catalog_maf)


    def get_area(self, ID):
        square = self.df.loc[self.df['АСУ ОДС Идентификатор'] == ID, 'Площадь'].iloc[0]
        self.__private_square = square
        return square if not pd.isnull(square) else None
    
    def get_maf(self, manufacturer):
        filtered_df = self.dfe[self.dfe['Поставщик МАФ'] == manufacturer]
        result_df = filtered_df[['Габаритные размеры', 'Наименование производителя', 'Цена', '№ по номенклатуре' ]]

        maf_array = result_df.to_dict(orient='records')

        for i in range(len(maf_array)):
            size = maf_array[i]['Габаритные размеры'].split('x')
            if len(size) >=2:
                try:
                    width = float(size[0]) * 0.001
                    length = float(size[1]) * 0.001
                    maf_array[i]['Габаритные размеры'] = round(width * length, 5)
                except ValueError:
                    print(f"Ошибка при преобразовании размеров: {maf_array[i]['Габаритные размеры']}")  
        
        # maf_array.sort(key = lambda item: item['Габаритные размеры']) # doesnt work as well, need to check it deeper
        return maf_array

        
    def small_elements(self, maf_dict, target_area, target_cost):
        selected_mafs = {}
        current_area = 0
        current_cost = 0
        sample_dict ={}
        for i in range(len(maf_dict)):
            sample_dict [i]=maf_dict[i]
        for manufacturer, maf_data in sample_dict.items():
            maf_area = float(maf_data['Габаритные размеры'])
            maf_cost = float(maf_data['Цена'])
            if current_area + maf_area <= target_area:
                if current_cost + maf_cost <= target_cost:
                    selected_mafs[manufacturer] = maf_data
                    current_area += maf_area
                    current_cost += maf_cost
            else:
                break
        
        return selected_mafs    
    
    def get_area_cost(self, ID_area, target_cost, manufacturer : str):
        self.get_area(ID_area)
        maf_array = self.get_maf(manufacturer)
        selected_mafs = self.small_elements(maf_array, self.__private_square, target_cost)
        numbers = [item['№ по номенклатуре'] for item in selected_mafs.values()]
        return numbers
   
    def get_manufacturer(self):
        suppliers = self.dfe['Поставщик МАФ'].unique()
        result = {"list": suppliers.tolist()}
        return result
    
    def get_areas(self):
        address_id_pairs = []
        for index, row in self.df.iterrows():
            address_id_pairs.append({"ID": str(row['АСУ ОДС Идентификатор']), "Address": row['Адрес']})
        result = {"list": address_id_pairs}
        return result
    
    def upload_mafs(self):
        xmls_path = os.path.join(os.path.dirname(__file__), "data_set", "Каталог 2024 23.05.2024", "МАФ 2024")
    
        mafs = []

        if not os.path.exists(xmls_path):
            print(f"Directory does not exist: {xmls_path}")
            return {"error": "Directory does not exist"}

        for filename in os.listdir(xmls_path):
            if filename.endswith(".xml"):
                file_path = os.path.join(xmls_path, filename)
                try:
                    tree = ET.parse(file_path)
                    root = tree.getroot()

                    if root.tag == 'Catalog':
                        vendor_code = root.find('vendorCode')
                        price = root.find('price')
                        name = root.find('name')
                        provider = root.find('provider')
                        image = root.find('image')
                        dimensions = root.find('dimensions')

                        if vendor_code is not None and price is not None and name is not None and provider is not None and image is not None and dimensions is not None:
                            maf = {
                                "ID": vendor_code.text,
                                "Cost": float(price.text),
                                "Name": name.text,
                                "Provider": provider.text,
                                "ImagePath": image.text,
                                "Dimensions": dimensions.text
                            }
                            mafs.append(maf)
                            # print(f"Appended MAF: {maf}")
                        else:
                            print(f"Missing elements in {file_path}")

                    else:
                        print(f"Unexpected root tag in {file_path}: {root.tag}")

                except ET.ParseError as e:
                    print(f"Error parsing {file_path}: {e}")
                except Exception as e:
                    print(f"Unexpected error: {e}")
        
        return {"list" : mafs}



        




