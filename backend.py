import pandas as pd

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
        
        maf_array.sort(key = lambda item: item['Габаритные размеры'])
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
    
    def get_area_cost(self, ID_area, target_cost, manufacturer):
        self.get_area(ID_area)
        maf_array = self.get_maf(manufacturer)
        selected_mafs = self.small_elements(maf_array, self.__private_square, target_cost)
        numbers = [item['№ по номенклатуре'] for item in selected_mafs.values()]
        return numbers

        




