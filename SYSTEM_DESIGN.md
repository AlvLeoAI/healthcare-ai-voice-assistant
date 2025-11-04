# System Design Document
## Healthcare AI Voice Assistant

**Author:** AI Solutions Engineer  
**Date:** October 29, 2025  
**Project:** Confido AI Take-Home Challenge

---

## 1. Executive Summary

This document describes the architecture, design decisions, and implementation details of an AI-powered voice assistant for healthcare front-desk operations. The system handles appointment scheduling, insurance verification, and general clinic inquiries through natural voice conversations.

**Key Achievements:**
- Full voice interaction pipeline (STT → LLM → TTS)
- Function calling for backend operations
- Natural conversation flow with context retention
- Edge case handling (unavailable slots, unknown insurance, etc.)

---

## 2. Architecture Overview

### 2.1 High-Level Architecture

```
User Audio Input
     ↓
Speech-to-Text (Whisper API)
     ↓
Conversation Engine (GPT-4o + Function Calling)
     ↓
Business Logic (Appointments, Insurance, Clinic Info)
     ↓
Response Generation (GPT-4o)
     ↓
Text-to-Speech (ElevenLabs)
     ↓
Audio Output
```

### 2.2 Component Interaction Flow

1. **User speaks** → Audio captured
2. **Whisper API** → Transcribes to text
3. **Conversation Engine** → 
   - Sends text to GPT-4o with conversation history
   - GPT-4o decides if function calling needed
   - If needed, executes function (check slots, book appointment, etc.)
4. **Response Generation** → GPT-4o generates natural language response
5. **ElevenLabs TTS** → Converts response to speech
6. **Audio Output** → Plays to user or saves to file

---

### 2.3 Demo Recordings

Three complete conversation demos are available in the `demos/` folder showcasing:
- Full appointment booking flow
- Insurance verification
- Edge case handling (no available slots)

See README.md for detailed demo descriptions.

---

## 3. Tech Stack & Tools

### 3.1 Core Technologies

| Component | Technology | Justification |
|-----------|-----------|---------------|
| **LLM** | OpenAI GPT-4o | Latest model with excellent function calling, natural conversation, fast response |
| **STT** | OpenAI Whisper API | Industry-leading accuracy, supports medical terminology |
| **TTS** | ElevenLabs | Superior voice quality and naturalness |
| **Backend** | Python 3.9+ | Rapid development, excellent AI/ML ecosystem |
| **Data Storage** | JSON Files | Simple for prototype, easy to inspect |

### 3.2 Why These Choices?

**GPT-4o over alternatives:**
- Best-in-class function calling
- Fast response times (important for voice)
- Excellent at maintaining conversation context
- Strong instruction following

**ElevenLabs over alternatives (Google TTS, Amazon Polly, Azure):**
- Most natural-sounding voices
- Emotional range for empathetic responses
- Easy API integration
- High-quality output

**Whisper API over alternatives (Deepgram, Google STT):**
- Best accuracy for general speech
- Good with medical terminology
- Same vendor as LLM (simpler billing/management)

---

## 4. Prompt Engineering Strategy

### 4.1 System Prompt Design

The system prompt is the foundation of assistant behavior:

```
You are an AI receptionist for Riverside Medical Center...

YOUR ROLE:
- Help patients schedule appointments
- Verify insurance information  
- Answer basic questions about the clinic

CONVERSATION RULES:
1. Ask ONE question at a time
2. Keep responses under 2 sentences
3. Confirm information before finalizing
4. Never provide medical advice
```

**Key Design Principles:**

1. **Clear Role Definition:** Assistant knows what it can/cannot do
2. **Conversation Rules:** Prevents verbose or confusing responses
3. **Tone Specification:** "Professional yet warm"
4. **Safety Guardrails:** No medical advice, emergency handling

### 4.2 Function Calling Design

Functions defined with precise schemas:

```python
{
    "name": "book_appointment",
    "description": "Book an appointment for a patient",
    "parameters": {
        "type": "object",
        "properties": {
            "patient_name": {...},
            "date": {"description": "YYYY-MM-DD format"},
            ...
        },
        "required": ["patient_name", "date", "time", "doctor_id"]
    }
}
```

**Benefits:**
- LLM knows exactly what data to collect
- Type safety and validation
- Clear contract between LLM and backend

### 4.3 Challenges & Solutions

