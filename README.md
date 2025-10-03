# Document Comparison and Meeting Transcription App

This is a FastAPI web application that provides two main features:
1. Document comparison: Compare two Word documents and generate a detailed comparison report
2. Meeting transcription: Transcribe audio/video recordings and process the content with AI

## Features

### Document Comparison
- Upload two DOC/DOCX files for comparison
- Generate a detailed comparison report in Excel format
- View and download historical comparisons
- Store all data in a MySQL database

### Meeting Transcription
- Upload MP3 audio or MP4 video files
- Transcribe meetings using Whisper
- Process transcriptions with AI to organize content
- Generate both raw and processed versions in Word format
- View and download historical transcriptions

## Installation

1. Clone the repository
2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Make sure MySQL is running on localhost:3316 with username/password: root/root
4. Run the application:
   ```
   python main.py
   ```

## Usage

1. Navigate to `http://localhost:8000` in your browser
2. Use the navigation buttons to access document comparison or meeting transcription features
3. For document comparison:
   - Upload two DOC/DOCX files
   - Click "Compare Documents"
   - Download the Excel comparison report
4. For meeting transcription:
   - Upload an MP3 or MP4 file
   - Click "Transcribe Meeting"
   - Download both raw and processed transcripts

## Project Structure

```
├── main.py                 # Main FastAPI application
├── database.py             # MySQL database connection and operations
├── doc_compare.py          # Document comparison logic
├── meeting_transcribe.py   # Meeting transcription logic
├── doc_checker.py          # Document comparison implementation (placeholder)
├── video_transcription.py  # Transcription implementation (placeholder)
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── templates/              # HTML templates
│   ├── base.html           # Base template
│   ├── index.html          # Home page
│   ├── login.html          # Login page
│   ├── doc_compare.html    # Document comparison page
│   └── meeting.html        # Meeting transcription page
├── static/                 # Static files
│   └── style.css           # CSS styles
├── uploads/                # Uploaded files (created at runtime)
├── results/                # Processing results (created at runtime)
```

## Database Schema

The application automatically creates two tables in the MySQL database:

1. `doc_comparisons`: Stores document comparison records
2. `meeting_transcriptions`: Stores meeting transcription records

## Customization

To implement the actual document comparison functionality, replace the placeholder code in `doc_checker.py`.
To implement the actual transcription functionality, replace the placeholder code in `video_transcription.py`.

## License

This project is licensed under the MIT License.