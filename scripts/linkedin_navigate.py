"""
LinkedIn Profile Navigation Script
Goes to LinkedIn and navigates to your profile

BEFORE RUNNING:
1. Close all Chrome instances
2. Launch Chrome with debugging:
   /Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
     --remote-debugging-port=9222 \
     --user-data-dir="$HOME/Library/Application Support/Google/Chrome"
3. Run this script: python scripts/linkedin_navigate.py
"""
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatBrowserUse

# Load API keys
load_dotenv('/Users/antonadmin/.browser-use.env')

async def main():
    # Connect to existing Chrome instance (must be started with --remote-debugging-port=9222)
    # This avoids profile copying because we don't launch Chrome, just connect to it
    browser = Browser(
        cdp_url="http://localhost:9222",
    )

    agent = Agent(
        task="""
        Go to linkedin.com and navigate to my profile page.
        If you're not logged in, tell me to log in first.
        If you are logged in, go to 'Me' or 'Profile' and report what you see on my profile.
        """,
        llm=ChatBrowserUse(),
        browser=browser,
    )

    # Run the agent
    result = await agent.run()
    print("\n" + "="*50)
    print("LINKEDIN NAVIGATION RESULT:")
    print(result)
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
