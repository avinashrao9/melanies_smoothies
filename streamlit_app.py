# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title(f":cup_with_straw: Customize your Smoothie!!")
st.write(
  """Choose the fruits you want in your custom Smoothie
  """
)

#option = st.selectbox(
#    "What is your favourite fruit?",
#    ("Banana", "Strawberries", "Peaches"),
#)

#st.write("You selected:", option)

#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)

name = st.text_input('Name on Smoothie')
st.write(name)

ingredients_list = st.multiselect(
    "Choose upto 5 ingredients..",my_dataframe,
    max_selections=5,
    #accept_new_options=True,
)

if ingredients_list:
    st.write(ingredients_list)

ingredients_string = ''
for each_fruit in ingredients_list:
    ingredients_string += each_fruit + ' '

st.write(ingredients_string)

my_insert_stmt = """ insert into smoothies.public.orders(name_on_order,ingredients)
                    values ('""" + name + """','""" + ingredients_string + """')"""

#st.write(my_insert_stmt)

time_to_insert = st.button('Submit Order')

if time_to_insert:
    session.sql(my_insert_stmt).collect()
    st.success('Your Smoothie is ordered!,' + name, icon="✅")

import requests  
smoothiefroot_response = requests.get("https://my.smoothiefroot.com/api/fruit/watermelon")  
st.text(smoothiefroot_response.json())
