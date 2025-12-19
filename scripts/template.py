"""
Browser-Use Script Template
Copy this template to create new automation scripts

BEFORE RUNNING:
1. Start Chrome with debugging: ./scripts/start_chrome_debug.sh
2. Run this script: python scripts/your_script.py
"""
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatBrowserUse

# Load API keys
load_dotenv('/Users/antonadmin/.browser-use.env')

async def main():
    # Connect to Chrome with persistent login (recommended)
    # Must start Chrome first: ./scripts/start_chrome_debug.sh
    browser = Browser(
        cdp_url="http://localhost:9222",
    )

    # Create agent with ChatBrowserUse (3-5x faster, optimized for browser automation)
    agent = Agent(
        task="""
        Your task description here.
        Be specific about what you want the agent to do.
        """,
        llm=ChatBrowserUse(),
        browser=browser,
    )

    # Run the agent
    result = await agent.run()
    print("\n" + "="*50)
    print("RESULT:")
    print(result)
    print("="*50)

if __name__ == "__main__":
    asyncio.run(main())
