import streamlit as st

from deta import Deta
from datetime import datetime
import pandas as pd
import streamlit_authenticator as stauth  # pip install streamlit-authenticator
from streamlit_option_menu import option_menu
from io import BytesIO
import plotly.express as px


DETA_KEY = st.secrets["DETA_KEY"]

deta=Deta(DETA_KEY)


db=deta.Base("clients")
db1=deta.Base("admins")
now = datetime.now()
d1= now.strftime("%d/%m/%Y %H:%M:%S")

def insert_period(names, l_name, emails,livcountry,livcity,fee,deg,grade,enlang,gerlang,country):
    """Returns the report on a successful creation, otherwise raises an error"""
    return db.put({"First Name": names, "Last Name": l_name, "Email address": emails,"Country":livcountry,"City":livcity,"Fee":fee,"Degree":deg,"Average grade":grade,"Level of English":enlang,
                   "Level of German":gerlang,"Prefered country of studies":country,"University applied to":"No university listed","University admitted to":"No university listed","Application status":"No status yet","Date of entry":d1})

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
    menu_title="Главное Меню",
    options=["Ввести данные и посмотреть вероятность поступления","База данных(для админов)"],
    icons=["house","book"],
    menu_icon="cast",
    default_index=0,
    orientation="horizontal"
    )

