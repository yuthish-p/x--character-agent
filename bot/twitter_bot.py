import os
import asyncio
import pickle  # Save session data
import json
from dotenv import load_dotenv
from twikit import Client

# Load environment variables
load_dotenv()

class TwitterBot:
    _instance = None
    SESSION_FILE = "session.pkl"  # Save session to avoid repeated logins
    COOKIES_FILE = "cookies.json"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TwitterBot, cls).__new__(cls)
            cls._instance._init_client()
        return cls._instance

    def _init_client(self):
        """Initialize the Twikit Client."""
        self.client = Client('en-US')
        self.username = os.getenv("TWITTER_USERNAME")
        self.password = os.getenv("TWITTER_PASSWORD")
        self.email = os.getenv("TWITTER_EMAIL")
        self.is_logged_in = False

    async def login(self):
        """Login once and reuse session if valid cookies exist."""
        if os.path.exists(self.COOKIES_FILE):
            try:
                with open(self.COOKIES_FILE, 'r', encoding='utf-8') as f:
                    cookies = json.load(f)
                self.client.set_cookies(cookies)
                self.client.load_cookies(self.COOKIES_FILE)
                
                # Check if session is valid by making a request
                try:
                    await self.client.get_me()
                    self.is_logged_in = True
                    print("Reused existing valid session!")
                    return
                except Exception:
                    print("Session invalid, logging in again...")
            except Exception as e:
                print("Failed to load session from cookies. Logging in again...", e)

        # Fresh login if no valid session exists
        try:
            await self.client.login(
                auth_info_1=self.username,
                auth_info_2=self.email,
                password=self.password
            )
            self.is_logged_in = True
            
            self.client.get_cookies()
            self.client.save_cookies(self.COOKIES_FILE)
            print("Logged in successfully and session saved!")
        except Exception as e:
            print("Login failed:", e)
            self.is_logged_in = False

    async def tweet(self, message):
        """Post a tweet if logged in."""
        if not self.is_logged_in:
            print("Error: Not logged in. Retrying login...")
            await self.login()
            if not self.is_logged_in:
                print("Login failed. Cannot post tweet.")
                return
        try:
            await self.client.create_tweet(message)
            print("Tweet posted successfully!")
        except Exception as e:
            print("Error posting tweet:", e)
