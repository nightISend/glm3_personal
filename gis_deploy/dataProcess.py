import pandas as pd
import psycopg2

postgre_connect = psycopg2.connect(
    database="work12345", 
    user="postgres", 
    password="Lvu123123",
    host="localhost",
    port="5432")
cursor = postgre_connect.cursor()
sql='''select id,events from sum_12345_wash'''
cursor.execute(sql) 
data=cursor.fetchall()

for row in data:
    events=row[1].replace('_x000D_','')
    updatesql=f'''
    UPDATE public.sum_12345_wash
	SET events=\'{events}\'
	WHERE id=\'{row[0]}\';
    '''
    cursor.execute(updatesql)
    postgre_connect.commit()
print("完成")