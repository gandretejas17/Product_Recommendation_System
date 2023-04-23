import pandas as pd
import matplotlib.pyplot as plt
import pickle

# Import Feature Engineered Sales Transaction file
sales_df = pd.read_csv('Sales-Transactions-Edited.csv')
# Top Selling Items
# Find the no of units sold of each product
# Find the unit price of each product (max of price considered, may required to be changed to median or mean)
top_sell_items_df = sales_df.groupby('Product').agg({'Qty':'sum', 'Rate':'max'})

# Reset the index by converting the Product into a column
top_sell_items_df.reset_index(inplace=True)


# Rank the product by most Qty sold
top_sell_items_df['Top_Sell_Rank'] = top_sell_items_df['Qty'].rank(method='min',ascending=False).astype(int)


# List the top 20 items sold
#top_sell_items_df.sort_values('Qty',ascending=False).head(20)
# Most Popular Items
# Considered Date column instead of Voucher, in counting the no of orders placed for a product.
# This ignores the multiple no of orders created in a single day.
# Here the understanding is that, this being a wholesale business,
#      a customer places a 2nd order of the same product in a day, only when he/she notices a wrong qty placed on the order.
# If the business considers to have Voucher column, instead of Date column, all the Date column below needs to be replaced.


# Remove duplicate records at Product, Date and Party level
unique_order_items_df = sales_df.drop_duplicates(['Product','Date','Party'])


# Find the no of orders placed and the unique no of customers placed orders, of each product
most_popular_items_df = unique_order_items_df.groupby('Product').agg({'Date':'count', 'Party':'nunique'})
most_popular_items_df.columns=['No_of_Orders','No_of_Customers']

# Reset the index by converting the Product into a column
most_popular_items_df.reset_index(inplace=True)


# Products with high no of orders can be considered as most frequently purchased items
# To find the most popular items, include the no of customers purchased and provide more weightage to products purchased by more customers

# Weighted No_of_Orders (W) = O * (C / M)
# O = No_of_Orders
# C = No_of_Customers purchased the product
# M = Maximum no of customers made transactions in the entire period

O = most_popular_items_df['No_of_Orders']
C = most_popular_items_df['No_of_Customers']
M = most_popular_items_df['No_of_Customers'].max()

most_popular_items_df['Weighted_No_of_Orders'] = O * (C / M)

# Rank the product by weighted no of orders
most_popular_items_df['Popularity_Rank'] = most_popular_items_df['Weighted_No_of_Orders'].rank(method='min',ascending=False).astype(int)


# List of top 20 most popular items sold
#most_popular_items_df.sort_values('Popularity_Rank',ascending=True).head(20)
# Merge all the Ranks
# Merge Top Selling Items Rank and Popularity Rank dataframes
product_rankings_df = pd.merge(top_sell_items_df,most_popular_items_df,how='inner',on='Product')

# Get only the Product, Price and Rank columns
product_rankings_df = product_rankings_df[['Product','Rate','Top_Sell_Rank','Popularity_Rank']]

# List the Product Rankings
#product_rankings_df.sort_values('Popularity_Rank',ascending=True).head(20)
# Write the Product Rankings into a .csv file
product_rankings_df.to_csv('Product-Rankings.csv',index=False)
# Create a Pickle (.pkl) file with the Ranking dataframe
pickle.dump(product_rankings_df, open('prod_ranking_model.pkl','wb'))
