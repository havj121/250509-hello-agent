# 250509-hello-agent

## 目标
复现 Datawhale《Hello Agents》第 1.3 节的 ReAct 智能体（旅行助手），将 LLM 接入层替换为 DeepSeek 官方 SDK，保留工具层 API key 接口。

## 方法
- **架构**：ReAct（Thought-Action-Observation）循环
- **LLM**：DeepSeek（通过 OpenAI SDK 接入，官方推荐方式）
- **工具**：
  - `get_weather` — wttr.in 免费 API，无需 key
  - `get_attraction` — Tavily Search API，需 `TAVILY_API_KEY`（可选，未配置时降级为静态提示）
- **流程**：LLM 生成 Thought + Action → 解析 Action 并执行工具 → Observation 追加到上下文 → 循环直到输出 finish

## 快速开始

```bash
# 1. 安装依赖
pip install -r requirements.txt

# 2. 配置环境变量
cp .env.example .env
# 编辑 .env，填入 DEEPSEEK_API_KEY（必填）和 TAVILY_API_KEY（可选）

# 3. 运行
python main.py
```

## 文件结构

```
250509-hello-agent/
├── main.py              # 入口
├── src/
│   ├── config.py        # 环境变量配置
│   ├── llm.py           # DeepSeek LLM 客户端
│   ├── tools.py         # 工具函数定义
│   └── agent.py         # ReAct 主循环 + 系统提示词
├── requirements.txt
├── .env.example
└── README.md
```

## 示例

```
请输入你的旅行需求: 今天上海天气怎么样？适合去哪里玩？

--- 第 1 轮 ---
>>> 调用 DeepSeek...
Thought: 首先查询上海今天的天气。
Action: get_weather(city="上海")

Observation: 上海当前天气：Sunny，气温22摄氏度

--- 第 2 轮 ---
>>> 调用 DeepSeek...
Thought: 天气晴朗，接下来推荐景点。
Action: get_attraction(city="上海", weather="Sunny")

Observation: 推荐：外滩、迪士尼、豫园...

--- 第 3 轮 ---
>>> 调用 DeepSeek...
Thought: 已获取足够信息。
Action: finish(answer="上海今天晴朗22°C，推荐去外滩散步或迪士尼乐园...")
```

## 关键设计

- **LLM 层**：使用 `openai` 包 + `base_url="https://api.deepseek.com"`，这是 DeepSeek 官方推荐的 Python SDK 接入方式
- **API key 接口保留**：Tavily 的 Key 从环境变量读取，留出了「其他服务 API key」的扩展接口
- **无 Key 降级**：`get_attraction` 在未配置 Tavily Key 时自动降级为静态提示，不报错

## 结论
验证了 ReAct 模式的智能体可以快速搭建，DeepSeek 的 OpenAI 兼容接口支持函数调用格式良好。后续可扩展更多工具和记忆机制。

## 状态
[ ] 进行中 / [x] 已完成 / [-] 已废弃
