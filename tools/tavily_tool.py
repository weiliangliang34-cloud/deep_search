import os
from typing import Literal

from dotenv import load_dotenv
from langchain_core.tools import tool
from tavily import TavilyClient

from api.monitor import monitor

load_dotenv()

tavily_client = TavilyClient(api_key=os.getenv("TAILY_API_KEY"))

# 定义网络搜索工具
@tool
def internet_search(
        query:str,
        topic:Literal['news','finance','general'] = 'news',
        max_results:int = 10,
        include_raw_content:bool = False,
):
    """
    根据用户问题,进行网络信息搜索
    注意,主要搜索公开的网络信息,如果指定查询数据库或者rag不能使用此工具!
    :param query: 用户的查询信息
    :param topic: 查询的类型
    :param max_results: 返回的最大条数
    :param include_raw_content:  是否返回原内容,False精简True详细
    :return:
    """
    # 监控埋点,每次调用这个工具,都会向前端推进调用进度
    monitor.report_tool(tool_name='网络搜索工具',
                        args={
                            'query':query,
                            'topic':topic,
                            'max_results':max_results,
                            'include_raw_content':include_raw_content
                        })
    return tavily_client.search(query=query, topic=topic, max_results=max_results, include_raw_content=include_raw_content)
