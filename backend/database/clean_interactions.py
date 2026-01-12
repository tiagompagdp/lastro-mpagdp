'''
/backend/database/clean_interactions.py
-> Script to clean all interaction records from the database
'''

import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from database.setup import db
from database.models import Interaction

def clean_interactions():
    count = Interaction.query.count()
    print(f"Found {count} interaction(s) to delete")

    if count == 0:
        print("No interactions to delete. Database is already clean.")
        return

    try:
        Interaction.query.delete()
        db.session.commit()
        print("✓ All interactions deleted successfully")

    except Exception as e:
        db.session.rollback()
        print(f"✗ Error deleting interactions: {e}")
        raise

if __name__ == "__main__":
    from app import app

    with app.app_context():
        clean_interactions()
