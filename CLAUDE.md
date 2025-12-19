# Browser-Use Project Instructions for Claude Code

## Project Overview
This project uses browser-use (v0.11.2) to automate browser tasks. The primary use case is Upwork job application automation.

## Environment Setup

### CRITICAL: Always run these commands before executing any Python script
```bash
source /Users/antonadmin/browser-use-env/bin/activate
export $(cat /Users/antonadmin/.browser-use.env | xargs)
```

Or use the convenience script:
```bash
source ./activate.sh
```

### Virtual Environment Location
- Path: `/Users/antonadmin/browser-use-env/`
- Python: 3.11

### API Keys Location
- Path: `/Users/antonadmin/.browser-use.env`
- Contains: OPENAI_API_KEY, GOOGLE_API_KEY, DEEPSEEK_API_KEY, BROWSER_USE_API_KEY

## Import Patterns

### CORRECT (use these):
```python
from browser_use import Agent, ChatOpenAI, ChatGoogle, ChatAnthropic
from browser_use import BrowserSession, Tools
from browser_use import ChatBrowserUse  # Optimized model, 3-5x faster
```

### WRONG (will cause errors):
```python
from langchain_openai import ChatOpenAI  # Causes 'ainvoke' error
from browser_use.browser import Browser, BrowserConfig  # Outdated
```

## Quick Start Template (ChatBrowserUse - Recommended)

### With Persistent Login (for LinkedIn, Upwork, etc.)

```python
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, Browser, ChatBrowserUse

load_dotenv('/Users/antonadmin/.browser-use.env')

async def main():
    # Connect to Chrome with persistent logins
    # Start Chrome first: ./scripts/start_chrome_debug.sh
    browser = Browser(cdp_url="http://localhost:9222")

    agent = Agent(
        task="YOUR TASK HERE",
        llm=ChatBrowserUse(),  # 3-5x faster, optimized for browser automation
        browser=browser,
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

### Without Login (basic automation)

```python
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, ChatBrowserUse

load_dotenv('/Users/antonadmin/.browser-use.env')

