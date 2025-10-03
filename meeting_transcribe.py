import os
from typing import List, Dict, Any, Optional
from database import Database

# Try to import the video_transcription module
try:
    import video_transcription
    HAS_VIDEO_TRANSCRIPTION = True
except ImportError:
    video_transcription = None  # Explicitly set to None
    HAS_VIDEO_TRANSCRIPTION = False
    print("Warning: video_transcription.py not found. Transcription will be simulated.")

class MeetingTranscribe:
    def __init__(self):
        self.db = Database()
    
    def transcribe_and_process(self, audio_path: Optional[str], video_path: Optional[str], raw_text_path: str, processed_text_path: str) -> bool:
        """
        Transcribe audio/video and process the text
        Returns True if successful, False otherwise
        """
        try:
            # Use the actual video_transcription module if available
            if HAS_VIDEO_TRANSCRIPTION and video_transcription is not None:
                # Choose the available file path (audio or video)
                input_file = audio_path or video_path
                if input_file:
                    result = video_transcription.process(input_file, raw_text_path, processed_text_path)
                    return result is not None  # Assuming process returns something on success
            # Simulate transcription for development
            self._simulate_transcription(audio_path or "", video_path or "", raw_text_path, processed_text_path)
            return True
        except Exception as e:
            print(f"Error during transcription: {e}")
            return False
    
    def _simulate_transcription(self, audio_path: str, video_path: str, raw_text_path: str, processed_text_path: str):
        """Simulate transcription by creating sample Word documents"""
        # Create raw text document
        with open(raw_text_path.replace('.docx', '.txt'), 'w') as f:
            f.write("Raw Transcription\n")
            f.write("================\n")
            f.write("This is a simulated raw transcription of the meeting.\n")
            f.write("In a real implementation, this would contain the actual transcribed text.\n")
        
        # Rename to .docx extension
        os.rename(raw_text_path.replace('.docx', '.txt'), raw_text_path)
        
        # Create processed text document
        with open(processed_text_path.replace('.docx', '.txt'), 'w') as f:
            f.write("Processed Meeting Notes\n")
            f.write("======================\n")
            f.write("This is a simulated processed version of the meeting transcription.\n")
            f.write("In a real implementation, this would contain the AI-processed meeting notes.\n")
        
        # Rename to .docx extension
        os.rename(processed_text_path.replace('.docx', '.txt'), processed_text_path)
    
    def save_record(self, transcription_id: str, audio_path: Optional[str], video_path: Optional[str], 
                   raw_text_path: str, processed_text_path: str, user_id: Optional[str] = None):
        """Save transcription record to database"""
        self.db.save_meeting_transcription(transcription_id, audio_path or "", video_path or "", raw_text_path, processed_text_path, user_id or "")

    def get_transcription_by_id(self, transcription_id: str) -> Dict[str, Any]:
        """Get a specific transcription by ID"""
        return self.db.get_meeting_transcription_by_id(transcription_id)

    def get_history(self, user_id: Optional[str] = None) -> List[Dict[str, Any]]:
        """Get transcription history"""
        return self.db.get_meeting_transcriptions(user_id or "")