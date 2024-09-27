import json
import pandas as pd
from itertools import chain
import logging

class DataCleaner():
    """This class provides the functionality of fixing and cleaning the data from WebScraper.. 
    Returns data as a .csv file ready for upload."""

    def __init__(self):
        self.data = []
        self.logger = logging.getLogger(__name__)


    def fix_missing_data(self):
        with open("scraped_data.json", "r") as file:
            data = json.load(file)  
    
        for i in range(len(data)):
            
            initial_length = len(data[i])  
            
            if '' in data[i]:
                logging.info(f"Action: pop. {data[i].pop('')}") 

            for j in data[i]:
            
                if j == '':  
                    data[i][j] = ['---']                  # Add dummy values to create df structure
                    logging.info(f'Action: dummy value for data structure{[i, j]}')  

            logging.info(f'Id: {i},initial: {initial_length} Final: {len(data[i])}')
        with open("populated_data.json", "w") as fp:
            json.dump(data, fp)         

    def data_cleaning(self):

        with open("populated_data.json", "r") as file:
            data = json.load(file)

        typed_update = {'Driftkostnad': int,
                        'Antal rum': float ,
                        'Våning': float,
                        'id': int,
                        'Boarea': float,
                        'Antal besök': int,
                        'Avgift': int,
                        'Byggår': int,}

        drop_list = ['Premium',
                        'Plus',
                        'Bostadstyp',
                        'Planerat tillträde',
                        'Biarea']

        for j in range(len(data[0:])):
            for i in data[j]:
                a = str(data[j][i])
                b = ''
                
                logging.info(['starting point: ',i,'itt #: ', j, 'value: ', a, ])
                
                
                if i == 'id':
                    a = str(data[j][i])
                    a = a.replace("[","").replace("]","") 
                    data[j][i] = a  
                
                if i == 'Våning':
                    a = str(data[j][i])
                    
                    a = a.replace("['","").replace("']","").replace(",","").replace('---', '0').split()
                            
                    data[j][i] = str(a[0])
                
                else:
                    a = str(data[j][i])
                    a = a.replace("['","").replace("']","").replace(r'\xa0', '').replace('kr/mån','').replace('kr/år','').replace('kr/m²','').replace('kr','').replace('m²','').replace(' rum','')
                    data[j][i] = a  
                                
                if i == 'Boarea':
                    a = str(data[j][i])
                    a = a.replace(',', '.')
                    data[j][i] = a            
                
                if i == 'Balkong':
                    a = str(data[j][i])
                    a = a.replace('---','Nej')
                    data[j][i] = a             
                
                if i == 'Uteplats':
                    a = str(data[j][i])
                    a = a.replace('---','Nej')
                    data[j][i] = a             
                
                if i in typed_update.keys():
                    a = str(data[j][i])
                    a = a.replace('---', '0')
                    data[j][i] = a
                    
                logging.info(['checkpoint: ',i,'itt #: ', j, 'value: ', b, ])
                        
        df = pd.DataFrame.from_dict(data)

        existing_drop_list = [col for col in drop_list if col in df.columns]
        df.drop(existing_drop_list, inplace=True, axis=1)

        df.drop(df[df['Pris']== '---' ].index, inplace=True)

        try:
            df.to_csv('final_data_for_DB.csv', index=False)
        except Exception as e:
            print(f"Error writing to CSV: {e}")
        
        print('Fuck uou we made it !!!!!!!!!')
            
    def clean(self):
        self.fix_missing_data()
        self.data_cleaning()
        print("data saved as 'final_data_for_DB.csv'")            
