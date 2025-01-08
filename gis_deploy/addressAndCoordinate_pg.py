# 连接postgresql
from transformers import AutoTokenizer, AutoModel
import requests
import psycopg2 

#获取位置信息
#test:string
def getAddressByModel(test):
    address=""
    #query语句不能用json格式写，添加一段历史记录后输出变得相对稳定
    text_query="任务:请从给出的关于海宁市的文本中提取事件的发生地，发生地必须是海宁市内的某个地点，不可以指海宁市这一大区域，如果没有发现位置信息则返回无位置信息。\n文本："+test
    # 如果没有位置会输出"事件发生地：无"
    text_system_info=[
        {
            "role": "user",
            "content":  '''任务:请从给出的关于海宁市的文本中提取事件的发生地，发生地必须是海宁市内的某个地点，不可以指海宁市这一大区域，如果没有发现位置信息则返回无位置信息。
            文本:来电人是海宁市周王庙镇石井村朱家角14号的小麦承包大户,反映其的收割机车队目前被阻拦在海宁市胡家兜收费站(G92杭州湾环线高速出口)。'''
        },
        {
            "role": "assistant",
            "metadata": "",
            "content": "事件发生地：海宁市胡家兜收费站(G92杭州湾环线高速出口)"
        },
        {
            "role": "user",
            "content":  '''任务:请从给出的关于海宁市的文本中提取事件的发生地，发生地必须是海宁市内的某个地点，不可以指海宁市这一大区域，如果没有发现位置信息则返回无位置信息。
            文本:来电人咨询海宁生育报销。'''
        },
        {
            "role": "assistant",
            "metadata": "",
            "content": "事件发生地：无"
        }
    ]
    response, history = model.chat(tokenizer, text_query, history=text_system_info,temperature=0.8,top_p=0.5)
    response=response.replace("。","")
    print("respone="+response)
    if response[0:5]=="事件发生地":
        address=response[6:]
    else:
        address="无"
    return address

# 如果返回的是字符串则是报错，否则是请求的返回
# 获取坐标
#param:str
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
                if row['district']!='海宁市':
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
    tokenizer = AutoTokenizer.from_pretrained("D:\ChatGLM3\model\chatglm3-6b", trust_remote_code=True)
    model = AutoModel.from_pretrained("D:\ChatGLM3\model\chatglm3-6b", trust_remote_code=True).quantize(4).cuda()
    model = model.eval()
    postgre_connect = psycopg2.connect(
        database="work12345", 
        user="postgres", 
        password="Lvu123123",
        host="localhost",
        port="5432")

    cursor = postgre_connect.cursor()
    cursor.execute("select id,events from train_12345") #查询数据表
    result=cursor.fetchall()
    count=0
    for row in result:
        address=getAddressByModel(row[1])
        coordinate=getCoordinate(address)
        sql=''
        if_success=""

        if address=="无" or type(coordinate)==str: #如果没有地址或者高德找不到地址会返回字符串，否则坐标数组
            if_success="true"
            sql=f'INSERT INTO train_12345_address_pre1 (id, address,if_success) VALUES (\'{row[0]}\',\'{address}\',{if_success})'
        else :
            # 判断获取到的坐标的格式是否正确
            try:
                longitude=coordinate[0]
                latitude=coordinate[1]
            except:
                if_success="false"
                sql=f'INSERT INTO train_12345_address_pre1 (id,if_success) VALUES (\'{row[0]}\',{if_success})'
            else:
                if_success="true"
                wkt=f'ST_GeomFromText(\'point({coordinate[0]} {coordinate[1]})\',4326)'
                sql=f'INSERT INTO train_12345_address_pre1 (id, address, longitude, latitude, geom,if_success) VALUES (\'{row[0]}\',\'{address}\',\'{coordinate[0]}\',\'{coordinate[1]}\',{wkt},{if_success})'
        
        try:
            cursor.execute(sql)
        except:
            postgre_connect.commit() # 在操作报错后先提交操作,避免后面的操作无法执行
            if_success="false"
            cursor.execute(f'INSERT INTO train_12345_address_pre1 (id,if_success) VALUES (\'{row[0]}\',{if_success})')
            print(f"{row[0]} 格式错误")

        postgre_connect.commit()
        count=count+1
        print(f"添加了{count}条数据")

    cursor.close()  # 关闭游标
    postgre_connect.close()  # 关闭数据库