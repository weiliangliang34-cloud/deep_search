# 创建网络搜索子智能体
# 方式1 dict 方式2 compiledSubAgent(langgraph和langchain兼容的方式)

from agent.prompts import sub_agent_prompt
from tools.tavily_tool import internet_search

network_search_agent = {
    "name":sub_agent_prompt['tavily']['name'],
    'description':sub_agent_prompt['tavily']['description'],
    'system_prompt':sub_agent_prompt['tavily']['system_prompt'],
    'tools':[internet_search]
}

