"""Command-line complaint manager for the CampusFix learning project."""

import storage


CATEGORIES = [
    "Electricity",
    "Water Supply",
    "Internet/Wi-Fi",
    "Classroom Maintenance",
    "Hostel Maintenance",
    "Library",
    "Other",
]

STATUSES = ["Pending", "In Progress", "Resolved"]


def get_non_empty_input(prompt):
    """Keep asking until the user enters text that is not only whitespace."""
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("This field cannot be empty. Please try again.")


def choose_category():
    """Display the category choices and return the selected category."""
    print("\nComplaint categories:")
    for number, category in enumerate(CATEGORIES, start=1):
        print(f"{number}. {category}")

    while True:
        selection = input("Choose a category number: ").strip()
        try:
            category_number = int(selection)
        except ValueError:
            print("Please enter a number from 1 to 7.")
            continue

        if 1 <= category_number <= len(CATEGORIES):
            return CATEGORIES[category_number - 1]
        print("Please choose a number from 1 to 7.")


def find_complaint(complaints, complaint_id):
    """Return a complaint whose ID matches, ignoring letter case."""
    wanted_id = complaint_id.strip().upper()
    for complaint in complaints:
        if complaint["complaint_id"].upper() == wanted_id:
            return complaint
    return None


def display_complaint(complaint):
    """Print all the information stored for one complaint."""
    print(f"\nComplaint ID: {complaint['complaint_id']}")
    print(f"Student name: {complaint['student_name']}")
    print(f"Category: {complaint['category']}")
    print(f"Description: {complaint['description']}")
    print(f"Location: {complaint['location'] or 'Not provided'}")
    print(f"Status: {complaint['status']}")


def register_complaint(complaints):
    """Collect complaint information, create an ID, and save the record."""
    print("\n--- Register a Complaint ---")
    student_name = get_non_empty_input("Student name: ")
    category = choose_category()
    description = get_non_empty_input("Complaint description: ")
    location = input("Location (optional): ").strip()

    existing_ids = [
        complaint.get("complaint_id", "")
        for complaint in complaints
    ]
    number = 100
    for existing_id in existing_ids:
        normalized_id = str(existing_id).strip().upper()
        if normalized_id.startswith("CF") and normalized_id[2:].isdigit():
            number = max(number, int(normalized_id[2:]))

    complaint_id = f"CF{number + 1}"
    while complaint_id.upper() in {str(value).upper() for value in existing_ids}:
        number += 1
        complaint_id = f"CF{number + 1}"

    complaint = {
        "complaint_id": complaint_id,
        "student_name": student_name,
        "category": category,
        "description": description,
        "location": location,
        "status": "Pending",
    }

    complaints.append(complaint)
    if storage.save_complaints(complaints):
        print(f"\nComplaint registered successfully. Your complaint ID is {complaint_id}.")
    else:
        complaints.pop()
        print("The complaint was not registered because it could not be saved.")


def view_all_complaints(complaints):
    """Show every complaint, or explain that there are none yet."""
    print("\n--- All Complaints ---")
    if not complaints:
        print("There are no complaints to display yet.")
        return

    for complaint in complaints:
        display_complaint(complaint)
        print("-" * 40)


def track_complaint(complaints):
    """Look up and display one complaint by its ID."""
    print("\n--- Track a Complaint ---")
    complaint_id = input("Enter the complaint ID: ").strip()
    complaint = find_complaint(complaints, complaint_id)
    if complaint is None:
        print(f"No complaint was found with ID '{complaint_id}'.")
        return
    display_complaint(complaint)


def update_complaint_status(complaints):
    """Change a complaint's status after checking its ID and selection."""
    print("\n--- Update Complaint Status ---")
    complaint_id = input("Enter the complaint ID: ").strip()
    complaint = find_complaint(complaints, complaint_id)
    if complaint is None:
        print(f"No complaint was found with ID '{complaint_id}'.")
        return

    print("\nAvailable statuses:")
    for number, status in enumerate(STATUSES, start=1):
        print(f"{number}. {status}")

    selection = input("Choose a status number: ").strip()
    try:
        status_number = int(selection)
    except ValueError:
        print("Invalid status selection. The status was not changed.")
        return

    if not 1 <= status_number <= len(STATUSES):
        print("Invalid status selection. The status was not changed.")
        return

    previous_status = complaint["status"]
    complaint["status"] = STATUSES[status_number - 1]
    if storage.save_complaints(complaints):
        print(f"Complaint {complaint['complaint_id']} status updated to {complaint['status']}.")
    else:
        complaint["status"] = previous_status
        print("The status was not changed because the update could not be saved.")


def view_statistics(complaints):
    """Count statuses and categories and print the resolution percentage."""
    print("\n--- Complaint Statistics ---")
    total = len(complaints)
    pending = 0
    in_progress = 0
    resolved = 0

    for complaint in complaints:
        if complaint["status"] == "Pending":
            pending += 1
        elif complaint["status"] == "In Progress":
            in_progress += 1
        elif complaint["status"] == "Resolved":
            resolved += 1

    resolution_percentage = resolved / total * 100 if total else 0
    print(f"Total complaints: {total}")
    print(f"Pending: {pending}")
    print(f"In Progress: {in_progress}")
    print(f"Resolved: {resolved}")

    print("\nComplaints by category:")
    for category in CATEGORIES:
        category_count = 0
        for complaint in complaints:
            if complaint["category"] == category:
                category_count += 1
        print(f"- {category}: {category_count}")

    print(f"\nResolution percentage: {resolution_percentage:.1f}%")


def main():
    """Load saved complaints and run the menu until the user exits."""
    complaints = storage.load_complaints()

    while True:
        print("\n========== CampusFix ==========")
        print("1. Register a Complaint")
        print("2. View All Complaints")
        print("3. Track Complaint by ID")
        print("4. Update Complaint Status")
        print("5. View Complaint Statistics")
        print("6. Exit")

        choice = input("Enter your choice: ").strip()
        if choice == "1":
            register_complaint(complaints)
        elif choice == "2":
            view_all_complaints(complaints)
        elif choice == "3":
            track_complaint(complaints)
        elif choice == "4":
            update_complaint_status(complaints)
        elif choice == "5":
            view_statistics(complaints)
        elif choice == "6":
            print("Thank you for using CampusFix. Goodbye!")
            break
        else:
            print("Invalid menu choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()
