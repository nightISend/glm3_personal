import pandas as pd
import psycopg2

postgre_connect = psycopg2.connect(
    database="work12345", 
    user="postgres", 
    password="Lvu123123",
    host="localhost",
    port="5432")
cursor = postgre_connect.cursor()

""" keep_default_na=False使excel里的空值为'' """
data=pd.read_excel("F:/Repo/资料备份/毕设/数据库数据/数据.xlsx",sheet_name="未训练提取（有历史记录，全）",keep_default_na=False)
for index, row in data.iterrows():
    id = row['id']
    events = row['events']
    category=row['category']
    name=row['name']
    phone=row['phone']
    occur_time=row['occur_time']
    solve_time=row['solve_time']
    goal=row['goal']
    address=row['address']
    geom=row['geom']
    longitude=row['longitude']
    latitude=row['latitude']
    sql=''
    if geom!='':
        sql=f'''
                INSERT INTO public.sum_12345_wash1(
                id, events, category, name, phone, goal, occur_time, solve_time, address, longitude, latitude, geom)
                VALUES ('{id}', '{events}', '{category}', '{name}', '{phone}', '{goal}','{occur_time}', '{solve_time}', '{address}', '{longitude}', '{latitude}', '{geom}');
            '''
    else:
        sql=f'''
                INSERT INTO public.sum_12345_wash1(
                id, events, category, name, phone,goal, occur_time, solve_time, address, geom)
                VALUES ('{id}', '{events}', '{category}', '{name}', '{phone}', '{goal}','{occur_time}', '{solve_time}', '{address}', null);
            '''
        
    print(sql)
    cursor.execute(sql)
    postgre_connect.commit()
cursor.close()  # 关闭游标
postgre_connect.close()  # 关闭数据库
