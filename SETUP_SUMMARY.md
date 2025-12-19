# Browser-Use Persistent Login Setup - SOLVED ✅

## Problem
Browser-use v0.11.2 automatically copies Chrome profiles to temp directories, losing all logged-in sessions.

## Solution
Use CDP (Chrome DevTools Protocol) connection to connect to a running Chrome instance instead of launching a new one.

## How It Works

### 1. Start Chrome with Remote Debugging
```bash
./scripts/start_chrome_debug.sh
```

This:
- Kills any running Chrome instances
- Starts Chrome with `--remote-debugging-port=9222`
- Uses profile at `~/.config/browseruse/chrome-debug`
- Keeps Chrome running in the background

### 2. Log In (One-Time Setup)
In the Chrome window that opens:
- Navigate to LinkedIn, Upwork, or any site
- Log in manually
- Login is saved in `~/.config/browseruse/chrome-debug`

### 3. Run Your Scripts
```python
from browser_use import Agent, Browser, ChatBrowserUse

browser = Browser(cdp_url="http://localhost:9222")

agent = Agent(
    task="Navigate to my LinkedIn profile",
    llm=ChatBrowserUse(),
    browser=browser,
)
await agent.run()
```

### 4. Results
- ✅ Scripts connect to the running Chrome
- ✅ All logins persist across runs
- ✅ No profile copying to temp directories
- ✅ Works with LinkedIn, Upwork, any authenticated site

## Files Created/Modified

1. **scripts/start_chrome_debug.sh** - Helper to start Chrome with debugging
2. **scripts/linkedin_navigate.py** - Working example with CDP connection
3. **scripts/template.py** - Updated template using CDP by default
4. **CLAUDE.md** - Complete documentation of the solution

## Workflow

```bash
# One-time setup
./scripts/start_chrome_debug.sh
# Log in to required sites in Chrome window

# Run automation (as many times as needed)
source ./activate.sh
python scripts/linkedin_navigate.py

# Chrome stays running - run more scripts without restarting
python scripts/upwork_automation.py

# When done, stop Chrome
pkill "Google Chrome"
```

## Key Learnings

1. **Browser-use 0.11.2 always copies profiles** - This is hardcoded and cannot be disabled
2. **CDP connection bypasses this** - Connecting to an existing Chrome avoids launching a new one
3. **Chrome requires non-default profile for debugging** - Cannot use default profile with `--remote-debugging-port`
4. **Solution is programmatic** - No manual Chrome launching required after initial setup

## Next Steps

Ready for Upwork automation:
1. Run `./scripts/start_chrome_debug.sh`
2. Log in to Upwork in the Chrome window
3. Create Upwork automation scripts using the template
4. Integrate with N8N workflow

