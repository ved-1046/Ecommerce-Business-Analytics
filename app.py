import folium
from folium.plugins import HeatMap
from streamlit_folium import st_folium
import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt

st.set_page_config(
    page_title='Ecommerce Sales Analytics',
    layout = 'wide'
)


st.title('E-Commerce Sales Analytics Dashboard')
st.markdown('### Business Intelligence Portal')

engine = create_engine("mysql+pymysql://root:vedika123%40321@localhost:3306/ecommerce_analysis")
#===========================================================================

customers_df = pd.read_sql("""
SELECT customer_id,
       customer_zip_code_prefix
FROM customers;
""", engine)


payments_df = pd.read_sql("""
SELECT order_id,
       payment_value
FROM payments;
""", engine)

orders_df = pd.read_sql("""
SELECT order_id,
       customer_id
FROM orders;
""", engine)

geolocation_df = pd.read_sql("""
SELECT geolocation_zip_code_prefix,
       geolocation_lat,
       geolocation_lng
FROM geolocation;
""", engine)

orders_customers_df = pd.merge(
    orders_df,customers_df,
    on='customer_id',
    how='inner'
)

orders_customers_payments_df = pd.merge(
    orders_customers_df,payments_df,
    on='order_id',
    how='inner'
)

geo_revenue_df = pd.merge(
    orders_customers_payments_df,
    geolocation_df,
    left_on = 'customer_zip_code_prefix',
    right_on='geolocation_zip_code_prefix',
    how='inner'
)
#===========================================================================
heatmap_data = geo_revenue_df[['geolocation_lat',
                               'geolocation_lng',
                               'payment_value']].sample(5000)

heatmap_data = heatmap_data.values.tolist()

#creating the map
m = folium.Map(
    location=[-15.79 , -47.88],
    zoom_start=4
) #these valuyes because these are approximately at center of brazil

#Adding heatmap
HeatMap(heatmap_data,
        radius=8,
        blur=12,
        max_zoom=10).add_to(m)

#we get all the states from the data
query = """
select distinct customer_state
from customers
order by customer_state
"""

states = pd.read_sql(query ,engine)

state_list = ['All'] + states['customer_state'].tolist() #toist converts pandas series into python list

st.sidebar.title('Filters')
selected_State = st.sidebar.selectbox(
    'Select State',
    state_list
)

if selected_State == 'All':
    query = """
    select count(*) as total_customers
    from customers;
    """
else:
    query = f"""
    select count(*) as total_custoemrs
    from customers
    where customer_state = '{selected_State}';
    """


st.write('Selected State: ' , selected_State)

col1 , col2 , col3 , col4 = st.columns(4)


total_customers_df = pd.read_sql(query , engine)

with col1:
    st.metric(
        label = 'Total Customers',
        value= f'{total_customers_df.iloc[0,0]:,}' #removes the comma
    )
#===============================================================================

#Total orders

if selected_State == 'All':
    query = """
select count(*) as total_orders
from orders;
"""
else:
    query = f"""
    select count(*) as total_oders
    from orders
    inner join customers
    on orders.customer_id = customers.customer_id
    where customer_state = '{selected_State}';
    """


total_orders_df = pd.read_sql(query , engine)

with col2:
    st.metric(
        label = 'Total orders',
        value=f'{total_orders_df.iloc[0,0]:,}'
    )
#==================================================================================
#Total revenue
if selected_State== 'All':
    query = """
select round(sum(payment_value),2) as total_revenue
from payments;
"""
else:
    query = f"""
    select  sum(payment_value) as total_revenue
from customers
inner join orders
on customers.customer_id = orders.customer_id 
inner join payments
on orders.order_id = payments.order_id
where customer_state = '{selected_State}';
"""
    
total_revenue_df = pd.read_sql(query , engine)

with col3:
    st.metric(
        label = 'Total Revenue',
        value=f'${total_revenue_df.iloc[0,0]:,.2f}'
    )

#==================================================================================

#Average Payment
if selected_State == 'All':
    query = """
select round(avg(payment_value ),2) as avg_payment
from payments;
"""

else:
    query = f"""

select avg(payment_value) as total_revenue
from customers
inner join orders
on customers.customer_id = orders.customer_id 
inner join payments
on orders.order_id = payments.order_id
where customer_state = '{selected_State}';
    """


avg_payments_df = pd.read_sql(query , engine)
     
with col4:
     st.metric(
        label = 'Avg payment',
        value=f'${avg_payments_df.iloc[0,0]:,.2f}'
    )
     
#=============================================================================

#Monthly revenue trend
if selected_State == 'All':
    query = """
select date_format(order_purchase_timestamp ,'%%Y-%%m') as month,
sum(payment_value) as total_revenue
from orders
inner join payments 
on orders.order_id = payments.order_id
group by month
order by month; 
"""

