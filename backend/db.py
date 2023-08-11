#!/usr/bin/env python3
"""
Results saving and loading
"""

import os

# DB library
import sqlite3

# Setup tasks
## Create ./data directory if it doesn't exist
base_folder = os.path.dirname(__file__)


class DataBase:
    """
    Database wrapper
    """
    
    def __init__(self, db_name: str):
        """
        Create a new database wrapper
        """
        
        self.db_name = db_name
        
        self.db_path = os.path.join(base_folder, 'data', f'{db_name}.db')
        
        self.db = sqlite3.connect(self.db_path)
        
        self.cursor = self.db.cursor()
        
    def add_survey(self, survey: str, questions: list):
        """
        Add a survey to the database
        """
        
        self.cursor.execute(
            f"""
            CREATE TABLE IF NOT EXISTS {survey} (
                id INTEGER PRIMARY KEY,
                {', '.join([f'q{i} INTEGER' for i, _ in enumerate(questions)])},
                reference TEXT
            )
            """
        )
        
        self.db.commit()
        
    def add_result(self, survey: str, questions, reference: str=None):
        """
        Add a user response to the database
        """
        
        self.cursor.execute(
            f"""
        INSERT INTO {survey} (
            {', '.join([f'q{i}' for i, _ in enumerate(questions)])},
            reference
        )
        VALUES (
            {', '.join([str(q) for q in questions])},
            '{reference}'
        )
        """
        )
        
        self.db.commit()
        
    def __contains__(self, survey: str) -> bool:
        """
        Check if the given survey exists
        """
        
        self.cursor.execute(
            f"""
            SELECT name
            FROM sqlite_master
            WHERE type='table' AND name='{survey}'
            """
        )
        
        return len(self.cursor.fetchall()) > 0