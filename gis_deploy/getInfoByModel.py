from transformers import AutoTokenizer, AutoModel
import requests
import psycopg2 
import pandas as pd
import json
from faker import Faker
import random

def getAddressByModel(test):
    text_query='''
    你是一个信息提取模型，你的任务是提取下列文本中提到的具体的事件发生地、时间、并判断文本内容的目的和类型，并以JSON的形式返回结果。
    返回的内容中只有位置、时间、目的和类别4个属性，其中位置和时间从文本中提取（若没有提到位置和事件则返回无，且时间和位置应尽可能详细），目的和类别由你从下列的选项中选取。
    目的限定两个类别:[反映、咨询]，类别限定10个类别:[安全监管类、公安政法类、公用事业类、建设交通类、经济综合类、科教文卫类、其他类、社会管理类、社会团体类、数字城管]。
    样例1:
    输入:来电人反映2023年5月在海宁市思潮健身办的2年健身卡，具体消费详情需要核实，更换健身房名字后倒闭了，咨询如何处理。
    输出:{
    "位置":"海宁市思潮健身办",
    "时间":"2023-5",
    "目的":"咨询",
    "类别":"经济综合类"
    }
    样例2:
    输入:【欠薪】来电人跟着缪丝在浙江晶科能源有限公司工作，其反映单位拖欠工资，咨询如何处理？。
    输出:{
    "位置":"浙江晶科能源有限公司",
    "时间":"无",
    "目的":"咨询",
    "类别":"经济综合类"
    }
    文本:'''+test
    text_system_info=[
        {
            "role": "user",
            "content":  '''你是一个信息提取模型，你的任务是提取下列文本中提到的具体的事件发生地、时间、并判断文本内容的目的和类型，并以JSON的形式返回结果。
            返回的内容中只有位置、时间、目的和类别4个属性，其中位置和时间从文本中提取（若没有提到位置和事件则返回无，且时间和位置应尽可能详细），目的和类别由你从下列的选项中选取。
            目的限定两个类别:[反映、咨询]，类别限定10个类别:[安全监管类、公安政法类、公用事业类、建设交通类、经济综合类、科教文卫类、其他类、社会管理类、社会团体类、数字城管]。
            样例1:
            输入:来电人反映2023年5月在海宁市思潮健身办的2年健身卡，具体消费详情需要核实，更换健身房名字后倒闭了，咨询如何处理。
            输出:{
            "位置":"海宁市思潮健身办",
            "时间":"2023-5",
            "目的":"咨询",
            "类别":"经济综合类"
            }
            样例2:
            输入:【欠薪】来电人跟着缪丝在浙江晶科能源有限公司工作，其反映单位拖欠工资，咨询如何处理？。
            输出:{
            "位置":"浙江晶科能源有限公司",
            "时间":"无",
            "目的":"咨询",
            "类别":"经济综合类"
            }
            文本:来电人是海宁市周王庙镇石井村朱家角14号的小麦承包大户,反映其的收割机车队目前被阻拦在海宁市胡家兜收费站(G92杭州湾环线高速出口)。'''
        },
        {
            "role": "assistant",
            "metadata": "",
            "content": '''{ "位置": "海宁市胡家兜收费站(G92杭州湾环线高速出口)", "时间": "无", "目的": "咨询", "类别": "社会管理类" )'''
        },
        {
            "role": "user",
            "content":  '''你是一个信息提取模型，你的任务是提取下列文本中提到的具体的事件发生地、时间、并判断文本内容的目的和类型，并以JSON的形式返回结果。
            返回的内容中只有位置、时间、目的和类别4个属性，其中位置和时间从文本中提取（若没有提到位置和事件则返回无，且时间和位置应尽可能详细），目的和类别由你从下列的选项中选取。
            目的限定两个类别:[反映、咨询]，类别限定10个类别:[安全监管类、公安政法类、公用事业类、建设交通类、经济综合类、科教文卫类、其他类、社会管理类、社会团体类、数字城管]。
            样例1:
            输入:来电人反映2023年5月在海宁市思潮健身办的2年健身卡，具体消费详情需要核实，更换健身房名字后倒闭了，咨询如何处理。
            输出:{
            "位置":"海宁市思潮健身办",
            "时间":"2023-5",
            "目的":"咨询",
            "类别":"经济综合类"
            }
            样例2:
            输入:【欠薪】来电人跟着缪丝在浙江晶科能源有限公司工作，其反映单位拖欠工资，咨询如何处理？。
            输出:{
            "位置":"浙江晶科能源有限公司",
            "时间":"无",
            "目的":"咨询",
            "类别":"经济综合类"
            }
            文本:市民来电咨询交警支队纪检室电话'''
        },
        {
            "role": "assistant",
            "metadata": "",
            "content": '''{ "位置": "无", "时间": "无", "目的": "咨询", "类别": "其它类" }'''
        }
    ]
    response, history = model.chat(tokenizer, text_query, history=text_system_info,temperature=0.8,top_p=0.5)
    response=response.replace("'",'"')
    return response

