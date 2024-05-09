import sqlite3
import pandas as pd
from itertools import combinations
from collections import Counter
import numpy as np
import matplotlib.pyplot as plt

class combos:
    """
    A class to analyze and visualize combo data.

    Attributes:
        df (DataFrame): A pandas DataFrame containing the data from the 'checks' table.
        price_df (DataFrame): A pandas DataFrame containing the data from the 'price_list' table.

    Methods:
        __init__(): Initializes the combos class by connecting to the SQLite database and loading necessary data.
        has_multiple_components(string: str, n: int) -> bool: Checks if a string contains at least n components separated by '/'.
        calculate_combo_price(products: list, discount: float) -> float: Calculates the total price of a combo given its products and discount percentage.
        make_combos(k: int, discount: float) -> DataFrame: Generates possible combos based on product frequency and discount, and returns a DataFrame.
        visualize_most_frequent_combos(top_n: int): Visualizes the top most frequent combos in a bar chart.
        visualize_expensive_combos(top_n: int): Visualizes the top most expensive combos in a bar chart.
        visualize_cheap_combos(top_n: int): Visualizes the top cheapest combos in a bar chart.
    """

    def __init__(self) -> None:
        """
        Initializes the combos class by connecting to the SQLite database and loading necessary data.

        Args:
            None

        Returns:
            None
        """
        conn = sqlite3.connect('database.db')
        self.df = pd.read_sql_query("SELECT * FROM checks", conn)
        self.price_df = pd.read_sql_query("SELECT * FROM price_list", conn)
        conn.close()

    def has_multiple_components(self, string: str, n: int) -> bool:
        """
        Checks if a string contains at least n components separated by '/'.

        Args:
            string (str): The string to be checked.
            n (int): The minimum number of components required.

        Returns:
            bool: True if the string has at least n components, False otherwise.
        """
        return len(string.split('/')) >= n

    def calculate_combo_price(self, products: list, discount: float = 10) -> float:
        """
        Calculates the total price of a combo given its products and discount percentage.

        Args:
            products (list): A list of products in the combo.
            discount (float): The discount percentage to be applied (default is 10%).

        Returns:
            float: The total price of the combo after applying the discount.
        """
        combo_price = 0
        for product in products:
            price = self.price_df.loc[self.price_df['product_name'] == product, 'price'].values
            if len(price) > 0:
                combo_price += price[0]
        return combo_price * (1 - discount / 100)

    def make_combos(self, k: int = 10, discount: float = 10) -> pd.DataFrame:
        """
        Generates possible combos based on product frequency and discount, and returns a DataFrame.

        Args:
            k (int): Maximum number of combos to generate (default is 10).
            discount (float): The discount percentage to be applied (default is 10%).

        Returns:
            DataFrame: A DataFrame containing the generated combos and their frequencies.
        """
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

    def visualize_most_frequent_combos(self, top_n: int = 5):
        """
        Visualizes the top most frequent combos in a bar chart.

        Args:
            top_n (int): Number of top most frequent combos to visualize (default is 5).

        Returns:
            None
        """
        most_frequent_combos = self.df['products'].value_counts().nlargest(top_n)
        most_frequent_combos.plot(kind='bar', figsize=(10, 6), color='skyblue')
        plt.title('Top {} Most Frequent Combos'.format(top_n))
        plt.xlabel('Combo')
        plt.ylabel('Frequency')
        plt.xticks(rotation=45)
        plt.show()

    def visualize_expensive_combos(self, top_n: int = 5):
        """
        Visualizes the top most expensive combos in a bar chart.

        Args:
            top_n (int): Number of top most expensive combos to visualize (default is 5).

        Returns:
            None
        """
        combos_df = self.make_combos(discount=0)

        # Calculate prices for each combo
        combos_df['Combo_Price'] = combos_df['Products'].apply(lambda x: self.calculate_combo_price(x))

        # Sort by combo price
        sorted_combos = combos_df.nlargest(top_n, 'Combo_Price')

        # Plot the top expensive combos
        sorted_combos.plot(kind='bar', x='Products', y='Combo_Price', figsize=(10, 6), color='salmon')
        plt.title('Top {} Expensive Combos'.format(top_n))
        plt.xlabel('Combo')
        plt.ylabel('Price')
        plt.xticks(rotation=45)
        plt.show()

    def visualize_cheap_combos(self, top_n: int = 5):
        """
        Visualizes the top cheapest combos in a bar chart.

        Args:
            top_n (int): Number of top cheapest combos to visualize (default is 5).

        Returns:
            None
        """
        combos_df = self.make_combos(discount=0)

        # Calculate prices for each combo
        combos_df['Combo_Price'] = combos_df['Products'].apply(lambda x: self.calculate_combo_price(x))

        # Sort by combo price
        sorted_combos = combos_df.nsm
