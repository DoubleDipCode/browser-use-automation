"""
Browser-Use with Custom Browser Session
Uses existing Chrome profile for persistent logins
Run: python examples/with_browser_session.py
"""
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, BrowserSession, ChatOpenAI

load_dotenv('/Users/antonadmin/.browser-use.env')

async def main():
    # Create browser session with Chrome
    browser_session = BrowserSession(
        executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        user_data_dir='/Users/antonadmin/.config/browseruse/profiles/default',
        headless=False,  # Set True for headless
    )
    
    # Create agent with custom browser
    agent = Agent(
        task="Go to github.com and tell me the trending repositories",
        llm=ChatOpenAI(model="gpt-4o-mini"),
        browser_session=browser_session,
    )
    
    result = await agent.run()
    print("\n" + "="*50)
    print("RESULT:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
