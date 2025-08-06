#!/usr/bin/env python3
"""
Call Monitoring Script
Monitor active SIP calls and agent status
"""

import asyncio
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

async def monitor_calls():
    """Monitor active SIP calls"""
    
    lkapi = api.LiveKitAPI(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET")
    )

    try:
        print("🔍 Monitoring SIP Calls...")
        print("=" * 50)
        
        # List rooms to see active calls
        print("📞 Checking for active call rooms...")
        
        # List rooms
        print(f"\n🏠 Checking Rooms...")
        rooms = await lkapi.room.list_rooms(api.ListRoomsRequest())
        
        if rooms.rooms:
            for room in rooms.rooms:
                if "real-estate" in room.name or "outbound-call" in room.name:
                    print(f"   Room: {room.name}")
                    print(f"   Participants: {room.num_participants}")
                    print(f"   Created: {room.creation_time}")
        
        print("\n" + "=" * 50)
        print("✅ Monitoring complete")
        
    except Exception as e:
        print(f"❌ Error monitoring calls: {e}")
    finally:
        await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(monitor_calls())
