from agent.prompts import sub_agent_prompt
from tools.ragflow_tools import get_assistant_list,ask_question

knowledge_sub_agent = {
    'name':sub_agent_prompt['ragflow']['name'],
    'description':sub_agent_prompt['ragflow']['description'],
    'system_prompt':sub_agent_prompt['ragflow']['system_prompt'],
    'tools':[get_assistant_list,ask_question],
}
