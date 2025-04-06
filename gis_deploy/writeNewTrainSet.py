import pandas as pd
import json

file=open("newdata_set.json",'w',encoding="utf-8")
data_dict={"instruction":"","input":"","output":""}
data_dict_list=[]
data=pd.read_excel("F:/Repo/资料备份/毕设/数据库数据/数据.xlsx",sheet_name="未训练提取（有历史记录，全）",keep_default_na=False)
i=0
for index, row in data.iterrows():
    i=i+1
    if i>100:
        break
    respone={
            '位置':'',
            '时间':'',
            '目的':'',
            '类别':''
            }
    isgetaddress=row['是否正确提取地址']
    isgettime=row['是否正确提取内部时间']
    time=row['innertime']
    category=row['category']
    goal=row['goal']
    address=row['address']
    events=row['events']

    if isgetaddress  ==True and isgettime==True:
        respone['位置']=address
        respone['时间']=str(time)
        respone['目的']=goal
        respone['类别']=category
        content='''你是一个信息提取模型，你的任务是提取下列文本中提到的具体的事件发生地、时间、并判断文本内容的目的和类型，并以JSON的形式返回结果。
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
            文本:'''+events
        data_dict["input"]=content
        data_dict["output"]=json.dumps(respone, indent=4, ensure_ascii=False)
        example=data_dict.copy()
        # 先把所有字典存在列表里再写出json文件，出来才会是以字典为内容的列表,否则是多个字典的组合且字典间没有逗号
        data_dict_list.append(example)
    else:
        continue
json.dump(data_dict_list,file,indent=4,ensure_ascii=False)
file.close()