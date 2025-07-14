# reddit_persona_builder.py

import os
import openai
import praw
from dotenv import load_dotenv
from tqdm import tqdm

# Load .env variables
load_dotenv()

# Set up OpenAI API
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set up Reddit API
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent=os.getenv("REDDIT_USER_AGENT")
)

def fetch_user_content(username, limit=50):
    user = reddit.redditor(username)

    posts = []
    comments = []

    try:
        for submission in tqdm(user.submissions.new(limit=limit), desc="Fetching posts"):
            posts.append({
                "type": "post",
                "title": submission.title,
                "body": submission.selftext,
                "url": submission.url,
                "permalink": f"https://www.reddit.com{submission.permalink}"
            })

        for comment in tqdm(user.comments.new(limit=limit), desc="Fetching comments"):
            comments.append({
                "type": "comment",
                "body": comment.body,
                "link": f"https://www.reddit.com{comment.permalink}"
            })

    except Exception as e:
        print("Error fetching Reddit data:", e)

    return posts + comments

def build_prompt(username, user_data):
    prompt = f"""
You are an expert at analyzing Reddit users.

Based on the following posts and comments from Reddit user u/{username}, generate a detailed USER PERSONA. 
The persona should include:
- Age (if inferable)
- Gender (if inferable)
- Occupation
- Location (if any)
- Personality traits
- Hobbies & Interests
- Writing style
- Political or ideological leanings (if any)
- Any other notable patterns

For each characteristic, include a CITATION from the original Reddit content that supports it.

---

USER DATA:
"""

    for item in user_data:
        if item["type"] == "post":
            prompt += f"\n[POST] Title: {item['title']}\nBody: {item['body']}\nURL: {item['permalink']}\n"
        elif item["type"] == "comment":
            prompt += f"\n[COMMENT] {item['body']}\nLink: {item['link']}\n"

    return prompt

def generate_persona(prompt):
    try:
        response = openai.ChatCompletion.create(
            #model="gpt-4",
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an intelligent assistant that analyzes Reddit users."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("OpenAI Error:", e)
        return None

def save_to_file(username, persona_text):
    filename = f"user_personas/{username}.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"\n Persona saved to: {filename}")

def main():
    profile_url = input("Enter Reddit profile URL (e.g. https://www.reddit.com/user/kojied/): ").strip()
    if not profile_url.startswith("https://www.reddit.com/user/"):
        print("Invalid URL format.")
        return

    username = profile_url.split("/user/")[1].replace("/", "")
    print(f"\n🔍 Generating persona for u/{username}...")

    user_data = fetch_user_content(username)
    if not user_data:
        print("No data found.")
        return

    prompt = build_prompt(username, user_data)
    persona = generate_persona(prompt)

    if persona:
        save_to_file(username, persona)
    else:
        print("Failed to generate persona.")

if __name__ == "__main__":
    main()
