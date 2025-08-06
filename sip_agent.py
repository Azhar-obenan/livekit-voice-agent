#!/usr/bin/env python3
"""
SIP-specific agent for real estate calls
"""

import asyncio
import logging
from livekit import rtc
from livekit.agents import (
    AutoSubscribe,
    JobContext,
    WorkerOptions,
    cli,
    llm,
)
from livekit.agents.voice_assistant import VoiceAssistant
from livekit.plugins import deepgram, openai, silero
from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger("sip-agent")
logger.setLevel(logging.INFO)

def prewarm(proc: JobContext):
    """Prewarm the agent"""
    proc.shutdown()

@cli.job_process
async def entrypoint(ctx: JobContext):
    """Main entrypoint for SIP calls"""
    
    logger.info(f"🎯 SIP Agent starting for room: {ctx.room.name}")
    
    # Connect to room first
    await ctx.connect(auto_subscribe=AutoSubscribe.AUDIO_ONLY)
    logger.info("✅ Connected to room")
    
    # Wait for participants
    logger.info("⏳ Waiting for participants...")
    
    # Create the voice assistant
    assistant = VoiceAssistant(
        vad=silero.VAD.load(),
        stt=deepgram.STT(model="nova-2"),
        llm=openai.LLM(model="gpt-4o-mini"),
        tts=openai.TTS(voice="alloy"),
        chat_ctx=llm.ChatContext().append(
            role="system",
            text=(
                "You are Elliott, a serious, professional outbound calling assistant for real estate. "
                "Your sole task is to ask property owners if they are open to selling their home right now. "
                "Do NOT sound overly friendly. Stay neutral, concise, and direct. "
                "Start with: 'Hi, this is Elliott — I'm with a local realtor. I was checking your property. Do you still own that by any chance?' "
                "If they say YES to owning: 'Got it, with the home prices being so high right now would you consider selling at this time?' "
                "If they say NO to selling: End the call politely. "
                "If they say YES to selling: Ask qualification questions about timeline, price, and motivation. "
                "Handle common objections professionally and end calls when appropriate."
            ),
        ),
    )

    # Start the assistant
    assistant.start(ctx.room)
    
    # Monitor for participants
    @ctx.room.on("participant_connected")
    def on_participant_connected(participant: rtc.RemoteParticipant):
        logger.info(f"📞 Participant joined: {participant.identity}")
        
        # Start conversation immediately when SIP participant joins
        if not participant.identity.startswith("agent-"):
            logger.info("🗣️  Starting conversation with SIP participant")
            asyncio.create_task(
                assistant.say(
                    "Hi, this is Elliott — I'm with a local realtor. I was checking your property. Do you still own that by any chance?",
                    allow_interruptions=True
                )
            )

    @ctx.room.on("participant_disconnected")
    def on_participant_disconnected(participant: rtc.RemoteParticipant):
        logger.info(f"📞 Participant left: {participant.identity}")

    # Keep the agent running
    logger.info("🎯 SIP Agent ready and waiting for calls...")
    
    # Initial greeting after a short delay
    await asyncio.sleep(3)
    logger.info("🗣️  Sending initial greeting")
    await assistant.say(
        "Hi, this is Elliott — I'm with a local realtor. I was checking your property. Do you still own that by any chance?",
        allow_interruptions=True
    )

if __name__ == "__main__":
    cli.run_app(
        WorkerOptions(
            entrypoint_fnc=entrypoint,
            prewarm_fnc=prewarm,
        ),
    )
