import streamlit as st

from deta import Deta
from datetime import datetime
import pandas as pd
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from streamlit_option_menu import option_menu
from io import BytesIO


DETA_KEY = st.secrets["DETA_KEY"]

deta=Deta(DETA_KEY)


db=deta.Base("clients")
db1=deta.Base("admins")
now = datetime.now()
d1= now.strftime("%d/%m/%Y %H:%M:%S")

def insert_period(names, l_name, emails,livcountry,livcity,fee,grade,enlang,gerlang,country):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"First Name": names, "Last Name": l_name, "Email address": emails,"Country":livcountry,"City":livcity,"Fee":fee,"Average grade":grade,"Level of English":enlang,
                   "Level of German":gerlang,"Prefered country of studies":country,"Application status":"No status yet","Date of entry":d1})

def fetch_all_users():
    """Returns a dict of all users"""
    res = db1.fetch()
    return res.items


def to_excel(df):
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, index=False, sheet_name='Sheet1')
    workbook = writer.book
    worksheet = writer.sheets['Sheet1']
    format1 = workbook.add_format({'num_format': '0.00'}) 
    worksheet.set_column('A:A', None, format1)  
    writer.save()
    processed_data = output.getvalue()
    return processed_data



selected=option_menu(
    menu_title="Main Menu",
    options=["Leave a record and see a recommendation","Edit database"],
    icons=["house","book"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
    )

if selected=="Leave a record and see a recommendation":
    name = st.text_area("", placeholder="Enter your first name here ...")
    last_name = st.text_area("", placeholder="Enter your last name here ...")
    email = st.text_area("", placeholder="Enter your email here ...")
    livcountry = st.text_area("", placeholder="Enter the country you live in here ...")
    livcity = st.text_area("", placeholder="Enter the city you live in here ...")
    fee=st.selectbox('Fee',('Free of charge studies','Paid studies'))
    grade=st.text_area("", placeholder="Enter your average school/university grade here...")
    enlang=st.selectbox('Level of English',('A1(Elementary)','A2(Elementary)','B1(Intermediate)','B2(Intermediate)','C1(Advanced)','C2(Advanced)'))
    gerlang=st.selectbox('Level of German',('A1(Lower Beginner)','A2(Upper Beginner)','B1(Lower Intermediate)','B2(Upper Intermediate)','C1(Lower Advanced)','C2(Upper Advanced/Fluent)','Goethe-Zertifikat','Goethe-Test PRO'))
    country=st.selectbox('Country of studies',('Austria','Hungary'))

    
    
    
    #st.subheader('Result')
    if st.button('Save'):
        insert_period(name,last_name,email,livcountry,livcity,fee,grade,enlang,gerlang,country)
        #res = db.fetch()
        #all_items = res.items
        #df = pd.DataFrame(all_items)
        st.write('Thank you, your record is saved')



if selected=="Edit database":
    users=fetch_all_users()

    usernames = [user["key"] for user in users]
    names = [user["name"] for user in users]
    hashed_passwords = [user["password"] for user in users]



    credentials = {"usernames":{}}

    for un, name, pw in zip(usernames, names, hashed_passwords):
        user_dict = {"name":name,"password":pw}
        credentials["usernames"].update({un:user_dict})



    authenticator = stauth.Authenticate(credentials, "app_home", "auth", cookie_expiry_days=30)

    name, authentication_status, username = authenticator.login("Login", "main")

    if authentication_status:
        #st.error("Username/password is correct")
        
        authenticator.logout("Logout", "sidebar")
        res = db.fetch()
        all_items = res.items
        df = pd.DataFrame(all_items)
        
        csv=df.to_csv().encode('utf-8')
        
        df_xlsx = to_excel(df)
        
        st.dataframe(df)
        st.download_button(
            label="Download data as Excel",
            data=df_xlsx,
            file_name='database.xlsx'#,
            #mime='text/csv',
            )
        st.header('Type data of the student')
        
        edname = st.text_area("", placeholder="Enter name of student ...")
        edlname = st.text_area("", placeholder="Enter last name of student ...")
        edemail=st.text_area("", placeholder="Enter email of student ...")
        
        #if st.button('Edit'):
        if len(df[(df['First Name']==edname)&(df['Last Name']==edlname)])>0:
            student_key=df[(df['First Name']==edname)&(df['Last Name']==edlname)&(df['Email address']==edemail)]['key'].tolist()[0]
            change=st.selectbox('What do you want to edit?',('First Name','Last Name','Email address','Country','City','Fee','Average grade','Level of English','Level of German','Prefered country of studies','Application status'))
            if change=='Application status':
                
                status=st.selectbox('Application status',('No status yet','Admitted','Failed'))
                if st.button('Save'):
                    updates = {
                        "Application status":status
                        }
                    db.update(updates, student_key)
                    st.write('Record was editted')
                
            elif change=='First Name':
                new_name=st.text_area("", placeholder="Change name of the student ...")
                if st.button('Save'):
                    updates = {
                        "First Name":new_name
                        }
                    db.update(updates, student_key)
                    st.write('Record was editted')
            
            elif change=='Last Name':
                newl_name=st.text_area("", placeholder="Change last name of the student ...")
                if st.button('Save'):
                    updates = {
                        "Last Name":newl_name
                        }
                    db.update(updates, student_key)
                    st.write('Record was editted')    
            
            elif change=='Email address':
                new_email=st.text_area("", placeholder="Change Email address of the student ...")
                if st.button('Save'):
                    updates = {
                        "Email address":new_email
                        }
                    db.update(updates, student_key)
                    st.write('Record was editted')
            
            elif change=='Country':
                new_country=st.text_area("", placeholder="Change country of the student ...")
                if st.button('Save'):
                    updates = {
                        "Country":new_country
                        }
                    db.update(updates, student_key)
                    st.write('Record was editted')
            
            elif change=='City':
                new_city=st.text_area("", placeholder="Change city of the student ...")
                if st.button('Save'):
                    updates = {
                        "City":new_city
                        }
                    db.update(updates, student_key)
                    st.write('Record was editted')
            
            elif change=='Fee':
                new_fee=st.selectbox('Fee',('Free of charge studies','Paid studies'))
                if st.button('Save'):
                    updates = {
                        "Fee":new_fee
                        }
                    db.update(updates, student_key)
                    st.write('Record was editted')
            
            elif change=='Average grade':
                new_grade=st.text_area("", placeholder="Change average grade of the student ...")
                if st.button('Save'):
                    updates = {
                        "Average grade":new_grade
                        }
                    db.update(updates, student_key)
                    st.write('Record was editted')
                    
            elif change=='Level of English':
                new_eng=st.selectbox('Level of English',('A1(Elementary)','A2(Elementary)','B1(Intermediate)','B2(Intermediate)','C1(Advanced)','C2(Advanced)'))
                if st.button('Save'):
                    updates = {
                        "Level of English":new_eng
                        }
                    db.update(updates, student_key)
                    st.write('Record was editted')        
                    
            elif change=='Level of German':
                new_ger=st.selectbox('Level of German',('A1(Lower Beginner)','A2(Upper Beginner)','B1(Lower Intermediate)','B2(Upper Intermediate)','C1(Lower Advanced)','C2(Upper Advanced/Fluent)','Goethe-Zertifikat','Goethe-Test PRO'))
                if st.button('Save'):
                    updates = {
                        "Level of German":new_ger
                        }
                    db.update(updates, student_key)
                    st.write('Record was editted')       
                    
            elif change=='Prefered country of studies':
                new_stcountry=st.selectbox('Country of studies',('Austria','Hungary'))
                if st.button('Save'):
                    updates = {
                        "Prefered country of studies":new_stcountry
                        }
                    db.update(updates, student_key)
                    st.write('Record was editted')        
                    
            
                
                    
                
        
        else:
            st.error("No such student or you put incorrect data")
        
        
        
   
        
        
        
        
        
        

    if authentication_status == False:  
        st.error("Username/password is incorrect")
    
    if authentication_status == None:
        st.warning("Please enter your username and password")    

    









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





    