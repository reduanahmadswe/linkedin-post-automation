import requests

class GeminiProvider:
    def generate(self, prompt, api_key):
        url = "https://generativeai.googleapis.com/v1/models/gemini-pro:generateContent"
        headers = {"Authorization": f"Bearer {api_key}"}
        data = {"prompt": prompt}
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            return response.json().get("content")
        else:
            print(f"Gemini API response: {response.text}")
            raise Exception("Gemini API failed")
