# Browser-Use Knowledge Base - v0.11.2
## Last Updated: December 19, 2025

---

## System Configuration

### Environment Setup
- **Location**: `/Users/antonadmin/browser-use-env/`
- **Version**: Browser-use v0.11.2 (Updated December 2025)
- **Python**: 3.11 in virtual environment
- **Platform**: macOS (Darwin)
- **API Keys**: Stored in `/Users/antonadmin/.browser-use.env`

### Activation Commands
```bash
# Activate environment
source /Users/antonadmin/browser-use-env/bin/activate

# Load environment variables
export $(cat ~/.browser-use.env | xargs)

# Or in one command:
source /Users/antonadmin/browser-use-env/bin/activate && export $(cat ~/.browser-use.env | xargs)
```

---

## Version 0.11.2 Import Patterns

### CORRECT Import Patterns (Current)

```python
# Primary imports - use these
from browser_use import Agent
from browser_use import ChatOpenAI, ChatAnthropic, ChatGoogle
from browser_use import BrowserSession
from browser_use import Tools

# New in 0.11.0 - Browser-Use optimized model
from browser_use import ChatBrowserUse

# Alternative LLM import path (also works)
from browser_use.llm import ChatOpenAI
```

### DEPRECATED/BROKEN Patterns

```python
# DON'T use langchain directly - causes "no field 'ainvoke'" error
from langchain_openai import ChatOpenAI  # WRONG

# Old browser config import - may not work
from browser_use.browser import Browser, BrowserConfig  # OUTDATED
```

---

## Basic Usage Examples

### 1. Simple Agent with OpenAI
```python
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, ChatOpenAI

load_dotenv()

async def main():
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )
    
    agent = Agent(
        task="Find the latest news on Upwork",
        llm=llm,
    )
    
    result = await agent.run()
    print(result)

asyncio.run(main())
```

### 2. Using Browser-Use Optimized Model (Recommended)
```python
import asyncio
from browser_use import Agent, ChatBrowserUse

async def main():
    agent = Agent(
        task="Your task here",
        llm=ChatBrowserUse()  # 3-5x faster, SOTA accuracy
    )
    await agent.run()

asyncio.run(main())
```

### 3. With Google Gemini
```python
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, ChatGoogle

load_dotenv()

async def main():
    llm = ChatGoogle(model='gemini-2.0-flash')
    
    agent = Agent(
        task="Your task here",
        llm=llm,
    )
    await agent.run()

asyncio.run(main())
```

### 4. With Skills (New in 0.11.0)
```python
from browser_use import Agent, ChatBrowserUse

agent = Agent(
    task='Your task',
    skills=['skill-uuid-1', 'skill-uuid-2'],  # Specific skills
    # or skills=['*'],  # All skills
    llm=ChatBrowserUse()
)
```

### 5. With Custom Browser Session
```python
import asyncio
from browser_use import Agent, BrowserSession, ChatOpenAI
from dotenv import load_dotenv

load_dotenv()

async def main():
    browser_session = BrowserSession(
        executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
        user_data_dir='~/.config/browseruse/profiles/default',
    )
    
    llm = ChatOpenAI(model="gpt-4o-mini")
    
    agent = Agent(
        task="Your task here",
        llm=llm,
        browser_session=browser_session
    )
    
    await agent.run()

asyncio.run(main())
```

### 6. With Custom Tools
```python
from browser_use import Agent, Tools, ChatOpenAI

tools = Tools()

@tools.action(description='Description of what this tool does.')
def custom_tool(param: str) -> str:
    return f"Result: {param}"

agent = Agent(
    task="Your task",
    llm=ChatOpenAI(model="gpt-4o-mini"),
    tools=tools,
)
```

---

## API Keys Configuration

### Current .browser-use.env Setup
- OPENAI_API_KEY: Working
- GOOGLE_API_KEY: Working (renamed from GEMINI_API_KEY)
- DEEPSEEK_API_KEY: Available
- ANTHROPIC_API_KEY: Empty - add if needed

### Environment Variable Notes
- GEMINI_API_KEY is DEPRECATED - Use GOOGLE_API_KEY instead
- Browser-Use reads from environment automatically when using their Chat classes

---

## Version History & Breaking Changes

### 0.11.0 to 0.11.2 (Current)
- Skills Integration: New skills parameter for agents
- ChatBrowserUse: Optimized model for browser automation
- Mistral provider: Added with schema sanitization
- Fallback LLM support: Automatic fallback to secondary models

### 0.10.0
- Major stability improvements
- Click coordinates recording
- Captcha and impossible task flags in AgentEvent
- Variable substitution in reruns
- Vercel AI Gateway integration

### 0.9.x
- Sandboxes support
- LLM-as-judge for monitoring
- Demo mode for in-browser logging
- Session manager improvements

### 0.7.x (Previous)
- Basic Agent/Controller pattern
- from browser_use.llm import ChatOpenAI pattern established

---

## Common Issues & Solutions

### Issue 1: ChatOpenAI object has no field ainvoke
- Cause: Using langchain ChatOpenAI instead of browser-use
- Solution: Import from browser_use or browser_use.llm

### Issue 2: Module not found errors
- Cause: Virtual environment not activated
- Solution: source /Users/antonadmin/browser-use-env/bin/activate

### Issue 3: API key errors
- Cause: Environment variables not loaded
- Solution: export $(cat ~/.browser-use.env | xargs)

### Issue 4: CDP Connection Errors During Execution
- Cause: Browser session lost connection (common with automation)
- Impact: Usually occurs mid-execution, doesn't prevent initial setup
- Solution: Normal behavior, script often still completes

### Issue 5: Chrome already running error
- Cause: Another Chrome instance using the profile
- Solution: Close other Chrome instances or use different profile

---

## Upwork Automation Project

### Goal
Automate job applications on Upwork via N8N workflow to Browser-use execution

### Status
- Browser-use foundation working
- Basic navigation confirmed
- Integration with N8N in progress

### Next Steps
1. Test Upwork login with persistent session
2. Build job search automation
3. Create application submission flow
4. Integrate with N8N webhook triggers

---

## Quick Reference

### Start a New Script
```python
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, ChatOpenAI

load_dotenv()

async def main():
    agent = Agent(
        task="YOUR TASK HERE",
        llm=ChatOpenAI(model="gpt-4o-mini"),
    )
    await agent.run()

asyncio.run(main())
```

### Run a Script
```bash
source /Users/antonadmin/browser-use-env/bin/activate
export $(cat ~/.browser-use.env | xargs)
python your_script.py
```

---

## Resources

- Documentation: https://docs.browser-use.com
- GitHub: https://github.com/browser-use/browser-use
- Discord: https://link.browser-use.com/discord
- Cloud Platform: https://cloud.browser-use.com
