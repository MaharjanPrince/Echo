import os
from datetime import datetime

# Path to the journal file (can be changed to a database)
JOURNAL_FILE_PATH = 'journal_entries.txt'

def save_journal_entry(book_id: str, reflection: str) -> None:
    """
    Saves a journal entry (reflection) with a timestamp and book_id to a file.

    Args:
    - book_id (str): The ID of the book (used as a unique identifier).
    - reflection (str): The philosophical reflection generated for the book.

    Returns:
    - None
    """
    # Ensure the directory exists
    os.makedirs(os.path.dirname(JOURNAL_FILE_PATH), exist_ok=True)
    
    # Get the current timestamp
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Format the entry with book_id and timestamp
    formatted_entry = f"{timestamp} - Book ID: {book_id}\n{reflection}\n\n"
    
    # Save the entry to the journal file
    with open(JOURNAL_FILE_PATH, 'a') as journal_file:
        journal_file.write(formatted_entry)


def read_journal_entries() -> str:
    """
    Reads all journal entries from the journal file.

    Returns:
    - str: The entire content of the journal file.
    """
    if os.path.exists(JOURNAL_FILE_PATH):
        with open(JOURNAL_FILE_PATH, 'r') as journal_file:
            return journal_file.read()
    return "No journal entries found."

