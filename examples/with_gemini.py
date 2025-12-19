"""
Using Google Gemini with Browser-Use
Run: python examples/with_gemini.py
"""
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, ChatGoogle

load_dotenv('/Users/antonadmin/.browser-use.env')

async def main():
    # Use Gemini Flash - fast and capable
    llm = ChatGoogle(model='gemini-2.0-flash')
    
    agent = Agent(
        task="Go to wikipedia.org and find information about browser automation",
        llm=llm,
    )
    
    result = await agent.run()
    print("\n" + "="*50)
    print("RESULT:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
