# 加载yml数据

import yaml
from pathlib import Path

# 定义加载函数
def load_yaml(path):
    with open(path,'r',encoding='utf-8') as f:
        return yaml.safe_load(f)


root_path = Path(__file__).parents[1]
yaml_path = root_path / "prompt" /"prompts.yml"

prompt_yaml_content = load_yaml(yaml_path)

main_agent_prompt = prompt_yaml_content["main_agent"]
sub_agent_prompt = prompt_yaml_content["sub_agents"]