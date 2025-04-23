import openai
import requests
from config import Config
from utils.logger import logger

class AIGenerator:
    def __init__(self,sys_context=""):
        self.use_openai = Config.USE_OPENAI
        self.use_google = Config.USE_GOOGLE
        self.sys_context = sys_context

    #TODO:nedd to change to  pattern and make dynamic
    def get_context(self):

        if self.use_openai:
            return self._openai(self.sys_context)
        elif self.use_google:
            return self._google(self.sys_context)
        else:
            logger.error("No AI model selected.")
            return None

    def _openai(self, prompt):
        
        try:
            openai.api_key = Config.OPENAI_API_KEY
            response = openai.ChatCompletion.create(
                model=Config.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}]
            )
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return None
        
    def _google(self, prompt):
        try:
            url = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateText"
            headers = {"Content-Type": "application/json"}
            payload = {"prompt": {"text": prompt}, "temperature": 0.7}
            response = requests.post(url, headers=headers, json=payload, params={"key": Config.GOOGLE_API_KEY})
            return response.json().get("candidates", [{}])[0].get("output", "")
        except Exception as e:
            logger.error(f"Google Gemini API error: {e}")
            return None