# LiveKit Voice Agent

A professional real estate outbound calling assistant built with LiveKit agents framework.

## Features
- Real estate cold calling automation
- Professional conversation flow with qualification questions
- Handles common objections and scenarios
- Built with LiveKit agents, OpenAI, and Deepgram

## Setup
1. Install dependencies: `pip install -r requirements.txt`
2. Copy `.env.example` to `.env` and fill in your API keys
3. Run the agent: `python agent.py dev`

## Configuration
- Update your LiveKit credentials in `.env`
- Set your OpenAI API key for LLM and TTS
- Configure Deepgram API key for speech recognition
- Update SIP trunk settings for outbound calling

## Usage
The agent follows a professional real estate calling script and can:
- Detect voicemails and automated responses
- Ask qualification questions
- Handle objections professionally
- Schedule follow-up calls with realtors
