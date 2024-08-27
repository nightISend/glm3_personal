import mysql.connector
from transformers import AutoTokenizer, AutoModel
import requests

#获取位置信息
#test:string
def getAddressByModel(test):
    address=""
    #query语句不能用json格式写，添加一段历史记录后输出变得相对稳定
    text_query="任务:从给出的文本中提取位置信息，如地址，地点，单位名称，企业名称等（如果没有发现位置信息则返回无位置信息）。\n文本："+test
    # 如果没有位置会输出"位置信息：无"
    text_system_info=[
        {
            "role": "user",
            "content":  '''任务：从给出的文本中提取位置信息，如地址，地点，单位名称，企业名称等（如果没有发现位置信息则返回无位置信息）\n文本:来电人反映海宁长安镇小区垃圾没人处理。'''
        },
        {
            "role": "assistant",
            "metadata": "",
            "content": "位置信息:海宁长安镇小区"
        }
    ]
    response, history = model.chat(tokenizer, text_query, history=text_system_info,temperature=0.8,top_p=0.5)
    response=response.replace("。","")
    print("respone="+response)
    if response[0:4]=="位置信息":
        address=response[5:]
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
    mysql_connect=mysql.connector.connect(
        host="localhost",  # MySQL服务器地址
        user="root",   # 用户名
        password="Lvu123123",  # 密码
        database="graduate_project"  # 数据库名称
    )

    cursor = mysql_connect.cursor()
    cursor.execute("select id,nr from shzl_12345")
    result=cursor.fetchall()
    count=0
    for row in result:
        address=getAddressByModel(row[1])
        coordinate=getCoordinate(address)
        sql=''
        if address=="无" or type(getCoordinate(address))==str:
            sql=f'INSERT INTO address (textId, address) VALUES (\'{row[0]}\',\'{address}\')'
        else :
            #逆天MySQL把4326坐标系的经纬度顺序弄反了
            wkt=f'ST_GeomFromText(\'point({coordinate[1]} {coordinate[0]})\',4326)'
            sql=f'INSERT INTO address (textId, address, longitude, latitude, geom) VALUES (\'{row[0]}\',\'{address}\',\'{coordinate[0]}\',\'{coordinate[1]}\',{wkt})'
        cursor.execute(sql)
        mysql_connect.commit()
        count=count+1
        print(f"添加了{count}条数据")
            
