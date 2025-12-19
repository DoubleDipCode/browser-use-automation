# Browser-Use Automation Project

Browser automation using browser-use v0.11.2 with AI agents.

## Quick Start

```bash
# 1. Navigate to project
cd /Users/antonadmin/browser-use-project

# 2. Activate environment (required before every session)
source ./activate.sh

# 3. Run an example
python examples/basic_agent.py
```

## Project Structure

```
browser-use-project/
├── CLAUDE.md           # Instructions for Claude Code
├── README.md           # This file
├── activate.sh         # Environment activation script
├── knowledge_base.md   # Detailed documentation
├── examples/           # Example scripts
│   ├── basic_agent.py          # Simple agent example
│   ├── with_browser_session.py # Custom browser config
│   ├── with_chatbrowseruse.py  # Optimized model
│   ├── with_gemini.py          # Google Gemini
│   └── upwork_test.py          # Upwork navigation test
└── scripts/            # Production automation scripts
```

## Environment Details

- **Python**: 3.11
- **Virtual Env**: `/Users/antonadmin/browser-use-env/`
- **API Keys**: `/Users/antonadmin/.browser-use.env`
- **Browser-Use Version**: 0.11.2

## Available Models

| Model | Import | Notes |
|-------|--------|-------|
| ChatBrowserUse | `from browser_use import ChatBrowserUse` | Optimized, 3-5x faster |
| GPT-4o Mini | `ChatOpenAI(model="gpt-4o-mini")` | Good balance of speed/quality |
| GPT-4o | `ChatOpenAI(model="gpt-4o")` | Most capable |
| Gemini Flash | `ChatGoogle(model="gemini-2.0-flash")` | Fast, good for simple tasks |

## Creating New Scripts

```python
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, ChatOpenAI

load_dotenv('/Users/antonadmin/.browser-use.env')

async def main():
    agent = Agent(
        task="Your task description here",
        llm=ChatOpenAI(model="gpt-4o-mini"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

## SSH Access

This project is set up for remote access via VS Code SSH:

1. SSH into the Mac
2. Open this folder in VS Code
3. Use Claude Code with the CLAUDE.md context
4. Always run `source ./activate.sh` first

## Primary Goal

Automate Upwork job applications:
1. N8N workflow identifies relevant jobs
2. Browser-use performs the application process
3. Handle authentication, navigation, form submission

## Resources

- [Browser-Use Docs](https://docs.browser-use.com)
- [GitHub](https://github.com/browser-use/browser-use)
- [Discord](https://link.browser-use.com/discord)
