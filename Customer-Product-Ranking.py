import pandas as pd
import matplotlib.pyplot as plt
import pickle

# Import Feature Engineered Sales Transaction file
sales_df = pd.read_csv('Sales-Transactions-Edited.csv')
# Items a Customer purchased the most
# Find the no of units sold of each product by customer
top_sell_cust_items_df = sales_df.groupby(['Party','Product']).agg({'Qty':'sum'})

# Reset the index by converting the Party and Product into a column
top_sell_cust_items_df.reset_index(inplace=True)


# Rank the product by most Qty sold, at Customer level
party_col = top_sell_cust_items_df['Party']
qty_col = top_sell_cust_items_df['Qty'].astype(str)
top_sell_cust_items_df['Top_Sell_Rank'] = (party_col + qty_col).rank(method='min',ascending=False).astype(int)


# List the top 20 items sold
#top_sell_cust_items_df.sort_values('Top_Sell_Rank',ascending=True).head(20)
# Items a Customer frequently purchased
# Considered Date column instead of Voucher, in counting the no of orders placed for a product.
# This ignores the multiple no of orders created in a single day.
# Here the understanding is that, this being a wholesale business,
#      a customer places a 2nd order of the same product in a day, only when he/she notices a wrong qty placed on the order.
# If the business considers to have Voucher column, instead of Date column, all the Date column below needs to be replaced.


# Remove duplicate records at Party, Product and Date level
unique_order_items_df = sales_df.drop_duplicates(['Party','Product','Date'])


# Find the no of orders placed and the unique no of customers placed orders, of each product
freq_items_df = unique_order_items_df.groupby(['Party','Product']).agg({'Date':'count'})
freq_items_df.columns=['No_of_Orders']

# Reset the index by converting the Party and Product into columns
freq_items_df.reset_index(inplace=True)


# Products with high no of orders are considered as most frequently purchased items

# Rank the product by No of Orders, at Customer Level
party_col = freq_items_df['Party']
ord_count_col = freq_items_df['No_of_Orders'].astype(str)
freq_items_df['Popularity_Rank'] = (party_col + ord_count_col).rank(method='min',ascending=False).astype(int)


# List of top 20 most popular items sold
#freq_items_df.sort_values('Popularity_Rank',ascending=True).head(20)
# Merge all the Ranks
# Merge Top Selling Items Rank and Popularity Rank dataframes
cust_prod_rankings_df = pd.merge(top_sell_cust_items_df,freq_items_df,how='inner',on=['Party','Product'])


# Merge the Unit Price (max price at product level)

# Find the unit price of each product (max of price considered, may required to be changed to median or mean)
items_price_df = sales_df.groupby(['Product']).agg({'Rate':'max'})

# Reset the index by converting the Party and Product into columns
items_price_df.reset_index(inplace=True)

# This ensures the same unit price is attached to the product purchased by different customers
cust_prod_rankings_df = pd.merge(cust_prod_rankings_df,items_price_df,how='left',on='Product')


# Get only the Customer, Product, Price and Rank columns
cust_prod_rankings_df = cust_prod_rankings_df[['Party','Product','Rate','Qty','Top_Sell_Rank','No_of_Orders','Popularity_Rank']]


# List the Product Rankings
#cust_prod_rankings_df.sort_values('Popularity_Rank',ascending=True).head(20)
# Write the Customer Product Rankings into a .csv file
cust_prod_rankings_df.to_csv('Customer-Product-Rankings.csv',index=False)
# Create a Pickle (.pkl) file with the Ranking dataframe¶
pickle.dump(cust_prod_rankings_df, open('cust_prod_ranking_model.pkl','wb'))
