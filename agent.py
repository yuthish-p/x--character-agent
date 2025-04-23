import asyncio

from plugins.CookiePlugin import CookiePlugin
from bot.TwitterClient import TwitterClient 
from config import Config
from ai.prompt_generator import PromptGenerator
from ai.ai_generator import AIGenerator
import json
import os

#TODO: change to database
def load_character_json(character_name):
    
    
    
    json_filename = f"{character_name}.character.json"
    script_directory = os.path.dirname(os.path.abspath(__file__))
    character_json_path = os.path.join(script_directory, f"characters/{json_filename}")

    

    try:
        with open(character_json_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Character JSON file not found at {character_json_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}")
        return None

def trim_quotes(s):
    if s.startswith('"') and s.endswith('"'):
        return s[1:-1]
    return s


async def main():
    
    
    character_data = load_character_json("aylin")
    
    #TODO: need to change dynic plugin use Strategy pattern 
    
    target_type = Config.COOKIE_TWITTER_TRAGET 
    plugin = CookiePlugin(target_type=target_type)
    plugin_context = plugin.get_prompt()
    
    Prompt_engine = PromptGenerator(character_data=character_data,real_time_data=plugin_context)
    sys_context = Prompt_engine.generate_prompt()
    
    print(sys_context)
    ai_engine = AIGenerator(sys_context=sys_context)
    post = ai_engine.get_context()
    print(trim_quotes(post))
    # bot = TwitterClient()
    # print(bot.post_tweet(trim_quotes(post)))


if __name__ == "__main__":
    asyncio.run(main())

