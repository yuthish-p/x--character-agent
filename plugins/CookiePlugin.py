import requests
from config import Config
import os

class CookiePlugin:
    def __init__(self, target_type="twitterUsername"):
        self.api_key = Config.COOKIE_API
        self.base_url = "https://api.cookie.fun/v2/agents"
        self.headers = {"x-api-key": self.api_key}
        self.target_type = target_type if target_type in ["twitterUsername", "contractAddress"] else "twitterUsername"
        self.selected_agents = set()
    
    def read_selected_agents(self, filename="selected_agents.txt"):
        if os.path.exists(filename):
            with open(filename, "r") as file:
                return set(line.strip() for line in file)
        return set()

    def write_selected_agent(self, agent_name, filename="selected_agents.txt"):
        with open(filename, "a") as file:
            file.write(f"{agent_name}\n")

    def getRandomAgent(self):
        try:
            # Start by getting the first page
            page = 1
            while True:
                url = f"{self.base_url}/agentsPaged?interval=_7Days&page={page}&pageSize=10"
                response = requests.get(url, headers=self.headers)
                response.raise_for_status()  
                data = response.json()

                # Check if 'ok' data exists in the response
                agents_data = data.get("ok", {}).get("data", [])
                if not agents_data:
                    return {"error": "No agent data found."}

                # Check for already selected agents
                selected_agents = self.read_selected_agents()

                for agent in agents_data:
                    twitter_usernames = agent.get("twitterUsernames", [])
                    # Try to get the first non-empty twitter username
                    agent_name = None
                    for username in twitter_usernames:
                        if username and username not in selected_agents:
                            agent_name = username
                            break
                    
                    # If a valid agent name is found
                    if agent_name:
                        # Write the selected agent to the file
                        self.write_selected_agent(agent_name)
                        return agent_name

                # If no valid agent was found, move to the next page
                page += 1

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch data from Cookie API: {str(e)}"}

    def get_prompt(self):
        try:
            agent_name = self.getRandomAgent()
            if isinstance(agent_name, dict) and "error" in agent_name:
                return agent_name

            target_map = {
                "twitterUsername": agent_name,
                "contractAddress": Config.COOKIE_TRAGET_TWITTER_CONTRACT_ADDRESS if hasattr(Config, "COOKIE_TRAGET_TWITTER_CONTRACT_ADDRESS") else None
            }
            
            target_value = target_map.get(self.target_type, None)

            if not target_value:
                return {"error": f"Invalid target value for {self.target_type}."}

            url = f"{self.base_url}/{self.target_type}/{target_value}?interval={Config.COOKIE_TRAGET_TWITTER_INTERVAL}"
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()  
            data = response.json()

            filtered_data = self.process_data(data)

            if "error" in filtered_data:
                return filtered_data
            
            return self.generate_prompt(agent_name, filtered_data)

        except requests.exceptions.RequestException as e:
            return {"error": f"Failed to fetch data from Cookie API: {str(e)}"}

    def process_data(self, response):
        try:
            if not response.get("success"):
                return {"error": "Invalid API response"}

            data = response.get("ok", {})

            return {
                "mindshare": data.get("mindshare"),
                "mindshareDeltaPercent": data.get("mindshareDeltaPercent"),
                "marketCap": data.get("marketCap"),
                "marketCapDeltaPercent": data.get("marketCapDeltaPercent"),
                "price": data.get("price"),
                "priceDeltaPercent": data.get("priceDeltaPercent"),
                "liquidity": data.get("liquidity"),
                "volume24Hours": data.get("volume24Hours"),
                "volume24HoursDeltaPercent": data.get("volume24HoursDeltaPercent"),
                "holdersCount": data.get("holdersCount"),
                "holdersCountDeltaPercent": data.get("holdersCountDeltaPercent"),
                "averageImpressionsCount": data.get("averageImpressionsCount"),
                "averageImpressionsCountDeltaPercent": data.get("averageImpressionsCountDeltaPercent"),
                "averageEngagementsCount": data.get("averageEngagementsCount"),
                "averageEngagementsCountDeltaPercent": data.get("averageEngagementsCountDeltaPercent"),
                "followersCount": data.get("followersCount"),
                "smartFollowersCount": data.get("smartFollowersCount"),
            }

        except KeyError:
            return {"error": "Failed to parse API response"}

    def generate_prompt(self, agent_name, data):

        if not data:
            return "Provide a crypto market update using the latest trends."

        prompt_parts = [
            f"Agent Name: {agent_name}",
            f"Market Cap: ${data.get('marketCap', 0):,.2f} (Change: {data.get('marketCapDeltaPercent', 0):.2f}%)",
            f"Price: ${data.get('price', 0):,.6f} (Change: {data.get('priceDeltaPercent', 0):.2f}%)",
            f"Liquidity: ${data.get('liquidity', 0):,.2f}",
            f"24H Volume: ${data.get('volume24Hours', 0):,.2f} (Change: {data.get('volume24HoursDeltaPercent', 0):.2f}%)",
            f"Mindshare Score: {data.get('mindshare', 'N/A')} (Change: {data.get('mindshareDeltaPercent', 0):.2f}%)",
            f"Holders Count: {data.get('holdersCount', 'N/A')} (Change: {data.get('holdersCountDeltaPercent', 0):.2f}%)",
            f"Followers Count: {data.get('followersCount', 'N/A')}",
            f"Smart Followers Count: {data.get('smartFollowersCount', 'N/A')}"
        ]

        # Join all parts to form the final prompt
        prompt = "\n\n".join(str(part) for part in prompt_parts)

        return prompt
