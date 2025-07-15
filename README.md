
->Reddit Persona Builder

Generate psychological user personas from any Reddit profile using LLMs (OpenAI GPT-3.5) and public post/comment data. This tool scrapes a user's public Reddit activity and analyzes it to infer personality traits, interests, opinions, and behavior patterns.

->Features
- Builds a psychological **user persona**
- Extracts Reddit posts and comments via Reddit API
- Uses **OpenAI GPT-3.5** to generate a persona
- Outputs persona to `.txt` file with **citations**
- Tested on real Reddit profiles
- Keeps API keys secret using `.env`

->Technologies Used
- Python 3.8+
- [PRAW (Python Reddit API Wrapper)](https://praw.readthedocs.io/en/latest/)
- [OpenAI API](https://platform.openai.com/)
- [dotenv](https://pypi.org/project/python-dotenv/)
- tqdm (for progress bars)

->Clone the repository
- git clone https:https://github.com/Priyanshu-Kumar-4160/PersonaBuilder.git
- cd PersonaBuilder

->Install dependencies
- pip install -r requirements.txt

->Setup .env file
- REDDIT_CLIENT_ID=your_reddit_client_id
- REDDIT_SECRET=your_reddit_secret
- REDDIT_USER_AGENT=your_user_agent_string
- OPENAI_API_KEY=your_openai_api_key

->Run the Script
- python reddit_persona_builder.py


