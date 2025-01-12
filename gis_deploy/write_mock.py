import pandas as pd
import json
import random
from datetime import timedelta
import psycopg2
def write_mock(data):
    file=open("mock.json",'w',encoding="utf-8")
    data_dict={"id":"",
               "events":"",
               "category":"",
               "name":"",
               "phone":"",
               "occur_time":"",
               "solve_time":"",
               "address":'',
               "longitude":'',
               "latitude":'',
               "geom":""
               }
    data_dict_list=[]
    for row in range(len(data)):
        new_occur_time=""
        if random.random()>0.5:
           new_occur_time =data[row][3]-timedelta(days=7)
        else:
            new_occur_time=data[row][3]
        data_dict["id"]=data[row][0]
        data_dict["events"]=data[row][1]
        data_dict["category"]=data[row][2]
        data_dict["name"]=data[row][4]
        data_dict["phone"]=str(data[row][5])
        data_dict["occur_time"]=new_occur_time.strftime("%Y-%m-%d %H:%M:%S")
        data_dict["solve_time"]=data[row][6].strftime("%Y-%m-%d %H:%M:%S")
        data_dict["address"]=data[row][7]
        data_dict["longitude"]=str(data[row][8])
        data_dict["latitude"]=str(data[row][9])
        data_dict["geom"]=data[row][10]
        example=data_dict.copy()
        data_dict_list.append(example)
    json.dump(data_dict_list,file,indent=4,ensure_ascii=False)
    file.close()
if __name__=="__main__":
    postgre_connect = psycopg2.connect(
        database="work12345", 
        user="postgres", 
        password="Lvu123123",
        host="localhost",
        port="5432")
    cursor = postgre_connect.cursor()
    sql='''
        select id,events,category,occur_time,person_name,person_phone,etl_times,
        sum_12345_address.address,longitude,latitude,ST_AsText(geom) as geom
        from person_event left join sum_12345_address on sum_12345_address.id=person_event.keyid where ST_AsText(geom)<>'' 
        '''
    cursor.execute(sql) 
    data=cursor.fetchall()
    write_mock(data)

    cursor.close()  # 关闭游标
    postgre_connect.close()  # 关闭数据库