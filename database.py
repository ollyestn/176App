import mysql.connector
from typing import List, Dict, Any
import os
from datetime import datetime

class Database:
    def __init__(self):
        self.host = "127.0.0.1"
        self.port = 3316
        self.user = "root"
        self.password = "root"
        self.database = "document_comparison"
        
        # Create database and tables if they don't exist
        self._initialize_database()
    
    def _get_connection(self):
        """Create and return a database connection"""
        return mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password,
            database=self.database
        )
    
    def _initialize_database(self):
        """Initialize database and create required tables"""
        # Connect without specifying database first
        conn = mysql.connector.connect(
            host=self.host,
            port=self.port,
            user=self.user,
            password=self.password
        )
        cursor = conn.cursor()
        
        # Create database if it doesn't exist
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {self.database}")
        cursor.close()
        conn.close()
        
        # Now connect to the specific database and create tables
        conn = self._get_connection()
        cursor = conn.cursor()
        
        # Create document comparisons table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS doc_comparisons (
                id VARCHAR(36) PRIMARY KEY,
                file1_path TEXT,
                file2_path TEXT,
                result_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id VARCHAR(36) DEFAULT NULL
            )
        """)
        
        # Create meeting transcriptions table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS meeting_transcriptions (
                id VARCHAR(36) PRIMARY KEY,
                audio_path TEXT,
                video_path TEXT,
                raw_text_path TEXT,
                processed_text_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                user_id VARCHAR(36) DEFAULT NULL
            )
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def save_doc_comparison(self, comparison_id: str, file1_path: str, file2_path: str, result_path: str, user_id: str = None):
        """Save document comparison record to database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO doc_comparisons (id, file1_path, file2_path, result_path, user_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (comparison_id, file1_path, file2_path, result_path, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_doc_comparisons(self, user_id: str = None) -> List[Dict[str, Any]]:
        """Retrieve document comparison history"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        
        if user_id:
            cursor.execute("""
                SELECT * FROM doc_comparisons 
                WHERE user_id = %s 
                ORDER BY created_at DESC
            """, (user_id,))
        else:
            cursor.execute("SELECT * FROM doc_comparisons ORDER BY created_at DESC")
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return results
    
    def save_meeting_transcription(self, transcription_id: str, audio_path: str, video_path: str, 
                                  raw_text_path: str, processed_text_path: str, user_id: str = None):
        """Save meeting transcription record to database"""
        conn = self._get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO meeting_transcriptions (id, audio_path, video_path, raw_text_path, processed_text_path, user_id)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (transcription_id, audio_path, video_path, raw_text_path, processed_text_path, user_id))
        
        conn.commit()
        cursor.close()
        conn.close()
    
    def get_meeting_transcriptions(self, user_id: str = None) -> List[Dict[str, Any]]:
        """Retrieve meeting transcription history"""
        conn = self._get_connection()
        cursor = conn.cursor(dictionary=True)
        
        if user_id:
            cursor.execute("""
                SELECT * FROM meeting_transcriptions 
                WHERE user_id = %s 
                ORDER BY created_at DESC
            """, (user_id,))
        else:
            cursor.execute("SELECT * FROM meeting_transcriptions ORDER BY created_at DESC")
        
        results = cursor.fetchall()
        cursor.close()
        conn.close()
        
        return results