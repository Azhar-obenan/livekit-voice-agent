#!/usr/bin/env python3
"""
Diagnostic script to check what's happening with calls
"""

import asyncio
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

async def diagnose_system():
    """Diagnose the calling system"""
    
    lkapi = api.LiveKitAPI(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET")
    )

    try:
        print("🔍 System Diagnosis")
        print("=" * 50)
        
        # Check rooms
        print("📋 Checking Rooms...")
        rooms = await lkapi.room.list_rooms(api.ListRoomsRequest())
        
        for room in rooms.rooms:
            if "real-estate" in room.name or "outbound-call" in room.name:
                print(f"   🏠 Room: {room.name}")
                print(f"      Participants: {room.num_participants}")
                print(f"      Created: {room.creation_time}")
                print(f"      Empty Timeout: {room.empty_timeout}")
                
                # Get room details
                participants = await lkapi.room.list_participants(
                    api.ListParticipantsRequest(room=room.name)
                )
                
                print(f"      Participant Details:")
                for p in participants.participants:
                    print(f"        - {p.identity} ({p.state}) - {p.kind}")
                    print(f"          Joined: {p.joined_at}")
                    print(f"          Tracks: {len(p.tracks)}")
        
        # Check workers
        print(f"\n🤖 Checking Workers...")
        # Note: Worker listing might not be available in all LiveKit versions
        
        print("\n" + "=" * 50)
        print("✅ Diagnosis complete")
        
    except Exception as e:
        print(f"❌ Error during diagnosis: {e}")
    finally:
        await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(diagnose_system())
