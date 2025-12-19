"""
Upwork Navigation Test
Tests basic Upwork navigation - does NOT submit applications
Run: python examples/upwork_test.py
"""
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, BrowserSession, ChatOpenAI

load_dotenv('/Users/antonadmin/.browser-use.env')

async def main():
    # Use persistent browser session for login state
    browser_session = BrowserSession(
        executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        user_data_dir='/Users/antonadmin/.config/browseruse/profiles/upwork',
        headless=False,
    )
    
    agent = Agent(
        task="""
        Go to upwork.com and:
        1. Check if logged in (look for profile icon or login button)
        2. If logged in, go to 'Find Work' or job search
        3. Search for 'python automation' jobs
        4. List the first 3 job titles you see
        
        Do NOT apply to any jobs - just report what you find.
        """,
        llm=ChatOpenAI(model="gpt-4o-mini"),
        browser_session=browser_session,
    )
    
    result = await agent.run()
    print("\n" + "="*50)
    print("UPWORK TEST RESULT:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
