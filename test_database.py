"""
Test script for database functionality
"""

from database import Database

def test_database():
    # Create database instance
    db = Database()
    
    # Test saving a document comparison record
    print("Testing document comparison record saving...")
    db.save_doc_comparison(
        "test-id-123",
        "uploads/test1.docx",
        "uploads/test2.docx",
        "results/test_result.xlsx"
    )
    
    # Test retrieving document comparison records
    print("Testing document comparison record retrieval...")
    comparisons = db.get_doc_comparisons()
    print(f"Found {len(comparisons)} comparison records")
    
    if comparisons:
        print("Latest comparison record:")
        print(comparisons[0])
    
    # Test saving a meeting transcription record
    print("\nTesting meeting transcription record saving...")
    db.save_meeting_transcription(
        "test-transcription-id-456",
        "uploads/meeting.mp3",
        "",  # Empty string instead of None
        "results/raw_transcript.docx",
        "results/processed_notes.docx"
    )
    
    # Test retrieving meeting transcription records
    print("Testing meeting transcription record retrieval...")
    transcriptions = db.get_meeting_transcriptions()
    print(f"Found {len(transcriptions)} transcription records")
    
    if transcriptions:
        print("Latest transcription record:")
        print(transcriptions[0])

if __name__ == "__main__":
    test_database()