def getCoordinate(param):
    result={}
    try:
        resp = requests.get(f"https://restapi.amap.com/v3/geocode/geo?address={param}&key=956f5653d5d99017638564a45d08acba")
        resp.raise_for_status()
        result = resp.json()
        if result['status']=='0':
            return "请求失败"
        else:
            for row in result['geocodes']:
                if row['city']!='三亚市':
                    continue
                else:
                    if row['level']!='区县':
                        return row['location'].split(',')
                    else:
                        return '获取坐标失败'
            return '获取坐标失败'
    except:
        result="请求错误"

if __name__=="__main__":
    tokenizer = AutoTokenizer.from_pretrained("E:\glm3_personal\model\chatglm3-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("E:\glm3_personal\model\chatglm3-6b", trust_remote_code=True).quantize(4).cuda()
    model = model.eval()
    postgre_connect = psycopg2.connect(
        database="work12345", 
        user="postgres", 
        password="Lvu123123",
        host="localhost",
        port="5432")
    cursor = postgre_connect.cursor()
    f=Faker(locale='zh_CN')
    i=0
    data=pd.read_excel("F:/Repo/资料备份/毕设/数据库数据/sanya12345_dataset.xlsx",sheet_name="sanya12345_dataset",keep_default_na=False)
    for index, row in data.iterrows():
        i=i+1
        if i>100:
            break
        events=row['工单内容']
        result=getAddressByModel(events) 
        i=i+1
        address=''
        time=''
        goal=''
        category=''
        sql=''
        try:
            result=json.loads(result)
            address=result['位置']
            time=str(result['时间'])
            goal=result['目的']
            category=result['类别']
        except:
            print(f"{row['order']}返回格式不对")
            continue

        try:
            coordinate=getCoordinate(address)
            if type(coordinate) !=str:
                wkt=f'ST_GeomFromText(\'point({coordinate[0]} {coordinate[1]})\',4326)'
                sql=f'''
                        INSERT INTO public.sum_12345_test(
                        id, events, category, name, phone, occur_time, solve_time, innertime,  goal, address, longitude, latitude, geom)
                        VALUES (\'{row['order']}\', \'{row['工单内容']}\', \'{category}\', \'{f.last_name()+random.choice(['女士','先生'])}\', \'{f.phone_number()}\', \'{str(row['来电时间'])}\', \'{str(row['处理时间'])}\', \'{time}\', \'{goal}\', \'{address}\', {coordinate[0]}, {coordinate[1]}, {wkt});
                    '''
            else:
                sql=f'''
                        INSERT INTO public.sum_12345_test(
                        id, events, category, name, phone, occur_time, solve_time, innertime,  goal, address)
                        VALUES (\'{row['order']}\', \'{row['工单内容']}\', \'{category}\', \'{f.last_name()+random.choice(['女士','先生'])}\', \'{f.phone_number()}\', \'{str(row['来电时间'])}\', \'{str(row['处理时间'])}\', \'{time}\', \'{goal}\', \'{address}\');
                    '''
            cursor.execute(sql)
        except Exception as e:
            print(f"{row['order']}sql报错")
            print(e)
            print(sql)
        postgre_connect.commit()
        print(f"添加{i}条数据")        
    cursor.close()  # 关闭游标
    postgre_connect.close()  # 关闭数据库
