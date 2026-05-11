import re

from .tools import AVAILABLE_TOOLS, TOOL_DESCRIPTIONS

SYSTEM_PROMPT = f"""你是一个智能旅行助手。你的任务是分析用户的请求，并使用可用工具一步步地解决问题。

# 可用工具:
{TOOL_DESCRIPTIONS}

# 行动格式:
你的回答必须严格遵循以下格式。首先是你的思考过程，然后是你要执行的具体行动。
Thought: [这里是你的思考过程和下一步计划]
Action: [这里是你要调用的工具，格式为 function_name(arg_name="arg_value")]

# 任务完成:
当你收集到足够的信息，能够回答用户的最终问题时，你必须使用 `finish(answer="...")` 来输出最终答案。

请开始！"""


def parse_action(text: str):
    """从模型输出中解析 Action 行"""
    m = re.search(r"Action:\s*(.+)", text, re.DOTALL)
    if not m:
        return None
    return m.group(1).strip()


def parse_kwargs(action_str: str):
    """解析 Action 字符串中的工具名和参数"""
    tool_name = re.search(r"(\w+)\(", action_str).group(1)
    args_part = re.search(r"\((.*)\)", action_str, re.DOTALL).group(1)
    kwargs = dict(re.findall(r'(\w+)="([^"]*)"', args_part))
    return tool_name, kwargs


def run_agent(user_input: str, llm, tavily_api_key: str = "", max_rounds: int = 5):
    """ReAct 主循环"""
    history = [f"用户请求: {user_input}"]
    print(f"用户输入: {user_input}\n" + "=" * 40)

    for turn in range(max_rounds):
        print(f"\n--- 第 {turn + 1} 轮 ---\n")
        full_prompt = "\n".join(history)

        output = llm.generate(full_prompt, SYSTEM_PROMPT)
        print(f"模型输出:\n{output}\n")
        history.append(output)

        action_str = parse_action(output)
        if not action_str:
            print("模型输出中未找到 Action，结束。")
            break
        else:
            print(f"动作解析结果: {action_str}")

        # finish → 输出最终答案
        if action_str.startswith("finish"):
            m = re.search(r'finish\(answer="(.*)"\)', action_str, re.DOTALL)
            if m:
                print(f"任务完成！最终答案:\n{m.group(1)}")
            break

        # 解析工具调用
        try:
            tool_name, kwargs = parse_kwargs(action_str)
        except (AttributeError, IndexError):
            print(f"解析 Action 失败: {action_str}")
            break

        if tool_name not in AVAILABLE_TOOLS:
            observation = f"错误：未定义的工具 '{tool_name}'"
        else:
            fn = AVAILABLE_TOOLS[tool_name]
            # get_attraction 需要额外传入 tavily_api_key
            if tool_name == "get_attraction":
                observation = fn(**kwargs, tavily_api_key=tavily_api_key)
            else:
                observation = fn(**kwargs)

        obs_line = f"Observation: {observation}"
        print(f"{obs_line}\n" + "=" * 40)
        history.append(obs_line)
