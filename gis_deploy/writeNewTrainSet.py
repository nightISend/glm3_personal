import pandas as pd
import json

file=open("newdata_set.json",'w',encoding="utf-8")
data_dict={"instruction":"","input":"","output":""}
data_dict_list=[]
data=pd.read_excel("F:/Repo/资料备份/毕设/数据库数据/数据.xlsx",sheet_name="未训练提取（有历史记录，全）",keep_default_na=False)
i=0
for index, row in data.iterrows():
    i=i+1
    if i>1000:
        break
    respone={
            '位置':'',
            '目的':'',
            '类别':''
            }
    isgetaddress=row['是否正确提取地址']
    isgettime=row['是否正确提取内部时间']
    category=row['category']
    goal=row['goal']
    address=row['address']
    events=row['events']
    
    if isgetaddress  ==True:
        respone['位置']=address
        respone['目的']=goal
        respone['类别']=category
        content='''你是一个信息提取模型，你的任务是提取下列文本中提到的具体的事件发生地、并判断文本内容的目的和类型，并以JSON的形式返回结果。
            返回的内容中只有位置、目的和类别3个属性，其中位置从文本中提取（若没有提到位置则返回无，且位置应尽可能详细），目的和类别由你从下列的选项中选取。
            目的限定两个类别:[反映、咨询]，类别限定10个类别:[安全监管类、公安政法类、公用事业类、建设交通类、经济综合类、科教文卫类、其他类、社会管理类、社会团体类、数字城管]。
            样例1:
            输入:来电人反映2023年5月在海宁市思潮健身办的2年健身卡，具体消费详情需要核实，更换健身房名字后倒闭了，咨询如何处理。
            输出:{
            "位置":"海宁市思潮健身办",
            "目的":"咨询",
            "类别":"经济综合类"
            }
            样例2:
            输入:市民来电反映：关于临春二路一巷红沙隧道口“临春棚改办门口”对面有一条高压电线距离地面1米的问题，未处理好。
            输出:{
            "位置":"临春二路一巷红沙隧道口",
            "目的":"反映",
            "类别":"建设交通类"
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