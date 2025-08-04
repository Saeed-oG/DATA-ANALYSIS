#DATA ANALYSIS

#STEP1-------------------Geting ready:
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
data1 = pd.read_csv(r'D:\PROGRAMING\DATA ANALYSIS\supermarket_sales - Sheet1.csv')
print(data1)
# print(data1.columns)
# print(data1.isnull().sum())
data1 = data1.dropna() # remove feilds whith not value
data1['Total'].fillna(data1['Total'].mean() , inplace=True) # replace empty fields whit average of other values
data1['Gender'].fillna(data1['Gender'].mode()[0] , inplace=True) # replace empty fields whit mode of other values
print(data1.dtypes) # Data types analysis
data1['Date'] = pd.to_datetime(data1['Date']) # Convert Data column format to datetime type
data1['Time'] = pd.to_datetime(data1['Time'], format='%H:%M').dt.time
print(data1.dtypes) # Data types analysis

data1 = data1.drop(['Invoice ID','Branch'] , axis=1) #remove unnecessary columns
data1 = data1.drop_duplicates() # remove duplicate rows
print(data1.head()) # show the top rows

# plt.figure(1 , figsize=(8, 6))  # set chart size
# sns.boxplot(y=data1['Total'], color='lightblue') # draw chart and set chart color
# plt.title('Boxplot of Total Sales', fontsize=14)  # title
# plt.ylabel('Total Sales (USD)', fontsize=12)  # y lable
# plt.grid(True)  # add net to chart
# plt.savefig('total_sales_boxplot.png', dpi=300)  # save chart picture

#STEP2--------------------remove outliers whith IQR:
Q1 = data1['Total'].quantile(0.25)
Q3 = data1['Total'].quantile(0.75)
IQR = Q3 - Q1
lower_boand = Q1 - 1.5 * IQR
upper_bound = Q3 + 1.5 * IQR
data1 = data1[(data1['Total'] >= lower_boand) & (data1['Total'] <= upper_bound)]

# plt.figure(2 , figsize=(8, 6))  # set chart size
# sns.boxplot(y=data1['Total'], color='lightblue') # draw chart and set chart color
# plt.title('Boxplot of Total Sales', fontsize=14)  # title
# plt.ylabel('Total Sales (USD)', fontsize=12)  # y lable
# plt.grid(True)  # add net to chart
# plt.savefig('total_sales_boxplot.png', dpi=300)  # save chart picture
data1.to_excel('cleaned_data.xlsx')

#STEP3---------------------EXPLORATORY DATA ANALYSIS
city_sales = data1.groupby('City')['Total'].sum()
print("Total sales by city:\n" , city_sales)
customer_sales = data1.groupby('Customer type')['Total'].mean()
print("\nAverage sales by customer type:\n" , customer_sales)
product_sales = data1.groupby('Product line')['Total'].sum().sort_values(ascending=False)
print("\nTotal sales by product line:\n" , product_sales)

data1['Month'] = data1['Date'].dt.month
monthly_sales = data1.groupby('Month')['Total'].sum()
print("\nMonthly ssales:\n" , monthly_sales)

data1['Day of week'] = data1['Date'].dt.day_name()
daily_sales = data1.groupby('Day of week')['Total'].sum()
print("\nDaily sales:\n" , daily_sales)

gender_product = data1.groupby(['Gender' , 'Product line'])['Total'].sum()
print("\nSeles by gender and product line:\n" , gender_product)

payment_customer = data1.groupby(['Payment' , 'Customer type'])['Total'].count()
print("\nSNumber of transactions by payment and customer type:\n" , payment_customer)

#STEP4-----------------------DATA VISUALIZATION:
plt.figure(3 , figsize=(8, 6))
sns.barplot(x=city_sales.index, y=city_sales.values, hue=city_sales.index, palette='Blues', legend=False)
plt.title('Total Sales by City', fontsize=14)
plt.xlabel('City', fontsize=12)
plt.ylabel('Total Sales (USD)', fontsize=12)
plt.grid(True)
plt.savefig('city_sales.png', dpi=300)

plt.figure(4 , figsize=(8, 6))
monthly_sales.plot(kind='line', marker='o', color='blue')
plt.title('Monthly Sales Trend', fontsize=14)
plt.xlabel('Month', fontsize=12)
plt.ylabel('Total Sales (USD)', fontsize=12)
plt.grid(True)
plt.savefig('monthly_sales.png', dpi=300)

plt.figure(5 , figsize=(8, 6))
sns.scatterplot(x='Quantity', y='Total', hue='Customer type', size='Customer type', data=data1, palette='deep')
plt.title('Quantity vs Total Sales by Customer Type', fontsize=14)
plt.xlabel('Quantity', fontsize=12)
plt.ylabel('Total Sales (USD)', fontsize=12)
plt.grid(True)
plt.savefig('quantity_total.png', dpi=300)

plt.figure(6 , figsize=(8, 8))
plt.pie(product_sales, labels=product_sales.index, autopct='%1.1f%%', colors=sns.color_palette('Blues', len(product_sales)))
plt.title('Sales Distribution by Product Line', fontsize=14)
plt.savefig('product_sales_pie.png', dpi=300)
plt.show()