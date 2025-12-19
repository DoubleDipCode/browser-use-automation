"""
Browser-Use 0.11.2 Import Test Script
Tests that all new import patterns work correctly.
"""
import asyncio
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv('/Users/antonadmin/.browser-use.env')

print("=" * 50)
print("Browser-Use 0.11.2 Import Test")
print("=" * 50)

# Test 1: Core imports
print("\n[1] Testing core imports...")
try:
    from browser_use import Agent
    print("    ✓ Agent imported successfully")
except ImportError as e:
    print(f"    ✗ Agent import failed: {e}")

# Test 2: LLM imports from browser_use
print("\n[2] Testing LLM imports from browser_use...")
try:
    from browser_use import ChatOpenAI
    print("    ✓ ChatOpenAI imported from browser_use")
except ImportError as e:
    print(f"    ✗ ChatOpenAI import failed: {e}")

try:
    from browser_use import ChatGoogle
    print("    ✓ ChatGoogle imported from browser_use")
except ImportError as e:
    print(f"    ✗ ChatGoogle import failed: {e}")

try:
    from browser_use import ChatAnthropic
    print("    ✓ ChatAnthropic imported from browser_use")
except ImportError as e:
    print(f"    ✗ ChatAnthropic import failed: {e}")

# Test 3: New ChatBrowserUse (0.11.0+)
print("\n[3] Testing ChatBrowserUse (new in 0.11.0)...")
try:
    from browser_use import ChatBrowserUse
    print("    ✓ ChatBrowserUse imported successfully")
except ImportError as e:
    print(f"    ✗ ChatBrowserUse import failed: {e}")

# Test 4: BrowserSession
print("\n[4] Testing BrowserSession...")
try:
    from browser_use import BrowserSession
    print("    ✓ BrowserSession imported from browser_use")
except ImportError as e:
    print(f"    ✗ BrowserSession import failed: {e}")

# Test 5: Tools
print("\n[5] Testing Tools...")
try:
    from browser_use import Tools
    print("    ✓ Tools imported from browser_use")
except ImportError as e:
    print(f"    ✗ Tools import failed: {e}")

# Test 6: Alternative LLM import path
print("\n[6] Testing alternative import path (browser_use.llm)...")
try:
    from browser_use.llm import ChatOpenAI as ChatOpenAI2
    print("    ✓ ChatOpenAI imported from browser_use.llm")
except ImportError as e:
    print(f"    ✗ Alternative import failed: {e}")

# Test 7: Check version
print("\n[7] Checking browser-use version...")
try:
    import browser_use
    version = getattr(browser_use, '__version__', 'unknown')
    print(f"    ✓ browser-use version: {version}")
except Exception as e:
    print(f"    ✗ Version check failed: {e}")

# Test 8: API key availability
print("\n[8] Checking API keys...")
openai_key = os.getenv('OPENAI_API_KEY')
google_key = os.getenv('GOOGLE_API_KEY')
print(f"    OPENAI_API_KEY: {'✓ Set' if openai_key else '✗ Not set'}")
print(f"    GOOGLE_API_KEY: {'✓ Set' if google_key else '✗ Not set'}")

# Test 9: Create a simple agent (no run)
print("\n[9] Testing Agent creation...")
try:
    from browser_use import Agent, ChatOpenAI
    llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)
    agent = Agent(
        task="Test task - not executed",
        llm=llm,
    )
    print("    ✓ Agent created successfully")
except Exception as e:
    print(f"    ✗ Agent creation failed: {e}")

print("\n" + "=" * 50)
print("Test Complete!")
print("=" * 50)
