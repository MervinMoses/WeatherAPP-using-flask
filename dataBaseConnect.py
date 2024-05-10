from dotenv import load_dotenv #pip install python-dotenv
from flask import request
import os
import pyodbc
import pandas as pd
from pydantic import BaseModel


# drop table userTable

# create table userTable (id int identity(1,1) primary key,username varchar(50),email varchar(100),upassword varchar(max),ispremium varchar(10) default 'false')

load_dotenv()
SERVER=os.getenv('SERVER')
DATABASE=os.getenv('DATABASE')
connectionString = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={SERVER};DATABASE={DATABASE}; Trusted_Connection=yes;'
conn = pyodbc.connect(connectionString)
id=None
ses_user=None

def getData(session_user):
    id=getID(session_user)
    if not isinstance(id, int):
        id = int(id)  # Convert to integer if necessary
    select_query = "SELECT cities FROM dbo.weather WHERE uid = ?"
    df = pd.read_sql(select_query, conn, params=[id])
    cities = df['cities'].tolist()
    return cities
    
def check_record_count(session_user):
    id=getID(session_user)
    if not isinstance(id, int):
        id = int(id)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM dbo.weather where uid=(?)",id)
    count = cursor.fetchone()[0]  # Get the count of records
    
    if count > 4:
        return False
    else:
        return True
    
def getID(ses_user):
    select_query = f"SELECT id FROM dbo.UserTable WHERE username = '{ses_user}'"
    df = pd.read_sql(select_query, conn)
    if not df.empty:
        id = df['id'].iloc[0]  # Extract the first password from the Series
        return id
        

def insert_city(current_user,new_city):
    id=getID(current_user)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dbo.weather (cities, uid) VALUES (?, ?)", (new_city,str(id)))
    conn.commit()

def get_premuim(session_user):
    ses_user=session_user
    id=getID(ses_user)
    if not isinstance(id, int):
        id = int(id)  # Convert to integer if necessary
    select_query = "SELECT ispremium FROM dbo.userTable WHERE id = ?"
    df = pd.read_sql(select_query, conn, params=[id])
    if not df.empty:
        premuim = df['ispremium'].iloc[0]
        if premuim=="true":
            return True
        return False
    return False
                  

def delete_city(city):
    cursor = conn.cursor()
    cursor.execute("delete from dbo.weather where (cities) = (?)", city) 
    conn.commit()
    
def getUsers():
    select_query = 'select * from dbo.UserTable'
    df = pd.read_sql(select_query, conn)
    users = [users for users in df['email']]
    return users

def getUserName():
    select_query = 'select * from dbo.UserTable'
    df = pd.read_sql(select_query, conn)
    users = [users for users in df['username']]
    return users

def getPassword(username):
    select_query = f"select id,upassword from dbo.UserTable where username=('{username}')"
    df = pd.read_sql(select_query, conn)
    if not df.empty:
        password = df['upassword'].iloc[0]  # Extract the first password from the Series
        return password
    

def register_user(new_user_email, new_user_username, new_user_password):
    cursor = conn.cursor()
    cursor.execute("INSERT INTO dbo.UserTable (username,email,upassword) VALUES (?,?,?)",new_user_email, new_user_username, new_user_password)
    conn.commit()
    return True
        
 
    



    

        
        