import streamlit as st

from deta import Deta
import pandas as pd



#DETA_KEY="a02njvwb_d9c6HV6N6AiVe9oDS4hqYUgQcUggWz2b"
DETA_KEY = st.secrets["DETA_KEY"]

deta=Deta(DETA_KEY)


db=deta.Base("clients")

name = st.text_area("", placeholder="Enter your first name here ...")
last_name = st.text_area("", placeholder="Enter your last name here ...")
email = st.text_area("", placeholder="Enter your email here ...")


def insert_period(names, l_name, emails):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"First Name": names, "Last Name": l_name, "Email address": emails})


# def fetch_all_periods():
#     """Returns a dict of all periods"""
#     res = db.fetch()
#     periods = [re for re in res]
#     return periods


# def get_period(period):
#     """If not found, the function will return None"""
#     return db.get(period)

#insert_period("feb", 2000, 3000, "no")

st.subheader('Result')
if st.button('push'):
    insert_period(name,last_name,email)
    res = db.fetch()
    all_items = res.items
    df = pd.DataFrame(all_items)
    st.write(df['First Name'][0])


















# Initialize connection.
# Uses st.experimental_singleton to only run once.
# @st.experimental_singleton

# Connection parameters
# host = "hostname"
# port = 5432
# database = "database_name"
# user = "user_name"
# password = "password"

# # Connect to the database
# conn = psycopg2.connect(host=host, port=port, database=database, user=user, password=password)


# def init_connection():
#     return psycopg2.connect(**st.secrets["postgres"])

# conn = init_connection()

# Perform query.
# Uses st.experimental_memo to only rerun when the query changes or after 10 min.
# @st.experimental_memo(ttl=600)
# def run_query(query):
#     with conn.cursor() as cur:
#         cur.execute(query)
#         return cur.fetchall()

# rows = run_query("SELECT * from clients;")

# Print results.
# for row in rows:
#     st.write(f"{row[0]} has a :{row[1]}:")
    
# Print the results
# for row in rows:
#     print(row)

# # Close the cursor and connection
# # cur.close()
# conn.close()





    