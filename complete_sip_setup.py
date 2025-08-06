#!/usr/bin/env python3
"""
Complete SIP Setup for Outbound Calling
This script sets up everything needed to make calls from +13082514678 to +923024491162
"""

import asyncio
import os
import sys
from dotenv import load_dotenv
from livekit import api
from livekit.protocol.sip import (
    CreateSIPOutboundTrunkRequest, 
    SIPOutboundTrunkInfo,
    CreateSIPParticipantRequest,
    ListSIPOutboundTrunkRequest
)

load_dotenv()

class SIPCallManager:
    def __init__(self):
        self.lkapi = api.LiveKitAPI(
            url=os.getenv("LIVEKIT_URL"),
            api_key=os.getenv("LIVEKIT_API_KEY"),
            api_secret=os.getenv("LIVEKIT_API_SECRET")
        )
        self.from_number = "+13082514678"
        self.to_number = "+923024491162"
    
    async def list_existing_trunks(self):
        """List all existing outbound trunks"""
        try:
            trunks = await self.lkapi.sip.list_sip_outbound_trunk(
                ListSIPOutboundTrunkRequest()
            )
            print(f"Found {len(trunks.items)} existing trunk(s):")
            for trunk in trunks.items:
                print(f"  - ID: {trunk.sip_trunk_id}")
                print(f"    Name: {trunk.name}")
                print(f"    Address: {trunk.address}")
                print(f"    Numbers: {trunk.numbers}")
                print()
            return trunks.items
        except Exception as e:
            print(f"Error listing trunks: {e}")
            return []
    
    async def create_outbound_trunk(self):
        """Create or use existing outbound trunk"""
        
        # Check for existing trunks first
        existing_trunks = await self.list_existing_trunks()
        
        # Use existing trunk if available
        if existing_trunks:
            trunk_id = existing_trunks[0].sip_trunk_id
            print(f"Using existing trunk: {trunk_id}")
            return trunk_id
        
        # Create new trunk
        print("Creating new outbound trunk...")
        trunk = SIPOutboundTrunkInfo(
            name="Real Estate Outbound Trunk",
            address=os.getenv("SIP_PROVIDER_ADDRESS", "sip.telnyx.com"),
            numbers=[self.from_number],
            auth_username=os.getenv("SIP_USERNAME", "your_username"),
            auth_password=os.getenv("SIP_PASSWORD", "your_password")
        )

        request = CreateSIPOutboundTrunkRequest(trunk=trunk)

        try:
            created_trunk = await self.lkapi.sip.create_sip_outbound_trunk(request)
            trunk_id = created_trunk.sip_trunk_id
            
            print(f"✅ Successfully created trunk: {trunk_id}")
            print(f"   Name: {created_trunk.name}")
            print(f"   Address: {created_trunk.address}")
            print(f"   Numbers: {created_trunk.numbers}")
            
            # Update .env file with trunk ID
            self.update_env_file("SIP_OUTBOUND_TRUNK_ID", trunk_id)
            
            return trunk_id
            
        except Exception as e:
            print(f"❌ Error creating trunk: {e}")
            return None
    
    async def make_call(self, trunk_id):
        """Make the outbound call"""
        
        print(f"\n📞 Initiating call from {self.from_number} to {self.to_number}...")
        
        # Generate a unique room name for this call
        import time
        room_name = f"call-{int(time.time())}"
        
        request = CreateSIPParticipantRequest(
            sip_trunk_id=trunk_id,
            sip_call_to=self.to_number,
            sip_number=self.from_number,
            room_name=room_name,
            participant_identity="sip-caller",
            participant_name="SIP Caller",
            participant_metadata='{"call_type": "outbound", "purpose": "real_estate"}',
            dtmf="",
            play_ringtone=True,
            hide_phone_number=False
        )
        
        # Create room first to ensure it exists
        from livekit.api import CreateRoomRequest
        room_request = CreateRoomRequest(name=room_name)
        
        try:
            await self.livekit_api.room.create_room(room_request)
            print(f"✅ Room created: {room_name}")
        except Exception as e:
            print(f"⚠️  Room creation note: {e} (may already exist)")

        try:
            participant = await self.lkapi.sip.create_sip_participant(request)
            
            print(f"✅ Call initiated successfully!")
            print(f"   Participant ID: {participant.participant_id}")
            print(f"   Room Name: {participant.room_name}")
            print(f"   SIP Call ID: {participant.sip_call_id}")
            print(f"\n🎯 Your agent should now be connected to the call!")
            print(f"   The agent will follow the real estate script you configured.")
            
            return participant
            
        except Exception as e:
            print(f"❌ Error making call: {e}")
            return None
    
    def update_env_file(self, key, value):
        """Update .env file with new key-value pair"""
        env_file = ".env"
        
        # Read existing content
        with open(env_file, 'r') as f:
            lines = f.readlines()
        
        # Check if key already exists
        key_exists = False
        for i, line in enumerate(lines):
            if line.startswith(f"{key}="):
                lines[i] = f"{key}={value}\n"
                key_exists = True
                break
        
        # Add new key if it doesn't exist
        if not key_exists:
            lines.append(f"{key}={value}\n")
        
        # Write back to file
        with open(env_file, 'w') as f:
            f.writelines(lines)
        
        print(f"📝 Updated .env file: {key}={value}")
    
    async def run_complete_setup(self):
        """Run the complete setup process"""
        print("🚀 Starting Complete SIP Setup for Real Estate Calling")
        print("=" * 60)
        
        # Step 1: Create or get trunk
        trunk_id = await self.create_outbound_trunk()
        if not trunk_id:
            print("❌ Failed to create/get trunk. Exiting.")
            return False
        
        # Step 2: Make the call
        participant = await self.make_call(trunk_id)
        if not participant:
            print("❌ Failed to initiate call. Exiting.")
            return False
        
        print("\n" + "=" * 60)
        print("✅ Setup Complete! Your real estate agent is now calling.")
        print("📋 Next Steps:")
        print("   1. The agent will follow your configured script")
        print("   2. Monitor the call through LiveKit dashboard")
        print("   3. Check agent.py for the conversation logic")
        
        return True
    
    async def close(self):
        """Close the API connection"""
        await self.lkapi.aclose()

async def main():
    """Main function"""
    
    # Check environment variables
    required_vars = ["LIVEKIT_URL", "LIVEKIT_API_KEY", "LIVEKIT_API_SECRET"]
    missing_vars = [var for var in required_vars if not os.getenv(var)]
    
    if missing_vars:
        print(f"❌ Missing required environment variables: {missing_vars}")
        print("Please check your .env file.")
        return
    
    # Check SIP credentials
    sip_vars = ["SIP_USERNAME", "SIP_PASSWORD"]
    missing_sip = [var for var in sip_vars if not os.getenv(var) or os.getenv(var) == f"your_{var.lower()}"]
    
    if missing_sip:
        print("⚠️  Warning: SIP credentials not configured properly.")
        print("Please update these in your .env file:")
        for var in missing_sip:
            print(f"   {var}=your_actual_{var.lower()}")
        print("\nYou'll need to get these from your SIP provider (Twilio, Telnyx, etc.)")
        
        response = input("\nContinue anyway? (y/N): ")
        if response.lower() != 'y':
            return
    
    # Run the setup
    manager = SIPCallManager()
    try:
        success = await manager.run_complete_setup()
        if success:
            print("\n🎉 All done! Your real estate calling system is ready.")
        else:
            print("\n❌ Setup failed. Please check the errors above.")
    finally:
        await manager.close()

if __name__ == "__main__":
    asyncio.run(main())
