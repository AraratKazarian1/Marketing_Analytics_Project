from group_five.database.schema import *
from group_five.database.sql_interactions import SqlHandler
from group_five.database.logger import CustomFormatter
from group_five.models.make_combos import combos
import pandas as pd

# Create the database and load the data
Inst=SqlHandler('database', 'checks')
Inst1=SqlHandler('database', 'companies')
Inst2=SqlHandler('database', 'price_list')

data=pd.read_csv('Data/data.csv')
companies = pd.read_csv('Data/companies.csv')
price_list = pd.read_csv('Data/price_list.csv')

Inst.insert_many(data)
Inst1.insert_many(companies)
Inst2.insert_many(price_list)

Inst.close_cnxn()

# Make new combos
m = combos()
f = m.make_combos(5)
print(f)
