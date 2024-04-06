
from helae.database.data_preperation import SqlHandler
from helae.database.logger import CustomFormatter
import pandas as pd


Inst=SqlHandler('database', 'checks')
Inst1=SqlHandler('database', 'companies')

data=pd.read_csv('data.csv')
companies = pd.read_csv('companies.csv')

Inst.insert_many(data)
Inst1.insert_many(companies)

Inst.close_cnxn()
