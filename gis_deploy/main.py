from transformers import AutoTokenizer, AutoModel
from tool_registry import dispatch_tool, get_tools
import json

tokenizer = AutoTokenizer.from_pretrained("D:\ChatGLM3\model\chatglm3-6b", trust_remote_code=True)
model = AutoModel.from_pretrained("D:\ChatGLM3\model\chatglm3-6b", trust_remote_code=True).quantize(4).cuda()
model = model.eval()

#添加对工具的描述，之后模型会根据问题选取合适的工具
tools = [
    {
        "name": "get_location",
        "description": "获取给定地址的经纬度坐标",
        "parameters": {
            "type": "object",
            "properties": {
                "address": {
                    "description": "需要地址"
                }
            },
            "required": ['address']
        }
    }
]
query='''
{
 "任务":"获取地址的经纬度坐标"
 "地址":"海宁市海昌街道洛隆路271号九方驾校"	
}
'''
# 提示词告诉模型可以从tool中选取需要的工具
system_info = {
"role": "system", 
"content": "Answer the following questions as best as you can. You have access to the following tools:",
"tools": tools
}

role="user"
history=[system_info]
# 第一次输入问题让模型自己选择需要的工具并设置参数
response, history = model.chat(tokenizer, query, history=history,role=role)
# 使用dispatch_tool方法调用对应的工具并将输出的python编码调整为json字符串
result = json.dumps(dispatch_tool(response['name'],response['parameters']), ensure_ascii=False)
# 将工具返回的结果重新输入给模型得到输出,注意role必须是observation
response, history = model.chat(tokenizer, result, history=history, role="observation")

print(response)