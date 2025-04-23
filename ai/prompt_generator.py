import random

class PromptGenerator:
    def __init__(self, character_data,real_time_data=None):

        self.character_data = character_data
        self.name = character_data.get("name", "Unknown")
        self.bio = character_data.get("bio", ["A unique personality."])[0]
        self.style = character_data.get("style", {}).get("post", ["A unique voice."])[0]
        self.tone = ", ".join(character_data.get("adjectives", ["bold", "confident"]))
        self.clients = character_data.get("clients", ["twitter"])  # List of platforms
        self.post_examples = character_data.get("postExamples", ["Crypto is wild today!"])
        self.post_length = character_data.get("postLength", "short").lower()  # short, medium, long
        self.topics = character_data.get("topics", ["Crypto market trends"])
        self.knowledge = character_data.get("knowledge", ["General crypto knowledge."])
        self.topic = random.choice(self.topics)  # Selects a random topic dynamically
        self.real_time_data = real_time_data

    def get_platform_guidelines(self, client):
        guidelines = {
            "twitter": "Make it concise and engaging.",
            "instagram": "Make it visually compelling.",
            "telegram": "Use a conversational and informative tone.",
        }
        return guidelines.get(client.lower(), "Ensure clarity and engagement.")


    def get_knowledge(self):
        return random.choice(self.knowledge) if self.knowledge else "Provide relevant insights."

    def get_post_example(self):
        return random.choice(self.post_examples) if self.post_examples else "Crypto is heating up!"

    def gen_header(self, client):
        return f"""
        You are {self.name}, a social media personality with {self.tone} traits.
        Your bio: {self.bio}
        Style: {self.style}
        Posting on {client.capitalize()}.
        Topic: {self.topic}
        """.strip()

    def gen_body(self, client):
        return f"""
        Task: Write a {client.capitalize()} post about "{self.topic}".
        - {self.get_platform_guidelines(client)}
        - Example post in {self.name}'s style: "{self.get_post_example()}"
        """.strip()
        
    

    def gen_knowledge_section(self):
        return f"""
        Use this insight in your response, keeping {self.name}'s personality in mind:
        "{self.get_knowledge()}"
        """.strip()

    def gen_footer(self, client):
        
        post_example = self.get_post_example()
        post_example_length = len(post_example)
        
        if post_example_length < 50:
            post_example_length = 80
        
        return f"""
        Craft a {self.post_length} post that sounds like {self.name}, using their personality, style, and humor.
        **utile the real time data and make your own decision and insight about the data **.
        **while genrate the post always metion the {client} clint  using @ or,# **.
        **while genrate the post use some post related emojis**.
        **post must be in the  given  {post_example_length} characters**
        The post should include **insights on price movement, market sentiment, and investor engagement**.
        Avoid hashtags and URLs. Write naturally, like a human and make simple {client} post,
        Example post: "{post_example}".
        """.strip()
        
    def generate_trending_content(self, client):

        trending_topic = random.choice(self.topics)  # Pick a trending topic
        post_example = self.get_post_example()

        platform_guidelines = {
            "twitter": f"Trending now: {trending_topic}. {post_example}",
            "instagram": f"Hot topic: {trending_topic}. Visualize this trend with an engaging post!",
            "telegram": f"Community discussion: {trending_topic}. {post_example}",
        }
        
        return platform_guidelines.get(client.lower(), f"Trending: {trending_topic}. {post_example}")

    #TODO: need to optimze the prompt generation
    def generate_prompt(self):
        
        prompts = []
        
        for client in self.clients:
            # Generate trending content if real-time data is not provided
            real_time_section = self.real_time_data if self.real_time_data else self.generate_trending_content(client)

            prompt = "\n\n".join([
                self.gen_header(client),
                self.gen_body(client),
                self.gen_knowledge_section(),
                real_time_section,
                self.gen_footer(client)
            ])
            prompts.append(prompt)

        return "\n\n---\n\n".join(prompts)  

