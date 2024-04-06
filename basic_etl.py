from helae.database.data_preperation import SqlHandler
from helae.database.logger import CustomFormatter
import pandas as pd


Inst=SqlHandler('database', 'checks')
Inst1=SqlHandler('database', 'companies')
Inst2=SqlHandler('database', 'price_list')

data=pd.read_csv('data.csv')
companies = pd.read_csv('companies.csv')
price_list = pd.read_csv('price_list.csv')

Inst.insert_many(data)
Inst1.insert_many(companies)
Inst2.insert_many(price_list)

Inst.close_cnxn()
