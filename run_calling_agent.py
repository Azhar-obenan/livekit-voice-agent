#!/usr/bin/env python3
"""
Run the Real Estate Calling Agent
This script starts the agent in the correct mode for handling outbound calls
"""

import subprocess
import sys
import os

def run_agent():
    """Run the agent in development mode for SIP calls"""
    
    print("🤖 Starting Real Estate Calling Agent...")
    print("=" * 50)
    print("Agent Configuration:")
    print("  - Mode: Development (for SIP calls)")
    print("  - Script: Real Estate Property Inquiry")
    print("  - Voice: OpenAI TTS (Alloy)")
    print("  - STT: Deepgram Nova-3")
    print("  - LLM: OpenAI GPT-4o-mini")
    print("=" * 50)
    
    try:
        # Run the agent in dev mode
        cmd = [sys.executable, "agent.py", "dev"]
        print(f"Running command: {' '.join(cmd)}")
        print("\n🚀 Agent is starting...")
        print("💡 The agent will automatically join calls made through the SIP system.")
        print("📞 Use complete_sip_setup.py to initiate calls.")
        print("\nPress Ctrl+C to stop the agent.\n")
        
        # Run the command
        subprocess.run(cmd, cwd=os.getcwd())
        
    except KeyboardInterrupt:
        print("\n\n🛑 Agent stopped by user.")
    except FileNotFoundError:
        print("❌ Error: agent.py not found. Make sure you're in the correct directory.")
    except Exception as e:
        print(f"❌ Error running agent: {e}")

if __name__ == "__main__":
    run_agent()
