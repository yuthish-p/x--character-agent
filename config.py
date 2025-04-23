import os
from dotenv import load_dotenv

load_dotenv(override=True)

#TODO: need to change to database
class Config:
    
    
    # Twitter Config
    TWITTER_CONSUMER_API_KEY = os.getenv("TWITTER_CONSUMER_API_KEY")
    TWITTER_CONSUMER_API_SECRET = os.getenv("TWITTER_CONSUMER_API_SECRET")
    TWITTER_ACCESS_TOKEN = os.getenv("TWITTER_ACCESS_TOKEN")
    TWITTER_ACCESS_SECRET = os.getenv("TWITTER_ACCESS_SECRET")
    TWITTER_POST_INTERVAL = int(os.getenv("TWITTER_POST_INTERVAL", 60))
    
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET")
    
    TWITTER_CLIENT_ID=os.getenv("TWITTER_CLIENT_ID")
    TWITTER_CLIENT_SECRET=os.getenv("TWITTER_CLIENT_SECRET")
    
    TWITTER_BEARER_TOKEN=os.getenv("TWITTER_BEARER_TOKEN")
    TWITTER_REDIRECT_URI=os.getenv("TWITTER_REDIRECT_URI")
    # REQUIRED_KEYS = [TWITTER_API_KEY, TWITTER_API_SECRET, TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET]
    # if any(key is None for key in REQUIRED_KEYS):
    #     raise ValueError("Missing Twitter API credentials. Please check your .env file.")

    # Telegram Config
    TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
    TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
    TELEGRAM_POST_INTERVAL = int(os.getenv("TELEGRAM_POST_INTERVAL", 90))

    # Instagram Config
    INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
    INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")
    INSTAGRAM_POST_INTERVAL = int(os.getenv("INSTAGRAM_POST_INTERVAL", 120))
    
    # AI Config
    USE_OPENAI = os.getenv("USE_OPENAI", "True").lower() == "true"
    USE_GOOGLE = os.getenv("USE_GOOGLE", "False").lower() == "true"
    
    #Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
    
    
    #Models
    OPENAI_MODEL = os.getenv("OPENAI_MODEL")
    GOOGLE_MODEL = os.getenv("GOOGLE_MODEL")
    
    
    #plugins config
    
    #plugins keys
    COOKIE_API = os.getenv("COOKIE_API")
    NEWS_API = os.getenv("NEWS_API")
    WEATHER_API = os.getenv("WEATHER_API")
    
    #cookie
    COOKIE_TWITTER_TRAGET = os.getenv("COOKIE_TWITTER_TRAGET", "username")  
    COOKIE_TRAGET_TWITTER_AGENT = os.getenv("COOKIE_TRAGET_TWITTER_AGENT", "")
    COOKIE_TRAGET_TWITTER_CONTRACT_ADDRESS = os.getenv("COOKIE_TRAGET_TWITTER_CONTRACT_ADDRESS", "")
    COOKIE_TRAGET_TWITTER_INTERVAL = os.getenv("COOKIE_TRAGET_TWITTER_INTERVAL", "_3Days")

    