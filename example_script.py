from combogenius.database.schema import *
from combogenius.database.sql_interactions import SqlHandler
from combogenius.logger.logger import CustomFormatter
from combogenius.models.make_combos import combos
import pandas as pd

#  Create the database and load the data
Inst  = SqlHandler('database', 'checks')
Inst1 = SqlHandler('database', 'companies')
Inst2 = SqlHandler('database', 'price_list')

data=pd.read_csv('data/data.csv')
companies = pd.read_csv('data/companies.csv')
price_list = pd.read_csv('data/price_list.csv')

Inst.insert_many(data)
Inst1.insert_many(companies)
Inst2.insert_many(price_list)

Inst.close_cnxn()

#  Make new combos
m = combos()
f = m.make_combos(5)
print(f)

m.calculate_combo_price(f.iloc[0])

m.visualize_most_frequent_combos()
m.visualize_expensive_combos()
m.visualize_cheap_combos()