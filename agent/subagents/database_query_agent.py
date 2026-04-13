from agent.prompts import sub_agent_prompt
from tools.db_tools import list_sql_tables,get_table_data,execute_sql_query

database_query_agent = {
    "name":sub_agent_prompt['db']['name'],
    "description":sub_agent_prompt['db']['description'],
    "system_prompt":sub_agent_prompt['db']['system_prompt'],
    "tools":[list_sql_tables,get_table_data,execute_sql_query]
}