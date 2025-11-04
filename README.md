# Healthcare AI Voice Assistant
## Confido AI - Take-Home Challenge

An AI-powered voice assistant for healthcare front-desk operations, built with OpenAI GPT-4o, Whisper, and ElevenLabs.

---

## 🎯 Overview

This system simulates a real healthcare clinic receptionist that can:
- **Schedule appointments** with availability checking
- **Verify insurance** coverage
- **Answer FAQs** about clinic information

The assistant uses:
- **OpenAI GPT-4o** for natural conversation
- **OpenAI Whisper** for speech-to-text
- **ElevenLabs** for high-quality text-to-speech
- **Function calling** for backend operations

---

## 📁 Project Structure

```
healthcare-voice-assistant/
├── src/
│   ├── conversation_engine.py    # LLM orchestration & function calling
│   ├── voice_handler.py          # STT/TTS integration
│   ├── appointment_service.py    # Appointment scheduling logic
│   └── insurance_service.py      # Insurance verification logic
├── data/
│   ├── appointments.json         # Mock appointment calendar
│   ├── insurance_providers.json  # Accepted insurance providers
│   └── clinic_info.json          # Clinic information
├── demos/                        # Complete demo recordings (3 MP3s)
├── recordings/                   # Individual audio clips from testing
├── main.py                       # Application entry point
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment variables template
├── README.md                     # This file
└── SYSTEM_DESIGN.md              # Architecture documentation

```

---

## 🚀 Setup Instructions

### 1. Prerequisites

- Python 3.9+
- OpenAI API key
- ElevenLabs API key

### 2. Installation

```bash
# Clone or extract the project
cd healthcare-voice-assistant

# Create virtual environment (recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure API Keys

```bash
# Copy the example env file
cp .env.example .env

# Edit .env and add your API keys
OPENAI_API_KEY=your_openai_api_key_here
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
ELEVENLABS_VOICE_ID=21m00Tcm4TlvDq8ikWAM  # Optional: Rachel voice (default)
```

**Getting API Keys:**
- OpenAI: https://platform.openai.com/api-keys
- ElevenLabs: https://elevenlabs.io/app/settings/api-keys

---



Create a `.env` file with:
```bash


```

> ⚠️ **Important Notes:**
> - These keys are for evaluation purposes only
> - For extended testing, please use your own API keys (see setup above)


---
## 🎮 Usage

### Run the Application

```bash
python main.py
```

### Available Modes

**1. Text Mode** - Interactive chat (no voice)
- Best for quick testing
- Type messages directly

**2. Voice Simulation - Appointment Scheduling**
- Simulates a complete appointment booking
- Generates audio recordings in `recordings/`

**3. Voice Simulation - Insurance Verification**
- Simulates insurance verification call
- Generates audio recordings

**4. Voice Simulation - No Available Slot**
- Handles edge case where requested time is unavailable
- Shows alternative slot offering

**5. Process Audio File**
- Upload your own audio file
- Full STT → LLM → TTS pipeline

---


---

## 🔊 Generated Recordings During Testing

When running voice simulations, individual audio clips are saved in the `recordings/` folder:
- `appointment_01_greeting.mp3`
- `appointment_02_response.mp3`
- ... etc.

These files show the step-by-step conversation flow.

---

## 🧠 How It Works

### Architecture

```
┌─────────────┐
│   User      │
│   Audio     │
└──────┬──────┘
       │
       ▼
┌─────────────────┐
│  Speech-to-Text │ (OpenAI Whisper)
│  (STT)          │
└──────┬──────────┘
       │
       ▼
┌─────────────────────────────┐
│  Conversation Engine        │
│  - GPT-4o for dialogue      │
│  - Function calling for:    │
│    * check_available_slots  │
│    * book_appointment       │
│    * verify_insurance       │
│    * get_clinic_info        │
└──────┬──────────────────────┘
       │
       ▼
┌─────────────────┐
│  Text-to-Speech │ (ElevenLabs)
│  (TTS)          │
└──────┬──────────┘
       │
       ▼
┌─────────────┐
│  Audio      │
│  Response   │
└─────────────┘
```

### Key Components

**1. Conversation Engine** (`conversation_engine.py`)
- Manages conversation state
- Uses GPT-4o with function calling
- Routes requests to appropriate services

**2. Voice Handler** (`voice_handler.py`)
- STT: OpenAI Whisper API
- TTS: ElevenLabs API with voice customization

**3. Appointment Service** (`appointment_service.py`)
- Mock calendar with available slots
- Booking logic with conflict checking
- Date formatting utilities

**4. Insurance Service** (`insurance_service.py`)
- Provider verification against accepted list
- Plan type checking (PPO, HMO, etc.)
- Informative responses for edge cases

---

## 🎯 Example Conversations

### Scenario 1: Appointment Scheduling

```
Assistant: Hello! Thank you for calling Riverside Medical Center. 
           I'm an AI assistant. How can I help you today?


User: I need to schedule an appointment
