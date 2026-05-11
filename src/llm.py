from openai import OpenAI


class DeepSeekClient:
    """通过 OpenAI SDK 调用 DeepSeek API（DeepSeek 官方推荐方式）"""

    def __init__(self, api_key: str, base_url: str = "https://api.deepseek.com", model: str = "deepseek-v4-flash"):
        self.model = model
        self.client = OpenAI(api_key=api_key, base_url=base_url)

    def generate(self, prompt: str, system_prompt: str) -> str:
        print(">>> 调用 DeepSeek...")
        try:
            resp = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                stream=False,
            )
            return resp.choices[0].message.content
        except Exception as e:
            return f"错误：调用 DeepSeek API 失败 - {e}"