async def main():
    agent = Agent(
        task="YOUR TASK HERE",
        llm=ChatBrowserUse(),  # 3-5x faster, optimized for browser automation
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

### Alternative: With OpenAI Models
```python
import asyncio
from dotenv import load_dotenv
from browser_use import Agent, ChatOpenAI

load_dotenv('/Users/antonadmin/.browser-use.env')

async def main():
    agent = Agent(
        task="YOUR TASK HERE",
        llm=ChatOpenAI(model="gpt-4o-mini"),
    )
    result = await agent.run()
    print(result)

asyncio.run(main())
```

## Available Models

### 1. ChatBrowserUse (RECOMMENDED)
Browser-use's optimized model - **3-5x faster** than other models.

```python
from browser_use import ChatBrowserUse
llm = ChatBrowserUse()
```

**Performance:**
- 65.7% accuracy on OnlineMind2Web (matches Gemini 2.5 Computer Use)
- ~3 seconds per step average
- 68 seconds average task completion (vs 225s for Gemini 2.5, 285s for Claude Sonnet 4.5)

**Pricing:**
- Input tokens: $0.50/1M
- Output tokens: $3.00/1M
- Cached tokens: $0.10/1M

**Why It's Faster:**
- KV cache optimization
- DOM-based navigation (screenshots only when needed)
- Smart text extraction from DOM
- Minimal output tokens

### 2. OpenAI Models
```python
from browser_use import ChatOpenAI
llm = ChatOpenAI(model="gpt-4o-mini")  # or "gpt-4o"
```

### 3. Google Gemini
```python
from browser_use import ChatGoogle
llm = ChatGoogle(model="gemini-2.0-flash")
```

## Browser Session Options

### Method 1: CDP Connection (RECOMMENDED for Persistent Logins)

**Use this for LinkedIn, Upwork, or any site requiring login persistence.**

Step 1: Start Chrome with remote debugging (one-time setup):
```bash
./scripts/start_chrome_debug.sh
```

Step 2: Log in to your sites manually in the opened Chrome window (one-time)

Step 3: Use CDP connection in your scripts:
```python
from browser_use import Agent, Browser, ChatBrowserUse

browser = Browser(
    cdp_url="http://localhost:9222",  # Connect to running Chrome instance
)

agent = Agent(
    task="Your task here",
    llm=ChatBrowserUse(),
    browser=browser,
)
```

**How it works:**
- Chrome stores logins in `~/.config/browseruse/chrome-debug`
- No profile copying to temp directories
- Logins persist across runs
- You must start Chrome with `./scripts/start_chrome_debug.sh` before running scripts

### Method 2: BrowserSession (No Persistent Logins)

**Note:** Browser-use 0.11.2 always copies profiles to temp directories, losing logins.

```python
from browser_use import BrowserSession

# Use custom browser-use profile (for isolated sessions)
browser_session = BrowserSession(
    executable_path='/Applications/Google Chrome.app/Contents/MacOS/Google Chrome',
    user_data_dir='/Users/antonadmin/.config/browseruse/profiles/default',
    headless=False,
)

# Headless mode (no visible browser)
browser_session = BrowserSession(headless=True)
```

## Custom Tools

```python
from browser_use import Tools

tools = Tools()

@tools.action(description='Description here')
def my_tool(param: str) -> str:
    return f"Result: {param}"

agent = Agent(task="...", llm=llm, tools=tools)
```

## Skills (New in 0.11.0)

```python
agent = Agent(
    task="...",
    llm=ChatBrowserUse(),
    skills=['skill-uuid-1'],  # or skills=['*'] for all
)
```

## Running Scripts

Always from project directory:
```bash
cd /Users/antonadmin/browser-use-project
source ./activate.sh
python your_script.py
```

## Troubleshooting

| Error | Solution |
|-------|----------|
| "no field 'ainvoke'" | Wrong import - use `from browser_use import ChatOpenAI` |
| Module not found | Activate venv: `source /Users/antonadmin/browser-use-env/bin/activate` |
| API key error | Load env: `export $(cat /Users/antonadmin/.browser-use.env | xargs)` |
| Chrome profile locked | Close other Chrome instances |

## Persistent Login Workflow

For automation requiring logged-in sessions (LinkedIn, Upwork):

1. **Start Chrome with debugging** (if not already running):
   ```bash
   ./scripts/start_chrome_debug.sh
   ```

2. **First time only:** Log in to required sites in the Chrome window

3. **Run your automation scripts:**
   ```bash
   source ./activate.sh
   python scripts/your_script.py
   ```

4. **Chrome stays running** - you can run multiple scripts without restarting

5. **To stop Chrome:**
   ```bash
   pkill "Google Chrome"
   ```

## File Structure
```
browser-use-project/
├── CLAUDE.md          # This file - Claude Code instructions
├── README.md          # Project documentation
├── activate.sh        # Environment activation script
├── knowledge_base.md  # Detailed browser-use documentation
├── requirements.txt   # API server dependencies
├── logging.yaml       # Logging configuration for API server
├── run_api.sh         # Start API server
├── stop_api.sh        # Stop API server
├── api/               # API server (FastAPI)
│   ├── __init__.py
│   ├── server.py      # FastAPI application
│   ├── config.py      # Configuration management
│   ├── models.py      # Pydantic request/response models
│   ├── database.py    # SQLite operations with WAL mode
│   ├── auth.py        # API key authentication
│   └── tasks.db       # SQLite database (gitignored)
├── logs/              # API server logs
│   └── api.log        # Rotating log file (gitignored)
├── examples/          # Example scripts
│   ├── basic_agent.py
│   ├── test_imports.py
│   ├── with_browser_session.py
│   ├── with_chatbrowseruse.py
│   ├── with_gemini.py
│   └── upwork_test.py
├── scripts/           # Production scripts
│   ├── template.py            # Script template (copy this to start new scripts)
│   ├── start_chrome_debug.sh  # Helper to start Chrome with CDP
│   ├── linkedin_navigate.py   # LinkedIn profile navigation (working example)
│   └── (your automation scripts)
└── tests/             # API server tests
    └── (test files to be added)
```

## API Server

### Overview
FastAPI-based HTTP server that allows N8N (or any HTTP client) to dynamically trigger browser automation tasks. The server accepts task requests, queues them for execution, and optionally sends webhook callbacks when tasks complete.

### Quick Start

#### 1. Start Chrome with CDP (if not already running)
```bash
./scripts/start_chrome_debug.sh
```

#### 2. Start the API Server
```bash
./run_api.sh
```

The server will:
- Initialize SQLite database with WAL mode
- Listen on `http://0.0.0.0:8000`
- Be accessible from N8N Docker at `http://host.docker.internal:8000`

#### 3. Stop the API Server
```bash
./stop_api.sh
```

### API Endpoints

#### Health Check
```bash
GET /health
```

Returns the health status of all components:
```json
{
  "api": "healthy",
  "chrome_cdp": "healthy",
  "database": "healthy",
  "queue_size": 0
}
```

#### Create Task
```bash
POST /tasks
Headers: X-API-Key: <your-api-key>
Content-Type: application/json
```

Request body:
```json
{
  "url": "https://example.com/application-form",
  "task_description": "Fill in the form with the provided details and submit",
  "form_data": {
    "name": "John Doe",
    "email": "john@example.com"
  },
  "callback_url": "http://n8n:5678/webhook/task-complete",
  "timeout": 300
}
```

Response:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "queued",
  "queue_position": null,
  "created_at": "2025-12-19T10:30:00Z"
}
```

#### Get Task Status
```bash
GET /tasks/{task_id}
Headers: X-API-Key: <your-api-key>
```

Response:
```json
{
  "task_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "url": "https://example.com/form",
  "task_description": "Fill in the form...",
  "result": "Task completed successfully",
  "error": null,
  "created_at": "2025-12-19T10:30:00Z",
  "started_at": "2025-12-19T10:30:05Z",
  "completed_at": "2025-12-19T10:32:15Z"
}
```

#### List Tasks
```bash
GET /tasks?status=completed&limit=50&offset=0
Headers: X-API-Key: <your-api-key>
```

Response:
```json
{
  "tasks": [...],
  "total": 42,
  "limit": 50,
  "offset": 0
}
```

### Task States
- `queued` - Task received, waiting for execution
- `running` - Currently being executed
- `completed` - Successfully finished
- `failed` - Error occurred
- `timeout` - Exceeded timeout limit

### N8N Integration

#### Setup in N8N

1. **Add API Key Credential** in N8N:
   - Type: Generic Credential Type
   - Name: `browserUseApi`
   - Value: Copy from `/Users/antonadmin/.browser-use.env` (API_SERVER_KEY)

2. **HTTP Request Node Configuration**:
   - Method: `POST`
   - URL: `http://host.docker.internal:8000/tasks`
   - Authentication: Use credential from step 1
   - Headers:
     - `X-API-Key`: `{{ $credentials.browserUseApi.key }}`
     - `Content-Type`: `application/json`
   - Body:
     ```json
     {
       "url": "{{ $json.jobUrl }}",
       "task_description": "{{ $json.taskDescription }}",
       "form_data": {{ $json.formData }},
       "callback_url": "{{ $resumeWebhookUrl }}"
     }
     ```

