import asyncio
import os
from dotenv import load_dotenv
from livekit import api
from livekit.protocol.sip import CreateSIPOutboundTrunkRequest, SIPOutboundTrunkInfo

load_dotenv()

async def create_outbound_trunk():
    """Create SIP outbound trunk for making calls"""
    
    lkapi = api.LiveKitAPI(
        url=os.getenv("LIVEKIT_URL"),
        api_key=os.getenv("LIVEKIT_API_KEY"),
        api_secret=os.getenv("LIVEKIT_API_SECRET")
    )

    # Create trunk configuration
    trunk = SIPOutboundTrunkInfo(
        name="Outbound Calling Trunk",
        address="sip.telnyx.com",  # You'll need to update this with your SIP provider
        numbers=["+13082514678"],  # Your outbound calling number
        auth_username=os.getenv("SIP_USERNAME", "your_sip_username"),
        auth_password=os.getenv("SIP_PASSWORD", "your_sip_password")
    )

    request = CreateSIPOutboundTrunkRequest(trunk=trunk)

    try:
        created_trunk = await lkapi.sip.create_sip_outbound_trunk(request)
        print(f"Successfully created trunk: {created_trunk.sip_trunk_id}")
        print(f"Trunk name: {created_trunk.name}")
        print(f"Trunk address: {created_trunk.address}")
        print(f"Trunk numbers: {created_trunk.numbers}")
        
        # Save trunk ID to environment file
        with open('.env', 'a') as f:
            f.write(f"\nSIP_OUTBOUND_TRUNK_ID={created_trunk.sip_trunk_id}\n")
        
        return created_trunk.sip_trunk_id
        
    except Exception as e:
        print(f"Error creating trunk: {e}")
        return None
    finally:
        await lkapi.aclose()

if __name__ == "__main__":
    asyncio.run(create_outbound_trunk())
