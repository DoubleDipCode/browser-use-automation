"""
Basic Browser-Use Agent Example
Run: python examples/basic_agent.py
"""
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, ChatOpenAI

# Load API keys
load_dotenv('/Users/antonadmin/.browser-use.env')

async def main():
    # Create agent with OpenAI
    agent = Agent(
        task="Go to google.com and search for 'browser automation python'",
        llm=ChatOpenAI(model="gpt-4o-mini", temperature=0),
    )
    
    # Run the agent
    result = await agent.run()
    print("\n" + "="*50)
    print("RESULT:")
    print(result)

if __name__ == "__main__":
    asyncio.run(main())
