import streamlit as st

from deta import Deta
import pandas as pd
import streamlit_authenticator as stauth  # pip install streamlit-authenticator



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




def fetch_all_users():
    """Returns a dict of all users"""
    res = db1.fetch()
    return res.items




db1=deta.Base("admins")



# users = fetch_all_users()

# usernames = [user["username"] for user in users]
# names = [user["First Name"] for user in users]
# hashed_passwords = [user["password"] for user in users]

# usernames=['ilyas3141','kymbat123','daniil456']
# names=['Ilias','Kymbat','Daniil']
# passwords=['ilyas3141','abc123','qwert456']
# hashed_passwords=stauth.Hasher(passwords).generate()


# credentials = {"usernames":{}}

# for un, name, pw in zip(usernames, names, passwords):
#     user_dict = {"name":name,"password":pw}
#     credentials["usernames"].update({un:user_dict})


# credentials = {
#         "key":{
#             "h84lu76ma34g":{
#                 "First Name":"Ilias",
#                 "password":"$2b$12$Fx29SffZvhhKHuGNtztaz.mndfT52s8q4fCbG5RJKyV7XV9W8pKW.",
#                 "username": "ilyas3141"
#                 },
#             "n4h15bebbidj":{
#                 "First Name":"Kymbat",
#                 "password":"$2b$12$KSKtf7Vibssl5V.gG7V1d.6R8Flr8bqzIcG2RnmMlldBkYKrjJiPm",
#                 "username": "kymbat123"
#                 }            
#             }
#         }


# names = ['John Smith', 'Rebecca Briggs']
# usernames = ['jsmith', 'rbriggs']
# passwords = ['123', '456']



# credentials = {"usernames":{}}

# for un, name, pw in zip(usernames, names, passwords):
#     user_dict = {"name":name,"password":pw}
#     credentials["usernames"].update({un:user_dict})

# credentials={'usernames': {'daniil456': {'name': 'Daniil', 'password': 'ilyas3141'},
#   'ilyas3141': {'name': 'Ilias', 'password': 'abc123'},
#   'kymbat123': {'name': 'Kymbat', 'password': 'qwert456'}}}




#WORKING CODE FOR LOGIN

# users=fetch_all_users()

# usernames = [user["key"] for user in users]
# names = [user["name"] for user in users]
# hashed_passwords = [user["password"] for user in users]



# credentials = {"usernames":{}}

# for un, name, pw in zip(usernames, names, hashed_passwords):
#     user_dict = {"name":name,"password":pw}
#     credentials["usernames"].update({un:user_dict})



# authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)

# name, authentication_status, username = authenticator.login("Login", "main")

# if authentication_status:
#     st.error("Username/password is correct")

# if authentication_status == False:
#     st.error("Username/password is incorrect")
    
# if authentication_status == None:
#     st.warning("Please enter your username and password")    













# authenticator = stauth.Authenticate(credentials,"sales_dashboard", "abcdef", cookie_expiry_days=30)

# name, authentication_status, username = authenticator.login("Login", "main")

# if authentication_status == False:
#     st.error("Username/password is incorrect")

# if authentication_status == None:
#     st.warning("Please enter your username and password")

# if authentication_status:
#     st.write("you logged in")
#     fname = st.text_area("", placeholder="Enter the first name of the student here ...")
#     lname = st.text_area("", placeholder="Enter the last name of the student here ...")
















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





    