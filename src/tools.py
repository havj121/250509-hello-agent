import requests


def get_weather(city: str) -> str:
    """查询指定城市的实时天气（无需 API Key）"""
    url = f"https://wttr.in/{city}?format=j1"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        cond = data["current_condition"][0]
        desc = cond["weatherDesc"][0]["value"]
        temp = cond["temp_C"]
        return f"{city}当前天气：{desc}，气温{temp}摄氏度"
    except requests.RequestException as e:
        return f"查询天气失败（网络错误）：{e}"
    except (KeyError, IndexError) as e:
        return f"解析天气数据失败：{e}"


def get_attraction(city: str, weather: str, tavily_api_key: str = "") -> str:
    """根据城市和天气搜索推荐景点，需要 TAVILY_API_KEY"""
    if not tavily_api_key:
        return f"（提示：未配置 TAVILY_API_KEY，无法搜索景点。建议去故宫、颐和园、长城等经典景点。）"

    from tavily import TavilyClient

    client = TavilyClient(api_key=tavily_api_key)
    query = f"'{city}' 在'{weather}'天气下最值得去的旅游景点推荐及理由"
    try:
        result = client.search(query=query, search_depth="basic", include_answer=True)
        if result.get("answer"):
            return result["answer"]
        items = [f"- {r['title']}: {r['content']}" for r in result.get("results", [])]
        return "搜索推荐如下：\n" + "\n".join(items) if items else "未找到相关推荐。"
    except Exception as e:
        return f"搜索景点时出错：{e}"


AVAILABLE_TOOLS = {
    "get_weather": get_weather,
    "get_attraction": get_attraction,
}

TOOL_DESCRIPTIONS = """- `get_weather(city: str)`: 查询指定城市的实时天气。
- `get_attraction(city: str, weather: str)`: 根据城市和天气搜索推荐的旅游景点。"""
