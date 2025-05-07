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
pdData=pd.DataFrame(data,columns=["编号","内容"])
print(pdData.iloc[0]["内容"])
pdData["内容长度"]=pdData['内容'].str.len()
print("文本长度均值",pdData["内容长度"].mean())
print("文本长度方差",pdData["内容长度"].var())
print("文本长度最大值",pdData["内容长度"].max())
print("文本长度最小值",pdData["内容长度"].min())
print("运行正常")