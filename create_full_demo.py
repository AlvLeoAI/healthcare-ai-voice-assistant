#!/usr/bin/env python3
"""
Create Full Demo Audio Files - Simplified Version
Generates user voice audio files that can be combined with assistant responses
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from elevenlabs import ElevenLabs, VoiceSettings
import logging

# Load environment variables
load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class FullDemoCreator:
    """Creates user voice audio files for complete conversations"""
    
    def __init__(self):
        self.elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        
        # Different voice for user (female voice)
        self.user_voice_id = "EXAVITQu4vr4xnSDxMaL"  # Sarah (female)
        
    def generate_user_audio(self, text: str, output_path: str) -> str:
        """Generate TTS for user speech"""
        logger.info(f"Generating user speech: {text[:50]}...")
        
        audio_generator = self.elevenlabs_client.text_to_speech.convert(
            voice_id=self.user_voice_id,
            text=text,
            model_id="eleven_monolingual_v1",
            voice_settings=VoiceSettings(
                stability=0.6,
                similarity_boost=0.8,
                style=0.0,
                use_speaker_boost=True
            )
        )
        
        # Save audio
        with open(output_path, "wb") as f:
            for chunk in audio_generator:
                f.write(chunk)
        
        logger.info(f"✓ User audio saved: {output_path}")
        return output_path
    
    def create_user_audios(self, user_texts: list, prefix: str):
        """
        Generate all user audio files for a conversation
        
        Args:
            user_texts: List of user statements
            prefix: Filename prefix (e.g., 'appointment', 'insurance')
        """
        logger.info(f"\n{'='*60}")
        logger.info(f"Creating user audio files for: {prefix}")
        logger.info(f"{'='*60}\n")
        
        # Create output directory
        output_dir = Path("recordings/user_voice")
        output_dir.mkdir(exist_ok=True)
        
        generated_files = []
        
        for idx, text in enumerate(user_texts):
            if not text:  # Skip empty texts
                continue
                
            output_path = output_dir / f"{prefix}_user_{idx+1:02d}.mp3"
            self.generate_user_audio(text, str(output_path))
            generated_files.append(str(output_path))
        
        logger.info(f"\n{'='*60}")
        logger.info(f"✓ Generated {len(generated_files)} user audio files")
        logger.info(f"{'='*60}\n")
        
        return generated_files


def create_appointment_demo():
    """Create user audio files for appointment scheduling demo"""
    
    user_texts = [
        "Hi I'm Sarah, I'd like to schedule an appointment",
        "Well, let me think... I need to see a doctor for check-out",
        "I don't have a preference",
        "Next Tuesday would be great",
        "Sure, can you find the next available morning",
        "Yes, could it be 11:30 AM?",
        "Dr. Smith please",
        "555-0123",
        "No, thank you",
        "Thanks",
    ]
    
    creator = FullDemoCreator()
    return creator.create_user_audios(user_texts, "appointment")


def create_insurance_demo():
    """Create user audio files for insurance verification demo"""
    
    user_texts = [
        "Hi! I just wanted to check if my insurance is accepted there",
        "It's Blue Cross Blue Shield",
        "Yeah, it's a PPO plan",
        "Awesome, thanks so much for confirming! I don't need to schedule an appointment — I just wanted to make sure my insurance was accepted. Thanks again!",
        "Thanks for your help!",
    ]
    
    creator = FullDemoCreator()
    return creator.create_user_audios(user_texts, "insurance")


def create_edge_case_demo():
    """Create user audio files for edge case demo"""
    
    user_texts = [
        "Hi, I was hoping to schedule an appointment for tomorrow",
        "I've been having some back pain and I'd like to see a doctor about it",
        "Definitely, Dr. Johnson",
        "Sure, what times do you have on Thursday?",
        "Friday could work...do you have anything around 2 PM?",
        "Let's check next week then",
        "Yes, please. You can reach me at 555-9876 if you need to confirm anything",
        "Sure...Sarah Johnson. Thanks so much for your help!",
        "got it, thanks",
    ]
    
    creator = FullDemoCreator()
    return creator.create_user_audios(user_texts, "edge_case")


def main():
    """Main entry point"""
    
    print("\n" + "="*60)
    print("User Voice Audio Generator")
    print("="*60 + "\n")
    
    # Check API key
    if not os.getenv("ELEVENLABS_API_KEY"):
        print("❌ ELEVENLABS_API_KEY not found in .env")
        sys.exit(1)
    
    print("This will generate USER voice audio files for 3 scenarios.")
    print("You can then combine them with assistant responses using")
    print("a free online tool or audio editor.\n")
    
    input("Press Enter to continue...")
    
    try:
        # Create all user audio files
        print("\n📞 Creating user audio for: Appointment Scheduling...")
        files1 = create_appointment_demo()
        
        print("\n📞 Creating user audio for: Insurance Verification...")
        files2 = create_insurance_demo()
        
        print("\n📞 Creating user audio for: Edge Case...")
        files3 = create_edge_case_demo()
        
        print("\n" + "="*60)
        print("✅ All user audio files created successfully!")
        print("="*60)
        print("\nGenerated files in: recordings/user_voice/")
        print(f"  - Appointment: {len(files1)} files")
        print(f"  - Insurance: {len(files2)} files")
        print(f"  - Edge Case: {len(files3)} files")
        
        print("\n" + "="*60)
        print("📝 NEXT STEPS:")
        print("="*60)
        print("\nTo create complete demo files:")
        print("\n1. Go to: https://clideo.com/merge-audio")
        print("\n2. Upload files in this order for each demo:")
        print("\n   APPOINTMENT DEMO:")
        print("   - recordings/user_voice/appointment_user_01.mp3")
        print("   - recordings/appointment_01_greeting.mp3")
        print("   - recordings/user_voice/appointment_user_02.mp3")
        print("   - recordings/appointment_02_response.mp3")
        print("   - ... (continue pattern)")
        print("\n   INSURANCE DEMO:")
        print("   - recordings/user_voice/insurance_user_01.mp3")
        print("   - recordings/insurance_01_greeting.mp3")
        print("   - ... (continue pattern)")
        print("\n   EDGE CASE DEMO:")
        print("   - recordings/user_voice/edge_case_user_01.mp3")
        print("   - recordings/appointment_no_slot_01_greeting.mp3")
        print("   - ... (continue pattern)")
        print("\n3. Export as MP3 with names:")
        print("   - DEMO_1_Appointment_Full.mp3")
        print("   - DEMO_2_Insurance_Full.mp3")
        print("   - DEMO_3_EdgeCase_Full.mp3")
        print("\n" + "="*60 + "\n")
        
    except Exception as e:
        logger.error(f"Error creating user audio: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