#### Example N8N Workflow
```
[Trigger: Job Found]
    ↓
[HTTP Request: POST /tasks] → Returns task_id
    ↓
[Set: Store task_id]
    ↓
[Wait for Webhook: callback_url] → Receives results
    ↓
[Process Results]
```

### Configuration

All configuration is managed via environment variables in `/Users/antonadmin/.browser-use.env`:

```bash
API_SERVER_KEY=<your-api-key>      # Required - Authentication key
API_HOST=0.0.0.0                   # Optional - Host to bind (default: 0.0.0.0)
API_PORT=8000                      # Optional - Port to listen on (default: 8000)
CHROME_CDP_URL=http://localhost:9222  # Optional - Chrome CDP URL
```

### API Key

The API server uses API key authentication via the `X-API-Key` header. The key is stored in `/Users/antonadmin/.browser-use.env` as `API_SERVER_KEY`.

To generate a new API key:
```bash
python -c "import secrets; print('API_SERVER_KEY=' + secrets.token_urlsafe(32))"
```

### Database

- **Type**: SQLite with WAL (Write-Ahead Logging) mode
- **Location**: `api/tasks.db`
- **Features**:
  - Concurrent read/write access
  - Persistent task history
  - Automatic cleanup of incomplete tasks on server restart

### Logging

- **Location**: `logs/api.log`
- **Rotation**: 10MB max file size, keep 30 backup files
- **Logs**: API requests, task execution, errors, Chrome CDP status

Monitor logs in real-time:
```bash
tail -f logs/api.log
```

### Current Status (Phase 2 Complete)

✅ **Implemented**:
- Core API server with FastAPI
- Health check endpoint
- Task creation and storage
- Task status retrieval
- Task listing with pagination
- API key authentication
- SQLite database with WAL mode
- Chrome CDP availability check

🚧 **In Progress (Phase 3)**:
- Background task queue with asyncio
- Browser-use Agent execution
- Webhook callbacks
- Task cancellation
- Queue status endpoint

### Testing the API

Example curl commands:

```bash
# Health check
curl http://localhost:8000/health

# Create a task
curl -X POST http://localhost:8000/tasks \
  -H "X-API-Key: YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://example.com/form",
    "task_description": "Fill out the contact form",
    "form_data": {"name": "Test User"},
    "timeout": 300
  }'

# Get task status
curl http://localhost:8000/tasks/{task_id} \
  -H "X-API-Key: YOUR_API_KEY"

# List tasks
curl "http://localhost:8000/tasks?limit=10" \
  -H "X-API-Key: YOUR_API_KEY"
```

## Primary Goal
Build Upwork job application automation:
1. N8N identifies relevant jobs
2. Browser-use performs the application
3. Handle login, navigation, form filling

## Reference Documentation
- Official docs: https://docs.browser-use.com
- GitHub: https://github.com/browser-use/browser-use