else:
    query = f"""
select date_format(order_purchase_timestamp ,'%%Y-%%m') as month,
sum(payment_value) as total_revenue
from customers
inner join orders
on customers.customer_id = orders.customer_id
inner join payments 
on orders.order_id = payments.order_id
where customer_state = '{selected_State}'
group by month
order by month;
"""

monthly_revenue_df = pd.read_sql(query , engine)


#Plotting
fig , ax = plt.subplots(figsize=(10,5))

ax.plot(
    monthly_revenue_df['month'],
    monthly_revenue_df['total_revenue'],
    marker = 'o'
)

ax.set_title('monthly Revenue Trend')
ax.set_xlabel('Month')
ax.set_ylabel('Revenue')
plt.xticks(rotation = 45)
st.pyplot(fig) #streamlit needs the figure object to be dispplayed inside the dashboard and not a sepearte window
#=============================================================================================================
col_left , col_right = st.columns(2)
if selected_State == 'All':
 query = """
select customer_state ,  sum(payment_value) as total_revenue
from customers
inner join orders
on customers.customer_id = orders.customer_id
inner join payments 
on orders.order_id = payments.order_id
group by customer_state
order by total_revenue desc;
"""
else:
     query = f"""
select customer_state ,  sum(payment_value) as total_revenue
from customers
inner join orders
on customers.customer_id = orders.customer_id
inner join payments 
on orders.order_id = payments.order_id
where customer_State = '{selected_State}'
group by customer_state
order by total_revenue desc;
"""

revenue_by_state_df = pd.read_sql(query ,engine)

fig ,ax = plt.subplots(figsize=(8,5))
ax.barh(revenue_by_state_df['customer_state'],
        revenue_by_state_df['total_revenue'],
        color = 'steelblue')

ax.set_title('Revenue By State')
ax.set_xlabel('Revenue')
ax.set_ylabel('States')
ax.invert_yaxis()
plt.tight_layout()

with col_left:
    st.pyplot(fig)
#===================================================================================================

if selected_State == 'All':
    query = """
select payment_type, count(*) as total_payments
from payments
group by payment_type
order by total_payments desc;
"""
else:
    query = f"""
select payment_type , count(*) as total_payments
from customers
inner join orders
on customers.customer_id = orders.customer_id
inner join payments 
on orders.order_id = payments.order_id
where customer_state = '{selected_State}'
group by payment_type
order by total_payments desc;
"""
    
payment_type_df = pd.read_sql(query, engine)

fig , ax = plt.subplots(figsize = (8,5))
ax.barh(payment_type_df['payment_type'],
        payment_type_df['total_payments'])

ax.set_title('Payments method distribution')
ax.set_xlabel('NUmber of Payments')
ax.set_ylabel('Payment Type')

plt.xticks(rotation = 20)

with col_right:
    st.pyplot(fig)

#================================================================================================
col_left_down , col_right_down = st.columns(2)

#Top 10 cities
if selected_State == 'All':
    query ="""
select customer_city ,
sum(payment_value) as total_revenue
from customers
inner join orders
on customers.customer_id = orders.customer_id
inner join payments
on orders.order_id = payments.order_id
group by customer_city
order by total_revenue desc
limit 10;
"""

else:
        query =f"""
select customer_city ,
sum(payment_value) as total_revenue
from customers
inner join orders
on customers.customer_id = orders.customer_id
inner join payments
on orders.order_id = payments.order_id
where customer_state = '{selected_State}'
group by customer_city
order by total_revenue desc
limit 10;
"""
top_cities_df = pd.read_sql(query , engine)
fig , ax = plt.subplots(figsize= (8,5))
ax.barh(top_cities_df['customer_city'],
       top_cities_df['total_revenue'],
       color = 'steelblue')


ax.set_title('Top 10 Cities By revenue')
ax.set_xlabel('Revenue')
ax.set_ylabel('Cities')

plt.xticks(rotation = 45)
with col_left_down:
    st.pyplot(fig)

#=================================================================================
#Product category revenue
query = """
select product_category_name , sum(price) as total_revenue
from order_items
inner join products on
order_items.product_id = products.product_id
group by product_category_name
order by total_revenue desc
limit 10;
"""

product_category_df = pd.read_sql(query , engine)

fig , ax = plt.subplots(figsize= (8,5))
ax.barh(product_category_df['product_category_name'],
      product_category_df['total_revenue'],
       color = 'steelblue')


ax.set_title('Product Category Revenue')
ax.set_xlabel('Revenue')
ax.set_ylabel('Product Category')
ax.invert_yaxis()
plt.xticks(rotation = 45)
with col_right_down:
    st.pyplot(fig)

st.subheader('geographic Revenue Heatmap')
st_folium(
    m,
    width=1000,
    height=600
)