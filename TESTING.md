# Testing Guide

## Quick Setup Verification

Run this first to verify everything is installed correctly:

```bash
python test_setup.py
```

This will check:
- Python version (3.9+)
- Required packages installed
- Data files present
- API keys configured

---

## Running Test Scenarios

### 1. Text Mode (Interactive Chat)

Best for quick testing without voice:

```bash
python main.py
# Select option 1
```

Example conversation:
```
You: Hi
Assistant: Hello! Thank you for calling Riverside Medical Center...

You: I need an appointment
Assistant: I'd be happy to help you schedule an appointment. May I have your name, please?

You: John Smith
Assistant: Thank you, John. What day works best for you?

You: Next Monday
Assistant: Let me check our available times for Monday, November 3rd...
```

### 2. Voice Simulation - Appointment Booking

Generates audio files showing complete appointment flow:

```bash
python main.py
# Select option 2
```

This creates audio files in `recordings/`:
- `appointment_01_greeting.mp3`
- `appointment_02_response.mp3`
- ... etc.

### 3. Voice Simulation - Insurance Verification

```bash
python main.py
# Select option 3
```

Creates audio files for insurance verification scenario.

### 4. Voice Simulation - Edge Case (No Available Slot)

Shows how system handles when requested time is unavailable:

```bash
python main.py
# Select option 4
```

### 5. Process Your Own Audio File

If you have a .wav or .mp3 file:

```bash
python main.py
# Select option 5
# Enter path to your audio file
```

---

## Expected Behaviors

### Successful Appointment Booking
✓ Assistant greets caller
✓ Identifies need (appointment scheduling)
✓ Collects patient name
✓ Asks for preferred date
✓ Checks availability using function call
✓ Offers available slots
✓ Collects doctor preference
✓ Confirms all details
✓ Books appointment
✓ Provides confirmation

### Insurance Verification
✓ Identifies insurance inquiry
✓ Asks for provider name
✓ Optionally asks for plan type
✓ Verifies against accepted list
✓ Provides clear acceptance/rejection
✓ Mentions referral requirements if applicable

### Edge Cases Handled
✓ Unavailable time requested → Offers alternatives
✓ Unknown provider → Offers to check with billing
✓ Unclear input → Asks for clarification
✓ Medical advice request → Politely declines, stays in scope

---

## Manual Testing Checklist

### Appointment Scheduling

- [ ] Can book appointment with available slot
- [ ] Handles unavailable slot gracefully
- [ ] Collects all required information
- [ ] Confirms details before booking
- [ ] Provides appointment confirmation

### Insurance Verification

- [ ] Verifies accepted provider correctly
- [ ] Handles unknown provider
- [ ] Checks plan type when provided
- [ ] Mentions referral requirements
- [ ] Provides copay information

### Clinic Information

- [ ] Answers location questions
- [ ] Provides hours of operation
- [ ] Lists available doctors
- [ ] Describes services offered

### Conversation Quality

- [ ] Responses are natural and friendly
- [ ] Asks one question at a time
- [ ] Doesn't provide medical advice
- [ ] Handles misunderstandings gracefully
- [ ] Maintains professional tone

---

## Troubleshooting

### "Missing API key" error
Make sure you copied `.env.example` to `.env` and added your keys:
```bash
cp .env.example .env
# Edit .env and add your API keys
```

### "Module not found" error
Install dependencies:
```bash
pip install -r requirements.txt
```

### Audio quality issues
Try different ElevenLabs voices by changing `ELEVENLABS_VOICE_ID` in `.env`:
- Rachel (default): `21m00Tcm4TlvDq8ikWAM`
- Adam: `pNInz6obpgDQGcFmaJgB`
- Bella: `EXAVITQu4vr4xnSDxMaL`

### Slow responses
This is normal - the system makes multiple API calls:
1. Whisper transcription (~1-2s)
2. GPT-4o response (~2-3s)
3. ElevenLabs TTS (~1-2s)

Total latency: 4-7 seconds per exchange

---

## Performance Metrics

Expected performance:
- **Transcription accuracy**: 95%+ (Whisper)
- **Response latency**: 4-7 seconds
- **Voice quality**: High (ElevenLabs)
- **Conversation success rate**: 85%+ for standard scenarios

---

## Next Steps

After testing:
1. Review generated audio files in `recordings/`
2. Check system logs for any errors
3. Read `SYSTEM_DESIGN.md` for architecture details
4. Explore code in `src/` directory
