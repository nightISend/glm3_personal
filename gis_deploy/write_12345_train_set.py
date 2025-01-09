import pandas as pd
import json
def write_set(data):
    # 标注utf-8否则乱码
    file=open("data_set.json",'w',encoding="utf-8")
    content="任务:请从给出的关于海宁市的文本中提取事件的发生地，发生地必须是海宁市内的某个地点，不可以指海宁市这一大区域，如果没有发现位置信息则返回无位置信息。"
    data_dict={"instruction":content,"input":"","output":""}
    data_dict_list=[]
    for row in range(len(data)):
        true_address=data.loc[row,'true_address']
        events=data.loc[row,'events']
        data_dict["input"]="文本:"+events
        data_dict["output"]="事件发生地:"+true_address
        # 字典是指针，前面存入的字段与后面的字典是相同的地址
        example=data_dict.copy()
        # 先把所有字典存在列表里再写出json文件，出来才会是以字典为内容的列表,否则是多个字典的组合且字典间没有逗号
        data_dict_list.append(example)
    json.dump(data_dict_list,file,indent=4,ensure_ascii=False)
    file.close()

if __name__=="__main__":
    excel_path="F:\Repo\资料备份\毕设\数据库数据\提取结果统计.xlsx"
    excel_sheet_name="sum_12345_address_pre"
    data=pd.read_excel(excel_path,sheet_name=excel_sheet_name,nrows=200)
    write_set(data)
