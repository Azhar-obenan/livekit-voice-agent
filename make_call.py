import asyncio
import os
from dotenv import load_dotenv
from livekit import api
from livekit.protocol.sip import CreateSIPParticipantRequest

load_dotenv()

async def make_outbound_call():
    """Make an outbound call using the configured trunk"""
    
    lkapi = api.LiveKitAPI(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET")
    )

    # Call configuration
    from_number = "+13082514678"  # Your outbound number
    to_number = "+923024491162"   # Target number in Pakistan
    trunk_id = os.getenv("SIP_OUTBOUND_TRUNK_ID")
    
    if not trunk_id:
        print("Error: SIP_OUTBOUND_TRUNK_ID not found. Please run setup_trunk.py first.")
        return

    # Create SIP participant request
    request = CreateSIPParticipantRequest(
        sip_trunk_id=trunk_id,
        sip_call_to=to_number,
        sip_number=from_number,
        room_name="outbound-call-room",
        participant_identity="outbound-caller",
        participant_name="Real Estate Agent",
        participant_metadata='{"call_type": "outbound", "purpose": "real_estate"}',
        dtmf="",
        play_ringtone=True,
        hide_phone_number=False,
        ringing_timeout=30,  # 30 seconds timeout
        max_call_duration=300,  # 5 minutes max call duration
        enable_krisp=True  # Enable noise cancellation
    )

    try:
        print(f"Initiating call from {from_number} to {to_number}...")
        participant = await lkapi.sip.create_sip_participant(request)
        
        print(f"Call initiated successfully!")
        print(f"Participant ID: {participant.participant_id}")
        print(f"Participant Identity: {participant.participant_identity}")
        print(f"Room Name: {participant.room_name}")
        print(f"SIP Call ID: {participant.sip_call_id}")
        
        return participant
        
    except Exception as e:
        print(f"Error making call: {e}")
        return None
    finally:
        await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(make_outbound_call())
