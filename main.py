#!/usr/bin/env python3
"""
Healthcare AI Voice Assistant
Main application file
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import logging

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.conversation_engine import ConversationEngine
from src.voice_handler import VoiceHandler

# Load environment variables
load_dotenv()

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class HealthcareVoiceAssistant:
    """Main application class for the healthcare voice assistant"""
    
    def __init__(self):
        logger.info("Initializing Healthcare Voice Assistant...")
        
        # Validate API keys
        self._validate_api_keys()
        
        # Initialize components
        self.conversation_engine = ConversationEngine()
        self.voice_handler = VoiceHandler()
        
        # Create recordings directory
        Path("recordings").mkdir(exist_ok=True)
        
        logger.info("Healthcare Voice Assistant initialized successfully!")
    
    def _validate_api_keys(self):
        """Validate required API keys are present"""
        required_keys = ["OPENAI_API_KEY", "ELEVENLABS_API_KEY"]
        missing_keys = [key for key in required_keys if not os.getenv(key)]
        
        if missing_keys:
            raise ValueError(
                f"Missing required API keys: {', '.join(missing_keys)}\n"
                "Please set them in your .env file"
            )
    
    def run_text_mode(self):
        """Run assistant in text mode (no voice)"""
        print("\n" + "="*60)
        print("Healthcare Voice Assistant - TEXT MODE")
        print("="*60)
        print("Type 'quit' or 'exit' to end the conversation\n")
        
        # Start conversation
        greeting = self.conversation_engine.get_greeting()
        print(f"Assistant: {greeting}\n")
        
        while True:
            # Get user input
            user_input = input("You: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['quit', 'exit', 'bye']:
                closing = "Thank you for calling Riverside Medical Center. Have a great day!"
                print(f"\nAssistant: {closing}")
                break
            
            # Get response from conversation engine
            response = self.conversation_engine.get_response(user_input)
            print(f"\nAssistant: {response}\n")
    
    def run_voice_mode_simulation(self, test_scenario: str = "appointment"):
        """
        Run a simulated voice conversation and save recordings
        
        Args:
            test_scenario: Type of scenario to simulate (appointment, insurance, faq)
        """
        print("\n" + "="*60)
        print("Healthcare Voice Assistant - VOICE MODE SIMULATION")
        print("="*60)
        print(f"Running scenario: {test_scenario}\n")
        
        # Define test scenarios
        scenarios = {
            "appointment": [
                "Hi, I'd like to schedule a check-up appointment",
                "Next Monday morning if possible",
                "Sure, what other mornings do you have available?",
                "Yes, Tuesday works. Dr. Smith please",
                "Yes, that time works perfectly for me",  
                "My name is Sarah Johnson and my phone is 555-0123",
                "It's just a routine annual physical",
                "Perfect, thank you so much!",
                "Thanks, have a great day!"
                
            ],
            "insurance": [
                "Hello, I'm calling to verify my insurance",
                "I have Blue Cross Blue Shield",
                "It's a PPO plan",
                "Great, thank you!",
                "That's all I needed",
                "Thanks, goodbye!"
            ],
            "appointment_no_slot": [
                "I need an appointment for November 3rd with Dr. Smith",
                "It's for back pain. How about November 4th at 9 AM?",
                "mmm...let me think, November 5th at 8 AM then?",
                "And...What about November 6th at 8 AM?",
                "Fine, November 7th at 1:30 PM",
                "Yes, please book it.",
                "My name is Noe Garcia, phone 555-9876",
                "Perfect, thank you!",
                "got it, goodbye!"
            ]
        }
        
        if test_scenario not in scenarios:
            print(f"Unknown scenario: {test_scenario}")
            return
        
        user_messages = scenarios[test_scenario]
        
        # Start conversation
        greeting = self.conversation_engine.get_greeting()
        print(f"Assistant: {greeting}")
        
        # Generate TTS for greeting
        greeting_audio = self.voice_handler.text_to_speech(
            greeting,
            f"recordings/{test_scenario}_01_greeting.mp3"
        )
        print(f"✓ Saved: {greeting_audio}\n")
        
        # Simulate conversation
        for idx, user_message in enumerate(user_messages, start=2):
            print(f"User: {user_message}")
            
            # Get AI response
            response = self.conversation_engine.get_response(user_message)
            print(f"Assistant: {response}")
            
            # Generate TTS for response
            response_audio = self.voice_handler.text_to_speech(
                response,
                f"recordings/{test_scenario}_{idx:02d}_response.mp3"
            )
            print(f"✓ Saved: {response_audio}\n")
        
        # Final closing
        closing = "Thank you for calling Riverside Medical Center. Have a great day!"
        print(f"Assistant: {closing}")
        closing_audio = self.voice_handler.text_to_speech(
            closing,
            f"recordings/{test_scenario}_final_closing.mp3"
        )
        print(f"✓ Saved: {closing_audio}\n")
        
        print("="*60)
        print(f"Scenario '{test_scenario}' completed!")
        print(f"Audio files saved in: recordings/")
        print("="*60)
    
    def process_audio_file(self, audio_file_path: str) -> str:
        """
        Process a single audio file (STT -> LLM -> TTS)
        
        Args:
            audio_file_path: Path to input audio file
            
        Returns:
            Path to output audio file
        """
        # Transcribe
        logger.info(f"Transcribing: {audio_file_path}")
        user_text = self.voice_handler.transcribe_audio(audio_file_path)
        print(f"User said: {user_text}")
        
        # Get response
        response_text = self.conversation_engine.get_response(user_text)
        print(f"Assistant: {response_text}")
        
        # Generate speech
        output_path = audio_file_path.replace(".wav", "_response.mp3")
        response_audio = self.voice_handler.text_to_speech(response_text, output_path)
        
        return response_audio


def main():
    """Main entry point"""
    
    print("\n" + "="*60)
    print("Healthcare AI Voice Assistant")
    print("Riverside Medical Center")
    print("="*60 + "\n")
    
    try:
        assistant = HealthcareVoiceAssistant()
        
        # Show menu
        print("Select mode:")
        print("1. Text Mode (interactive chat)")
        print("2. Voice Simulation - Appointment Scheduling")
        print("3. Voice Simulation - Insurance Verification")
        print("4. Voice Simulation - No Available Slot")
        print("5. Process Audio File (STT -> LLM -> TTS)")
        
        choice = input("\nEnter choice (1-5): ").strip()
        
        if choice == "1":
            assistant.run_text_mode()
        elif choice == "2":
            assistant.run_voice_mode_simulation("appointment")
        elif choice == "3":
            assistant.run_voice_mode_simulation("insurance")
        elif choice == "4":
            assistant.run_voice_mode_simulation("appointment_no_slot")
        elif choice == "5":
            audio_path = input("Enter path to audio file: ").strip()
            if Path(audio_path).exists():
                assistant.process_audio_file(audio_path)
            else:
                print(f"File not found: {audio_path}")
        else:
            print("Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
