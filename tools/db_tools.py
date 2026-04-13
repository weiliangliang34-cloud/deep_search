import os

import mysql
from dotenv import load_dotenv
from langchain_core.tools import tool
from mysql.connector import Error
from sqlalchemy.dialects.mysql import pymysql

from api.monitor import monitor

load_dotenv()

def get_db_config():
    config = {
        "host": os.getenv("MYSQL_HOST", "localhost"),
        "port": int(os.getenv("MYSQL_PORT", "3306")),
        "user": os.getenv("MYSQL_USER"),
        "password": os.getenv("MYSQL_PASSWORD"),
        "database": os.getenv("MYSQL_DATABASE"),
        "charset": os.getenv("MYSQL_CHARSET", "utf8mb4"),
        "collation": os.getenv("MYSQL_COLLATION", "utf8mb4_unicode_ci"),
        "autocommit": True,
        "sql_mode": os.getenv("MYSQL_SQL_MODE", "TRADITIONAL")
    }
    # 移除 None 值（核心必要操作）
    config = {k: v for k, v in config.items() if v is not None}

    # 补充：校验核心配置是否存在（可选但推荐）
    required_keys = ["user", "password", "database"]
    missing_keys = [k for k in required_keys if k not in config]
    if missing_keys:
        raise ValueError(f"缺失数据库核心配置：{', '.join(missing_keys)}")

    return config

@tool
def list_sql_tables()->str:
    """
    查询当前库中所有可用的表
    作用:为了模型识别哪些可用的表!方便进行后续的自定义sql查询
    :return: 有表:可用的表:表1,表2,表3 没有表:没有可用的表 出现异常:查询出现异常:异常信息
    """

    # 埋点
    monitor.report_tool(tool_name='数据库查询工具',args={})

    try:
        # 使用with释放连接和cursor资源
        # 创建链接
        with mysql.connector.connect(**get_db_config()) as conn:
            # 创建cursor
            with conn.cursor() as cursor:
                # cursor执行sql
                sql = 'show tables;'
                cursor.execute(sql)
                # cursor获取返回结果[(表1),(表2),(表3)
                tables = cursor.fetchall()
                if not tables:
                    return '没有可用的表'
                table_names = [table[0] for table in tables]
                return f"可用的表:{','.join(table_names)}"
    except Error as e:
        # 确保要捕捉异常信息,返回异常提示,避免直接报错
        raise f'查询出现异常{str(e)}'


@tool
def get_table_data(table_name)->str:
    """
    查询指定表名的数据！当前工具调用之前，必须先调用list_sql_tables完成表名的校验！
    此工具的作用：1.可以完成单表数据的查询 2. 可以为多表查询提供表结果信息（列名&数据格式）
    :param table_name: 表名
    :return: csv格式的数据（模拟表格数据格式）
             1.第一行是列信息，列之间使用,（英文的逗号）分割
             2.第二行开始是表数据，值之间也使用,(英文的逗号)分割
             3.行和行之间使用\n分割
             4.至多表数据查询100条
             例如：
                id,name,age\n -> 列头
                1,张三,18\n
                1,张三,18\n    -> 至多查询100条
                1,张三,18\n
                1,张三,18\n
    """
    monitor.report_tool(tool_name='根据表名查询数据', args={"table_name":table_name})
    config = get_db_config()
    try:
        with mysql.connector.connect(**config) as conn:
            with conn.cursor() as cursor:
                sql = f'select * from {table_name} limit 100;'
                cursor.execute(sql)
                description = cursor.description
                if not description:
                    return f'数据表:{table_name}没有数据'
                columns = [desc[0] for desc in  description]
                # 表数据
                rows = cursor.fetchall()
                # (1,张三,18) -> ('1','张三','18') -> ['1','张三','18']
                result = [".".join(map(str,row)) for row in rows]

                header_str = ".".join(columns)
                data_str = "\n".join(result)
                return f"{header_str}\n{data_str}"
    except Error as e:
        return f'查询表数据出现异常:{str(e)}'

@tool
def execute_sql_query(query)->str:
    """
    执行自定义查询sql语句！切记：执行之前，需要通过执行 list_sql_tables明确表名！执行get_table_data
    明确表结构和数据格式！
    :param query: 要执行的自定义sql语句
    :return: csv格式的数据（模拟表格数据格式）
             1.第一行是列信息，列之间使用,（英文的逗号）分割
             2.第二行开始是表数据，值之间也使用,(英文的逗号)分割
             3.行和行之间使用\n分割
             4.至多表数据查询100条
             例如：
                id,name,age\n -> 列头
                1,张三,18\n
                1,张三,18\n    -> 至多查询100条
                1,张三,18\n
                1,张三,18\n
    """
    monitor.report_tool(tool_name="数据库表数据查询工具：execute_sql_query", args={"query":query})

    # 获取数据库参数
    config = get_db_config()
    try:
        with mysql.connector.connect(**config) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                description = cursor.description
                if not description:
                    return f"执行自定义SQL语句查询没有结果，sql为：{query}！"
                columns = [ desc[0] for desc in description ] # [1,2,3,4]
                rows = cursor.fetchall()
                results = [ ",".join(map(str,row)) for row in rows]
                header_str = ",".join(columns)
                data_str = "\n".join(results)
                return f"{header_str}\n{data_str}"
    except Error as e:
        return f"查询出现异常：{str(e)}"
