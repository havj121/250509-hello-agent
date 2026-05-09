"""智能体入口：ReAct 旅行助手"""

from src.config import load_config
from src.llm import DeepSeekClient
from src.agent import run_agent


def main():
    cfg = load_config()

    if not cfg["deepseek_api_key"]:
        print("错误：请在 .env 文件中配置 DEEPSEEK_API_KEY")
        return

    llm = DeepSeekClient(
        api_key=cfg["deepseek_api_key"],
        base_url=cfg["deepseek_base_url"],
        model=cfg["deepseek_model"],
    )

    print("=" * 50)
    print("  智能旅行助手 v1.0")
    print("=" * 50)
    print()

    prompt = input("请输入你的旅行需求: ").strip()
    if not prompt:
        prompt = "你好，请帮我查询一下今天北京的天气，然后根据天气推荐一个合适的旅游景点。"

    run_agent(prompt, llm, tavily_api_key=cfg.get("tavily_api_key", ""))


if __name__ == "__main__":
    main()