**Challenge 1: Verbose Responses**
- Problem: Assistant gave long explanations
- Solution: Added "Keep responses under 2 sentences" rule
- Result: Natural conversational pace

**Challenge 2: Multiple Questions**
- Problem: "What's your name and when would you like to come in?"
- Solution: "Ask ONE question at a time" rule
- Result: Clearer conversations

**Challenge 3: Premature Booking**
- Problem: LLM would book before confirming all details
- Solution: Emphasize "collect ALL information step by step"
- Result: Proper information gathering

---

## 5. Data Model & Business Logic

### 5.1 Appointment System

**Available Slots Structure:**
```json
{
  "2025-11-03": {
    "dr_smith": ["09:00", "10:00", "14:00"],
    "dr_johnson": ["09:30", "11:00"]
  }
}
```

**Business Rules:**
1. Check slot availability before booking
2. Remove slot once booked
3. Generate unique appointment ID
4. Timestamp all bookings

### 5.2 Insurance Verification

**Data Structure:**
```json
{
  "accepted_providers": [
    {
      "name": "Blue Cross Blue Shield",
      "plans_accepted": ["PPO", "HMO", "EPO"],
      "requires_referral": false
    }
  ]
}
```

**Verification Logic:**
1. Case-insensitive provider matching
2. Check against accepted list
3. Verify plan type if provided
4. Return structured response

**Edge Cases:**
- Unknown provider → Offer to check with billing
- Provider accepted, plan unknown → Clarify plan types
- Provider not accepted → Polite rejection

---

## 6. Assumptions & Limitations

### 6.1 Current Assumptions

1. **Single Speaker**: One person at a time
2. **Clear Audio**: No heavy background noise
3. **English Only**: Whisper transcribes to English
4. **No Authentication**: No patient identity verification (prototype)
5. **Mock Data**: All data simulated, no real database
6. **Single Conversation**: No multi-call context

### 6.2 Known Limitations

**Technical:**
- No real-time streaming
- No interrupt handling
- Limited to ~200 token responses
- No conversation persistence

**Product:**
- Can't handle multiple appointments in one call
- No real EHR integration
- No SMS/email confirmations
- No transfer to human capability

**Security:**
- No HIPAA compliance measures
- No data encryption
- API keys in environment variables

### 6.3 Production Requirements

For production, we would need:

1. **HIPAA Compliance:**
   - End-to-end encryption
   - Audit logging
   - BAA with vendors
   - Data retention policies

2. **Real Integrations:**
   - EHR system (Epic, Cerner)
   - Real-time calendar via HL7/FHIR
   - Insurance verification API
   - Notification services (SMS/Email)

3. **Scalability:**
   - PostgreSQL/MongoDB instead of JSON
   - Redis caching
   - Load balancing
   - WebSocket for streaming

4. **Monitoring:**
   - Call quality metrics
   - Success rate tracking
   - Error tracking (Sentry)
   - A/B testing

---

## 7. Future Improvements

### 7.1 Short-term (1-2 weeks)

1. **Real-time Streaming:**
   - WebSocket bidirectional audio
   - Deepgram streaming STT
   - ElevenLabs streaming TTS

2. **Better NLU:**
   - Improved date/time parsing
   - Fuzzy slot matching
   - Multi-intent handling

3. **Voice Quality:**
   - Custom voice cloning
   - Noise reduction
   - Echo cancellation

### 7.2 Long-term (1-3 months)

1. **Production Infrastructure:**
   - Docker containerization
   - Kubernetes deployment
   - CI/CD pipeline

2. **Advanced AI:**
   - Fine-tuned model on healthcare data
   - RAG for clinic knowledge
   - Multi-agent architecture

3. **Analytics:**
   - Real-time monitoring dashboard
   - Success metrics
   - Patient satisfaction tracking

---

## 8. Conclusion

This prototype demonstrates functional AI voice automation for healthcare that successfully handles natural conversation, multi-step workflows, and edge cases.

The system proves viability of AI-powered front-desk automation while highlighting engineering considerations for production.

**Key Learnings:**
1. Prompt engineering is critical for consistent behavior
2. Function calling enables reliable backend integration
3. Voice quality significantly impacts user experience
4. Healthcare requires additional safety/compliance layers

---

## Appendix: Sample Conversation Flow

```
Assistant: Hello! Thank you for calling Riverside Medical Center. 
           I'm an AI assistant. How can I help you today?

User: I need to schedule an appointment