if selected=="Ввести данные и посмотреть вероятность поступления":
    st.write('Заполните форму чтобы посмотреть рекомендацию и вероятность поступления')
    name = st.text_area("", placeholder="Ваше имя ...")
    last_name = st.text_area("", placeholder="Ваша фамилия ...")
    email = st.text_area("", placeholder="Ваш email ...")
    livcountry = st.text_area("", placeholder="Страна проживания ...")
    livcity = st.text_area("", placeholder="Город проживания ...")
    fee=st.selectbox('Желаемая форма обучения',('Бесплатная(стипендия)','Платная'))
    deg=st.selectbox('Предпочтительный уровень образования',('Бакалавриат','Магистратура'))
    
    grade = st.number_input("Ваш средний балл в школе/университете...")
    #grade=st.text_area("", placeholder="Enter your average school/university grade here...")
    enlang=st.selectbox('Уровень английского',('Никакой','A1','A2','B1','B2','C1','C2'))
    gerlang=st.selectbox('Уровень немецкого',('Никакой','A1','A2','B1','B2','C1','C2'))
    if fee=='Бесплатная(стипендия)':
        st.write('Вы выбрали бесплатную форму обучения как желаемую, в таком случае рекомендуем Вам рассмотреть вариант с поступлением в *венгерские* университеты')
        
    else:
        st.write('Вы выбрали платную форму обучения как желаемую, в таком случае рекомендуем Вам рассмотреть вариант с поступлением в *австрийские* университеты')
    country=st.selectbox('Предпочитаемая страна обучения',('Венгрия','Австрия'))
    if country=='Австрия':
         bur=st.selectbox('Знание бюрократического лексикона и законов',('Плохое','Хорошее','Отличное'))

    
    
    
    #st.subheader('Result')
    if st.button('Сохранить'):
        insert_period(name,last_name,email,livcountry.lower(),livcity.lower(),fee,deg,grade,enlang,gerlang,country)
        #res = db.fetch()
        #all_items = res.items
        #df = pd.DataFrame(all_items)
        st.write('Спасибо, ваша информация записана!')
        st.write('Вероятность вашего успешного поступления на основе введенных показателей:')
        if (country=='Венгрия'):
            if (enlang=='A1'):
                if (grade>=3.0)&(grade<3.5):
                    st.write('25%')
                    st.write('C помощью Samga Abroad вы поднимите вероятность поступления до 58% !')
                elif (grade<3.0):
                    st.write('10%')    
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 50% !') 
                elif (grade>=3.5)&(grade<4.5):
                    st.write('45%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 78% !')
                elif (grade>=4.5)&(grade<=5.0):
                    st.write('60%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 80% !')   
            elif (enlang=='Никакой'):
                if (grade>=3.0)&(grade<3.5):
                    st.write('15%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 55% !')
                elif (grade<3.0):
                    st.write('меньше 10%')    
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 50% !')    
                elif (grade>=3.5)&(grade<4.5):
                    st.write('35%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 68% !')
                elif (grade>=4.5)&(grade<=5.0):
                    st.write('50%')   
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 70% !')
            elif (enlang=='A2'):
                if (grade>=3.0)&(grade<3.5):
                    st.write('30%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 63% !')
                elif (grade<3.0):
                    st.write('15%')   
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 55% !')    
                elif (grade>=3.5)&(grade<4.5):
                    st.write('50%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 83% !')
                elif (grade>=4.5)&(grade<=5.0):
                    st.write('65%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 85% !')
            elif (enlang=='B1'):
                if (grade>=3.0)&(grade<3.5):
                    st.write('40%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 73% !')
                elif (grade<3.0):
                    st.write('25%')   
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 58% !')
                elif (grade>=3.5)&(grade<4.5):
                    st.write('60%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 80% !')
                elif (grade>=4.5)&(grade<=5.0):
                    st.write('75%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 90% !')
            elif (enlang=='B2'):
                if (grade>=3.0)&(grade<3.5):
                    st.write('50%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 70% !')
                elif (grade<3.0):
                    st.write('35%')    
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 68% !')
                elif (grade>=3.5)&(grade<4.5):
                    st.write('70%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 90% !')
                elif (grade>=4.5)&(grade<=5.0):
                    st.write('85%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
            elif (enlang=='C1'):
                if (grade>=3.0)&(grade<3.5):
                    st.write('55%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 75% !')
                elif (grade<3.0):
                    st.write('40%')    
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 73% !')
                elif (grade>=3.5)&(grade<4.5):
                    st.write('75%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 90% !')
                elif (grade>=4.5)&(grade<=5.0):
                    st.write('90%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
            elif (enlang=='C2'):
                if (grade>=3.0)&(grade<3.5):
                    st.write('65%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 85% !')
                elif (grade<3.0):
                    st.write('50%')    
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 70% !')
                elif (grade>=3.5)&(grade<4.5):
                    st.write('85%')
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
                elif (grade>=4.5)&(grade<=5.0):
                    st.write('100%')       
                    st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
        elif (country=='Австрия'):
            if deg=='Бакалавриат':
                if (gerlang=='A1'):
                    if bur=='Плохое':
                        st.write('25%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 58% !')
                    elif bur=='Хорошее':
                        st.write('45%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 78% !')
                    elif bur=='Отличное':
                        st.write('60%')  
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 80% !')
                elif (gerlang=='A2'):
                    if bur=='Плохое':
                        st.write('30%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 63% !')
                    elif bur=='Хорошее':
                        st.write('50%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 83% !')
                    elif bur=='Отличное':
                        st.write('65%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 85% !')
                elif (gerlang=='Никакой'):
                    if bur=='Плохое':
                        st.write('15%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 55% !')
                    elif bur=='Хорошее':
                        st.write('35%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 68% !')
                    elif bur=='Отличное':
                        st.write('50%')  
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 70% !')
                elif (gerlang=='B1'):
                    if bur=='Плохое':
                        st.write('40%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 73% !')
                    elif bur=='Хорошее':
                        st.write('60%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 80% !')
                    elif bur=='Отличное':
                        st.write('75%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 90% !')
                elif (gerlang=='B2'):
                    if bur=='Плохое':
                        st.write('50%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 70% !')
                    elif bur=='Хорошее':
                        st.write('70%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 90% !')
                    elif bur=='Отличное':
                        st.write('85%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
                elif (gerlang=='C1'):
                    if bur=='Плохое':
                        st.write('55%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 75% !')
                    elif bur=='Хорошее':
                        st.write('75%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 90% !')
                    elif bur=='Отличное':
                        st.write('90%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
                elif (gerlang=='C2'):
                    if bur=='Плохое':
                        st.write('65%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 85% !')
                    elif bur=='Хорошее':
                        st.write('85%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
                    elif bur=='Отличное':
                        st.write('100%') 
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
            else:
                if (enlang=='A1'):
                    if bur=='Плохое':
                        st.write('25%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 58% !')
                    elif bur=='Хорошее':
                        st.write('45%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 78% !')
                    elif bur=='Отличное':
                        st.write('60%')  
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 80% !')
                elif (enlang=='A2'):
                    if bur=='Плохое':
                        st.write('30%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 63% !')
                    elif bur=='Хорошее':
                        st.write('50%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 83% !')
                    elif bur=='Отличное':
                        st.write('65%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 85% !')
                elif (enlang=='Никакой'):
                    if bur=='Плохое':
                        st.write('15%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 55% !')
                    elif bur=='Хорошее':
                        st.write('35%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 68% !')
                    elif bur=='Отличное':
                        st.write('50%')  
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 70% !')
                elif (enlang=='B1'):
                    if bur=='Плохое':
                        st.write('40%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 73% !')
                    elif bur=='Хорошее':
                        st.write('60%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 80% !')
                    elif bur=='Отличное':
                        st.write('75%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 90% !')
                elif (enlang=='B2'):
                    if bur=='Плохое':
                        st.write('50%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 70% !')
                    elif bur=='Хорошее':
                        st.write('70%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 90% !')
                    elif bur=='Отличное':
                        st.write('85%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
                elif (enlang=='C1'):
                    if bur=='Плохое':
                        st.write('55%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 75% !')
                    elif bur=='Хорошее':
                        st.write('75%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 90% !')
                    elif bur=='Отличное':
                        st.write('90%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
                elif (enlang=='C2'):
                    if bur=='Плохое':
                        st.write('65%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 85% !')
                    elif bur=='Хорошее':
                        st.write('85%')
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
                    elif bur=='Отличное':
                        st.write('100%') 
                        st.write('С помощью Samga Abroad вы поднимите вероятность поступления до 100% !')
                
        st.write('Данная оценка вероятности является приблизительной, так как условия поступления в университеты на разные специальности могут радикально отличаться. Мы советуем выйти на связь с нашими экспертами для более точного персонального анализа вашей ситуации')        
            



if selected=="База данных(для админов)":
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
        df=df.drop_duplicates(subset=['Email address'])
        df['Date of entry']=pd.to_datetime(df['Date of entry'], format="%d/%m/%Y %H:%M:%S")
        df=df.sort_values(by='Date of entry',ascending=False)
        
        csv=df.to_csv().encode('utf-8')
        
        df_xlsx = to_excel(df)
        
        st.dataframe(df)
        st.download_button(
            label="Скачать базу в формате Excel",
            data=df_xlsx,
            file_name='database.xlsx'#,
            #mime='text/csv',
            )
        check=st.checkbox('Анализ')
        if check:
            df['count']=1
            fig=px.pie(df,names='Prefered country of studies',values='count')
            st.header('Страна обучения')
            st.write(fig)
            
            st.header('Страна проживания')
            fig1=px.pie(df,names='Country',values='count',color_discrete_sequence=px.colors.sequential.Viridis)
            st.write(fig1)
            
            fig=px.pie(df,names='Fee',values='count',color_discrete_sequence=px.colors.sequential.Plasma)
            st.header('Выбранная форма обучения')
            st.write(fig)   
            
            fig=px.pie(df,names='Application status',values='count',color_discrete_sequence=px.colors.sequential.Cividis)
            st.header('Статус поступления')
            st.write(fig) 
            
            df1=df
            df1['Date of entry']=pd.to_datetime(df1['Date of entry'], format="%d/%m/%Y").dt.date
            fig = px.line(df1.groupby(by='Date of entry').sum())
            st.header('Количество записей в день')
            st.write(fig)
        
        
        st.write('Найти студента в базе:')
        ement = st.text_area("", placeholder="Введите имя и фамилию студента для просмотра ...")
        #ement1 = st.text_area("", placeholder="Enter last name of student you want to look at ...")
        if st.button('Показать'):
            st.dataframe(df[(((df['First Name']==ement.split()[0].lower())|(df['First Name']==ement.split()[0]))|((df['First Name']==ement.split()[1].lower())|(df['First Name']==ement.split()[1])))&(((df['Last Name']==ement.split()[0].lower())|(df['Last Name']==ement.split()[0]))|((df['Last Name']==ement.split()[1].lower())|(df['Last Name']==ement.split()[1])))])
        st.write('Введите email студента чьи данные вы хотите поменять:')
        # edname = st.text_area("", placeholder="Введите имя ...")
        # edlname = st.text_area("", placeholder="Введите фамилию ...")
        edemail=st.text_area("", placeholder="Введите email ...")
        
        #if st.button('Edit'):
        if len(df[((df['First Name']==ement.split()[0])|(df['First Name']==ement.split()[1]))&((df['Last Name']==ement.split()[1])|(df['Last Name']==ement.split()[0]))])>0:
            student_key=df[(df['Email address']==edemail)]['key'].tolist()[0]
            change=st.selectbox('Что вы хотите изменить?',('Имя','Фамилия','Email','Страна','Город','Желаемая форма обучения','Средний балл','Уровень английского','Уровень немецкого','Страна обучения','Выбранный университет','Университет поступления','Статус поступления','Удалить студента из базы'))
            if change=='Статус поступления':
                
                status=st.selectbox('Статус поступления',('Нет статуса','Поступил/а','Не поступил/а'))
                if st.button('Сохранить'):
                    updates = {
                        "Application status":status
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')
            elif change=='Выбранный университет':
                newl_name=st.text_area("", placeholder="Измените выбранный университет ...")
                if st.button('Сохранить'):
                    updates = {
                        "University applied to":newl_name
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')     
            elif change=='Университет поступления':
                newl_name=st.text_area("", placeholder="Измените университет поступления...")
                if st.button('Сохранить'):
                    updates = {
                        "University admitted to":newl_name
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')         
                
            elif change=='Имя':
                new_name=st.text_area("", placeholder="Измените имя ...")
                if st.button('Сохранить'):
                    updates = {
                        "First Name":new_name
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')
            
            elif change=='Фамилия':
                newl_name=st.text_area("", placeholder="Измените фамилию ...")
                if st.button('Сохранить'):
                    updates = {
                        "Last Name":newl_name
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')    
            
            elif change=='Email':
                new_email=st.text_area("", placeholder="Измените email ...")
                if st.button('Сохранить'):
                    updates = {
                        "Email address":new_email
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')
            
            elif change=='Страна':
                new_country=st.text_area("", placeholder="Введите страну ...")
                if st.button('Сохранить'):
                    updates = {
                        "Country":new_country
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')
            
            elif change=='Город':
                new_city=st.text_area("", placeholder="Введите город ...")
                if st.button('Сохранить'):
                    updates = {
                        "City":new_city
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')
            
            elif change=='Форма обучения':
                new_fee=st.selectbox('Форма обучения',('Бесплатная(стипендия)','Платная'))
                if st.button('Сохранить'):
                    updates = {
                        "Fee":new_fee
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')
            
            elif change=='Средний балл':
                new_grade=st.number_input("Введите новый средний балл...")
                if st.button('Сохранить'):
                    updates = {
                        "Average grade":new_grade
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')
                    
            elif change=='Уровень английского':
                new_eng=st.selectbox('Уровень английского',('A1','A2','B1','B2','C1','C2'))
                if st.button('Сохранить'):
                    updates = {
                        "Level of English":new_eng
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')        
                    
            elif change=='Уровень немецкого':
                new_ger=st.selectbox('Уровень немецкого',('A1','A2','B1','B2','C1','C2'))
                if st.button('Сохранить'):
                    updates = {
                        "Level of German":new_ger
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')       
                    
            elif change=='Страна обучения':
                new_stcountry=st.selectbox('Страна обучения',('Венгрия','Австрия'))
                if st.button('Сохранить'):
                    updates = {
                        "Prefered country of studies":new_stcountry
                        }
                    db.update(updates, student_key)
                    st.write('Запись сохранена')        
                    
            elif change=='Удалить студента из базы':
                if st.button('Удалить'):
                    db.delete(student_key) 
                    st.write('Запись удалена')
                
                    
                
        
        else:
            st.error("Студента с такими данными не существует в базе, проверьте введенную информацию")
        
        
        
   
        
        
        
        
        
        

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





    