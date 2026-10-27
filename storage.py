"""JSON file storage helpers for the CampusFix learning project."""

import json
from pathlib import Path


DATA_FILE = Path(__file__).parent / "data" / "complaints.json"
REQUIRED_FIELDS = (
    "complaint_id",
    "student_name",
    "category",
    "description",
    "location",
    "status",
)


def _is_complaint_list(data):
    """Check that saved JSON has the list-and-dictionary shape the app uses."""
    if not isinstance(data, list):
        return False

    for complaint in data:
        if not isinstance(complaint, dict):
            return False
        for field in REQUIRED_FIELDS:
            if not isinstance(complaint.get(field), str):
                return False
    return True


def _create_empty_file():
    """Create an empty JSON list only when the file does not already exist."""
    DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
    try:
        with DATA_FILE.open("x", encoding="utf-8") as file:
            json.dump([], file, indent=4)
            file.write("\n")
    except FileExistsError:
        pass


def load_complaints():
    """Read complaints from JSON, returning an empty list after a clear error."""
    try:
        _create_empty_file()
        with DATA_FILE.open("r", encoding="utf-8") as file:
            complaints = json.load(file)
    except json.JSONDecodeError:
        print(
            f"Error: {DATA_FILE} contains invalid JSON. "
            "The original file has been left unchanged."
        )
        return []
    except (OSError, UnicodeError) as error:
        print(f"Error: Could not read complaint data: {error}")
        return []

    if not _is_complaint_list(complaints):
        print(
            f"Error: {DATA_FILE} does not contain a valid complaint list. "
            "The original file has been left unchanged."
        )
        return []
    return complaints


def save_complaints(complaints):
    """Save complaints unless the existing file is malformed or has bad data."""
    try:
        DATA_FILE.parent.mkdir(parents=True, exist_ok=True)
        if DATA_FILE.exists():
            with DATA_FILE.open("r", encoding="utf-8") as file:
                existing_data = json.load(file)
            if not _is_complaint_list(existing_data):
                print(
                    f"Error: Refusing to overwrite invalid complaint data in {DATA_FILE}."
                )
                return False

        if not _is_complaint_list(complaints):
            print("Error: Complaint data has an unexpected format and was not saved.")
            return False

        with DATA_FILE.open("w", encoding="utf-8") as file:
            json.dump(complaints, file, indent=4, ensure_ascii=False)
            file.write("\n")
    except json.JSONDecodeError:
        print(
            f"Error: Refusing to overwrite invalid JSON in {DATA_FILE}. "
            "The original file has been left unchanged."
        )
        return False
    except (OSError, UnicodeError) as error:
        print(f"Error: Could not save complaint data: {error}")
        return False

    return True
