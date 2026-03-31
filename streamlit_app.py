# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
import requests
import pandas as pd

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie!!")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'),col('SEARCH_ON'))
#st.dataframe(data=my_dataframe, use_container_width=True)

pd_sf = my_dataframe.to_pandas()
#st.dataframe(pd_df)

name = st.text_input('Name on Smoothie')
st.write(name)

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients..",my_dataframe,
    max_selections=5,
)

if ingredients_list:
    st.write(ingredients_list)

ingredients_string = ''
for each_fruit in ingredients_list:
    ingredients_string += each_fruit + ' '
  
    search_on=pd_df.loc[pd_df['FRUIT_NAME'] == each_fruit, 'SEARCH_ON'].iloc[0]
    st.write('The search value for ', each_fruit,' is ', search_on, '.')
  
    st.subheader(each_fruit + ' Nutrition information')
    smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/" + each_fruit)  
    sf_df = st.dataframe(data=smoothiefroot_response.json(), use_container_width=True)

st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(name_on_order,ingredients)
                    values ('""" + name + """','""" + ingredients_string + """')"""

#st.write(my_insert_stmt)

time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!,' + name, icon="✅")
