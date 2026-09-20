import sys
import os

# Add backend directory to path
sys.path.append(os.path.dirname(__file__))

from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.exc import OperationalError

def test_connection():
    # Load the same configuration used by the application
    db_uri = settings.SQLALCHEMY_DATABASE_URI
    
    # Hide the password from output
    safe_uri = db_uri
    if ":" in db_uri and "@" in db_uri:
        # e.g., postgresql://user:pass@host/db
        parts = db_uri.split("@")
        user_pass = parts[0].split(":")
        if len(user_pass) >= 3:
            safe_uri = f"{user_pass[0]}:{user_pass[1]}:***@{parts[1]}"
            
    print(f"Attempting to connect to: {safe_uri}")
    
    try:
        from sqlalchemy import text
        engine = create_engine(db_uri)
        with engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            if result.fetchone()[0] == 1:
                print("SUCCESS: Connected to PostgreSQL and executed SELECT 1")
    except OperationalError as e:
        print("FAILED: Could not connect to PostgreSQL")
        print(f"Error details: {e}")
    except Exception as e:
        print("FAILED: An unexpected error occurred")
        print(f"Error details: {e}")

if __name__ == "__main__":
    test_connection()
