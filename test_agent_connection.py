#!/usr/bin/env python3
"""
Test script to create a room and see if agent connects
"""

import asyncio
import os
from dotenv import load_dotenv
from livekit import api

load_dotenv()

async def test_agent_connection():
    """Test if agent connects to a room"""
    
    lkapi = api.LiveKitAPI(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET")
    )

    try:
        print("🧪 Testing Agent Connection")
        print("=" * 50)
        
        # Create a test room
        room_name = "test-agent-room"
        print(f"📋 Creating test room: {room_name}")
        
        room_request = api.CreateRoomRequest(name=room_name)
        room = await lkapi.room.create_room(room_request)
        print(f"✅ Room created: {room.name}")
        
        # Wait a moment for agent to potentially join
        print("⏳ Waiting 10 seconds for agent to join...")
        await asyncio.sleep(10)
        
        # Check participants
        participants = await lkapi.room.list_participants(
            api.ListParticipantsRequest(room=room_name)
        )
        
        print(f"👥 Participants in room:")
        for p in participants.participants:
            print(f"   - {p.identity} ({p.state}) - {p.kind}")
            
        if len(participants.participants) > 0:
            print("✅ Agent connected successfully!")
        else:
            print("❌ No agent connected to room")
            
        # Clean up
        await lkapi.room.delete_room(api.DeleteRoomRequest(room=room_name))
        print(f"🧹 Cleaned up test room")
        
    except Exception as e:
        print(f"❌ Error during test: {e}")
    finally:
        await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(test_agent_connection())
