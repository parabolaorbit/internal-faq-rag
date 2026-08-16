from datetime import datetime

def get_current_date() -> str:
    """Get the current date in YYYY-MM-DD format."""
    return "{ \"answer\": \"" + datetime.now().strftime("%Y-%m-%d") + "\", \"confidence\": 1.0, \"needs_more_information\": false }"