
import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title(f"My mum's New Healthy Diner")

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avacado Toast')

streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pd.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show )

# create the repeatable code block 
def get_fruityvice_date(this_fruit_choice):
     fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
     fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
     return fruityvice_normalized

# New section to display fruityvice api response
streamlit.header("Fruityvice Fruit Advice!")
## Add a Text Entry Box and Send the Input to Fruityvice as Part of the API Call
#fruit_choice = streamlit.text_input('What fruit would you like information about?','Kiwi')
try:
    fruit_choice = streamlit.text_input("What fruit would you like information about?")
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:
        back_from_function = get_fruityvice_date(fruit_choice)
        streamlit.dataframe(back_from_function)
except URLError as e:
    streamlit.error()

#streamlit.write('The user entered ', fruit_choice)

#fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
#streamlit.text(fruityvice_response.json())

# flatten the json format to tabluar form dataframe
#fruityvice_normalized = pd.json_normalize(fruityvice_response.json())
# make a table on streamlit
#streamlit.dataframe(fruityvice_normalized)
# don't run anything past here while we troubleshoot




# connect to snowflake trail account
#my_cur = my_cnx.cursor()
#my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")

streamlit.header("The fruit load list contains:")
# Snowflake-related functions
def get_fruit_load_list():
     with my_cnx.cursor() as my_cur:
          my_cur.execute("select * from fruit_load_list")
          return my_cur.fetchall()
# add a button to load the fruit
if streamlit.button('Get Fruit Load List'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     my_data_rows = get_fruit_load_list()
     my_cnx.close()
     streamlit.dataframe(my_data_rows)
#streamlit.stop()
     
# allow the end user to add a fruit to the list
def insert_row_snowflake(new_fruit):
     with my_cnx.cursor() as my_cur:
          my_cur.execute("insert into fruit_load_list values ('" + new_fruit + "')")
          return "Thanks for adding " + new_fruit
add_my_fruit = streamlit.text_input("What fruit would you like to add?")
if streamlit.button('Add a Fruit to the List'):
     my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
     back_from_function = insert_row_snowflake(add_my_fruit)
     my_cnx.close()
     streamlit.text(back_from_function)

