import sqlite3
import pandas as pd
from itertools import combinations
from collections import Counter
import numpy as np 
import matplotlib.pyplot as plt

class combos:
    def __init__(self):
        conn = sqlite3.connect('database.db')
        self.df = pd.read_sql_query("SELECT * FROM checks", conn)
        self.price_df = pd.read_sql_query("SELECT * FROM price_list", conn)
        conn.close()

    def has_multiple_components(self, string, n):
        return len(string.split('/')) >= n

    def calculate_combo_price(self, products, discount=10):
        combo_price = 0
        for product in products:
            price = self.price_df.loc[self.price_df['product_name'] == product, 'price'].values
            if len(price) > 0:
                combo_price += price[0]
        return combo_price * (1 - discount / 100)

    def make_combos(self, k=10, discount=10):
        unique_products = set(self.df['products'])
        product_frequencies = Counter(unique_products)
        frequencies = list(product_frequencies.values())
        unique_products = self.df['products'].unique()
        product_frequencies = Counter(self.df['products'])
        frequencies = [product_frequencies[product] for product in unique_products]
        frequency_table = pd.DataFrame({'Products': unique_products, 'Frequency': frequencies})
        sorted_frequency_table = frequency_table.sort_values(by='Frequency', ascending=False)

        best_i, best_j = None, None
        min_len = float('inf')  
        
        for i in range(3, 5):
            for j in range(2, int(np.sqrt(len(sorted_frequency_table)))):
                sorted_frequency_table['Products'] = sorted_frequency_table['Products'].astype(str)
                
                mask = sorted_frequency_table['Products'].apply(lambda x: self.has_multiple_components(x, i))
                filtered_table = sorted_frequency_table[mask].copy()  
                
                filtered_table.drop(filtered_table[filtered_table['Frequency'] < j].index, inplace=True)
                
                length = len(filtered_table) 
                if length <= k:
                    return filtered_table  
                
                if length < min_len:  
                    best_i, best_j = i, j
                    min_len = length
        
        mask = sorted_frequency_table['Products'].apply(lambda x: self.has_multiple_components(x, best_i))
        filtered_table = sorted_frequency_table[mask].copy()
        filtered_table.drop(filtered_table[filtered_table['Frequency'] < best_j].index, inplace=True)

        filtered_table['Combo_Price'] = filtered_table['Products'].apply(lambda x: self.calculate_combo_price(x.split('/'), discount))
        
        return filtered_table
    
    def visualize_most_frequent_combos(self, top_n=5):
        most_frequent_combos = self.df['products'].value_counts().nlargest(top_n)
        most_frequent_combos.plot(kind='bar', figsize=(10, 6), color='skyblue')
        plt.title('Top {} Most Frequent Combos'.format(top_n))
        plt.xlabel('Combo')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.show()

    def visualize_expensive_combos(self, top_n=5):
        sorted_table = self.make_combos(discount=0)
        top_expensive_combos = sorted_table.nlargest(top_n, 'Combo_Price')
        top_expensive_combos.plot(kind='bar', x='Products', y='Combo_Price', figsize=(10, 6), color='salmon')
        plt.title('Top {} Expensive Combos'.format(top_n))
        plt.xlabel('Combo')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.show()

    def visualize_cheap_combos(self, top_n=5):
        sorted_table = self.make_combos(discount=0)
        top_cheap_combos = sorted_table.nsmallest(top_n, 'Combo_Price')
        top_cheap_combos.plot(kind='bar', x='Products', y='Combo_Price', figsize=(10, 6), color='lightgreen')
        plt.title('Top {} Cheap Combos'.format(top_n))
        plt.xlabel('Combo')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.show()

#combos_instance = combos()
#combos_instance.make_combos()
#combos_instance.visualize_most_frequent_combos()