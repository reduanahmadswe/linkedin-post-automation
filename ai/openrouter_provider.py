import requests

class OpenRouterProvider:
    def generate(self, prompt, api_key):
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
        data = {
            "model": "openai/gpt-3.5-turbo",
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 512
        }
        response = requests.post(url, headers=headers, json=data)
        try:
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                print(f"OpenRouter API response: {response.text}")
                raise Exception("OpenRouter API failed")
        except Exception as e:
            print(f"OpenRouter API decode error: {response.text}")
            raise e
