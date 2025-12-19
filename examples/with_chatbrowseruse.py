"""
Using ChatBrowserUse - Browser-Use's Optimized Model
This model is 3-5x faster and optimized for browser automation
Run: python examples/with_chatbrowseruse.py
"""
import asyncio
from browser_use import Agent, ChatBrowserUse

async def main():
    # ChatBrowserUse is browser-use's own optimized model
    # No API key needed in env - uses browser-use cloud
    agent = Agent(
        task="Go to news.ycombinator.com and tell me the top 3 stories",
        llm=ChatBrowserUse(),
    )
    
    result = await agent.run()
    print("\n" + "="*50)
    print("RESULT:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
