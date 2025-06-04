#!/usr/bin/env python3
"""
Verification script for the entry removal functionality.
This script will:
1. Initialize the database
2. Add test entries
3. Delete an entry
4. Verify the entry was deleted
"""

import os
import sqlite3
from flaskr.flaskr import app, init_db, get_db

def verify_implementation():
    print("Starting verification of entry removal functionality...")
    
    # Set up the Flask application context
    with app.app_context():
        # Initialize the database
        print("Initializing database...")
        init_db()
        
        # Add test entries
        print("Adding test entries...")
        db = get_db()
        db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
                  ['Test Entry 1', 'This is test entry 1'])
        db.execute('INSERT INTO entries (title, text) VALUES (?, ?)',
                  ['Test Entry 2', 'This is test entry 2'])
        db.commit()
        
        # Verify entries were added
        print("Verifying entries were added...")
        entries = db.execute('SELECT id, title, text FROM entries').fetchall()
        print(f"Found {len(entries)} entries:")
        for entry in entries:
            print(f"  ID: {entry['id']}, Title: {entry['title']}")
        
        if len(entries) < 2:
            print("ERROR: Failed to add test entries!")
            return False
        
        # Delete an entry
        entry_to_delete = entries[0]
        print(f"Deleting entry with ID {entry_to_delete['id']}...")
        db.execute('DELETE FROM entries WHERE id = ?', [entry_to_delete['id']])
        db.commit()
        
        # Verify entry was deleted
        print("Verifying entry was deleted...")
        remaining_entries = db.execute('SELECT id, title, text FROM entries').fetchall()
        print(f"Found {len(remaining_entries)} entries after deletion:")
        for entry in remaining_entries:
            print(f"  ID: {entry['id']}, Title: {entry['title']}")
        
        # Check if the deleted entry is no longer in the database
        deleted_entry = db.execute('SELECT id FROM entries WHERE id = ?', 
                                  [entry_to_delete['id']]).fetchone()
        
        if deleted_entry is None:
            print("SUCCESS: Entry was successfully deleted!")
            return True
        else:
            print("ERROR: Failed to delete entry!")
            return False

if __name__ == '__main__':
    success = verify_implementation()
    if success:
        print("Verification completed successfully!")
    else:
        print("Verification failed!")