import pandas as pd
import logging
from sqlalchemy import create_engine

class DataSaver():
    
    def __init__(self):
        self.logger = logging.getLogger(__name__)
    
    def connect_to_sql(self):
        engine = create_engine('mssql://CHRIS_SKOLDATOR/hemnet?trusted_connection=yes&driver=ODBC+Driver+17+for+SQL+Server')
        return engine
    def csv_to_df_to_sql(self, engine):
        data_df = pd.read_csv('final_data_for_DB.csv')
        data_df.to_sql('hemnet', con=engine, if_exists='append')

    def validate_upload(self, engine):
        data = pd.read_sql_query('SELECT * FROM hemnet', engine)
        print(data)
    
    def save_data(self):
        engine = self.connect_to_sql()
        self.csv_to_df_to_sql(engine)
        self.validate_upload(engine)
        