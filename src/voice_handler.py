import os
from openai import OpenAI
from elevenlabs import ElevenLabs, VoiceSettings
from pathlib import Path
import soundfile as sf
from typing import Optional
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceHandler:
    """Handles Speech-to-Text and Text-to-Speech operations"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.elevenlabs_client = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))
        self.voice_id = os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4TlvDq8ikWAM")
        
    def transcribe_audio(self, audio_file_path: str) -> str:
        """
        Transcribe audio file to text using OpenAI Whisper
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Transcribed text
        """
        try:
            with open(audio_file_path, "rb") as audio_file:
                transcript = self.openai_client.audio.transcriptions.create(
                    model="whisper-1",
                    file=audio_file,
                    language="en"
                )
            logger.info(f"Transcribed: {transcript.text}")
            return transcript.text
        except Exception as e:
            logger.error(f"Transcription error: {e}")
            raise
    
    def text_to_speech(self, text: str, output_path: Optional[str] = None) -> str:
        """
        Convert text to speech using ElevenLabs
        
        Args:
            text: Text to convert to speech
            output_path: Optional path to save audio file
            
        Returns:
            Path to generated audio file
        """
        try:
            logger.info(f"Generating speech for: {text[:50]}...")
            
            # Generate audio
            audio_generator = self.elevenlabs_client.text_to_speech.convert(
                voice_id=self.voice_id,
                text=text,
                model_id="eleven_monolingual_v1",
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                    style=0.0,
                    use_speaker_boost=True
                )
            )
            
            # Save audio to file
            if output_path is None:
                output_path = f"recordings/response_{hash(text)}.mp3"
            
            # Ensure directory exists
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            
            # Write audio data
            with open(output_path, "wb") as f:
                for chunk in audio_generator:
                    f.write(chunk)
            
            logger.info(f"Audio saved to: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"TTS error: {e}")
            raise
    
    def text_to_speech_stream(self, text: str):
        """
        Stream text to speech (for real-time playback)
        
        Args:
            text: Text to convert to speech
            
        Yields:
            Audio chunks
        """
        try:
            audio_generator = self.elevenlabs_client.text_to_speech.convert(
                voice_id=self.voice_id,
                text=text,
                model_id="eleven_monolingual_v1",
                voice_settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                )
            )
            
            for chunk in audio_generator:
                yield chunk
                
        except Exception as e:
            logger.error(f"TTS streaming error: {e}")
            raise
    
    def get_available_voices(self):
        """Get list of available ElevenLabs voices"""
        try:
            voices = self.elevenlabs_client.voices.get_all()
            return [(v.voice_id, v.name) for v in voices.voices]
        except Exception as e:
            logger.error(f"Error fetching voices: {e}")
            return []
