import sqlite3
import pandas as pd
from itertools import combinations
from collections import Counter
import numpy as np

#def make_combos(num_new_combos: int):
conn = sqlite3.connect('database.db')
df = pd.read_sql_query("SELECT * FROM checks", conn)
conn.close()



unique_products = set(df['products'])
product_frequencies = Counter(unique_products)
frequencies = list(product_frequencies.values())
unique_products = df['products'].unique()
product_frequencies = Counter(df['products'])
frequencies = [product_frequencies[product] for product in unique_products]
frequency_table = pd.DataFrame({'Products': unique_products, 'Frequecny': frequencies})
sorted_frequency_table = frequency_table.sort_values(by='Frequency', ascending=False)

def has_multiple_components(string, n):
    return len(string.split('/')) >= n

def top_at_most_k_combos(k, sorted_frequency_table):
    best_i, best_j = None, None
    min_len = float('inf')  # Initialize min_len with infinity
    
    for i in range(3, 5):
        for j in range(2, int(np.sqrt(len(sorted_frequency_table)))):
            # Convert 'Order' column to strings
            sorted_frequency_table['Order'] = sorted_frequency_table['Order'].astype(str)
            
            mask = sorted_frequency_table['Order'].apply(lambda x: has_multiple_components(x, i))
            # Filter the DataFrame using the mask
            filtered_table = sorted_frequency_table[mask].copy()  # Create a copy to avoid modifying the original DataFrame
            
            filtered_table.drop(filtered_table[filtered_table['Frequency'] < j].index, inplace=True)
            
            length = len(filtered_table)
            if length <= k:
                return filtered_table  # Return immediately if the condition is met
            
            if length < min_len:  # Update the best_i and best_j if we found a better solution
                best_i, best_j = i, j
                min_len = length
    
    # After the loops, if no solution is found, return the filtered table with the best_i and best_j values
    mask = sorted_frequency_table['Order'].apply(lambda x: has_multiple_components(x, best_i))
    filtered_table = sorted_frequency_table[mask].copy()
    filtered_table.drop(filtered_table[filtered_table['Frequency'] < best_j].index, inplace=True)
    
    return filtered_table