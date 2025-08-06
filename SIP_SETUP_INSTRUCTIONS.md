# Real Estate SIP Calling Setup

This setup allows you to make outbound calls from `+1 308 251 4678` to `+923024491162` using your LiveKit voice agent.

## 🔧 Prerequisites

1. **SIP Provider Account**: You need an account with a SIP provider like:
   - Twilio
   - Telnyx  
   - Vonage
   - etc.

2. **Phone Number**: You need to have `+1 308 251 4678` provisioned with your SIP provider.

## 📝 Setup Steps

### Step 1: Configure SIP Credentials

Update your `.env` file with your SIP provider credentials:

```bash
# Replace these with your actual SIP provider details
SIP_USERNAME=your_actual_sip_username
SIP_PASSWORD=your_actual_sip_password  
SIP_PROVIDER_ADDRESS=sip.telnyx.com  # or your provider's SIP address
```

### Step 2: Run the Complete Setup

```bash
python complete_sip_setup.py
```

This script will:
- Create an outbound SIP trunk
- Configure it for your phone number
- Initiate a call from `+1 308 251 4678` to `+923024491162`

### Step 3: Start Your Agent (In Another Terminal)

```bash
python run_calling_agent.py
```

This starts your real estate agent that will handle the call conversation.

## 🎯 How It Works

1. **SIP Trunk**: Creates a connection to your SIP provider
2. **Outbound Call**: Initiates call from your number to target number
3. **Agent Connection**: Your LiveKit agent joins the call automatically
4. **Script Execution**: Agent follows your real estate calling script

## 📞 Call Flow

1. Call is initiated from `+1 308 251 4678`
2. Target number `+923024491162` receives the call
3. When answered, your agent starts the conversation:
   - "Hi [first_name], this is Elliott — I'm with a local realtor..."
4. Agent follows your complete real estate script
5. Handles objections and qualifies leads automatically

## 🔍 Monitoring

- Check LiveKit dashboard for call status
- Monitor agent logs for conversation flow
- View call metrics and recordings

## ⚠️ Important Notes

1. **SIP Provider**: You must have an active SIP provider account
2. **Phone Number**: `+1 308 251 4678` must be provisioned with your provider
3. **Costs**: Outbound calls will be charged by your SIP provider
4. **Compliance**: Ensure you comply with calling regulations in your area

## 🛠️ Troubleshooting

### "SIP credentials not configured"
- Update `SIP_USERNAME` and `SIP_PASSWORD` in `.env`

### "Trunk creation failed"  
- Check your SIP provider credentials
- Verify phone number is provisioned
- Check SIP provider address is correct

### "Call failed to connect"
- Verify target number format: `+923024491162`
- Check your SIP provider has international calling enabled
- Ensure sufficient account balance with SIP provider

## 📋 Files Created

- `complete_sip_setup.py` - Main setup and calling script
- `run_calling_agent.py` - Agent runner for call handling  
- `setup_trunk.py` - SIP trunk creation only
- `make_call.py` - Call initiation only

## 🎉 Success Indicators

When everything works correctly, you'll see:
- ✅ Trunk created successfully
- ✅ Call initiated successfully  
- 🤖 Agent connected to call
- 📞 Target number receives call from your agent

Your real estate agent will now automatically handle outbound calls following your configured script!
