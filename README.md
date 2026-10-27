# CampusFix — College Complaint Management System

CampusFix is a beginner-friendly command-line application for registering college facility complaints and checking their progress. It uses Python's built-in JSON support to keep complaint records between runs.

This is an educational project, not a production service. **Administrator authentication is not implemented**: anyone who can run the program can choose the status-update menu option.

## The problem

Students may report broken fans, water supply problems, Wi-Fi outages, damaged furniture, and other campus issues verbally or through informal messages. Those reports can be difficult to track. CampusFix demonstrates a simple way to record each report with an ID and a status.

## Project objectives

- Practice Python fundamentals in a complete, runnable program.
- Register complaints and give each one a unique ID.
- Find complaints and update their progress.
- Save complaint data locally in a JSON file.
- Summarize complaint counts and resolution progress.

## Features

- Repeating six-option menu with invalid-choice handling.
- Complaint categories: Electricity, Water Supply, Internet/Wi-Fi, Classroom Maintenance, Hostel Maintenance, Library, and Other.
- Required student name and description, plus optional location.
- Generated IDs such as `CF101`.
- Case-insensitive complaint lookup.
- Statuses: Pending, In Progress, and Resolved.
- Counts by status and category, plus resolution percentage.
- Local JSON persistence, with helpful handling for missing or malformed files.

## Technologies and Python concepts

The project uses only the Python standard library: `json` for data storage and `pathlib` for file paths and directory creation.

Concepts demonstrated:

- Variables, strings, numbers, lists, and dictionaries.
- `input()` and `print()` for command-line interaction.
- Converting menu text to integers and handling conversion errors.
- `if` / `elif` / `else` decisions and `for` / `while` loops.
- Functions with parameters and return values.
- Reading and writing files, JSON, and exception handling.

There are no external packages, database, web interface, AI features, or classes.

## Project structure

```text
campusfix-cli/
├── main.py
├── storage.py
├── .gitignore
├── README.md
└── data/
    ├── .gitkeep
    └── complaints.json   # created automatically the first time the app runs
```

`main.py` contains the menu and complaint features. `storage.py` handles JSON file loading and saving. The `data/` directory is created automatically if it is missing.

## Requirements and installation

- Python 3.8 or newer.
- No package installation is required.

Open the project folder in VS Code. In VS Code, choose **Terminal → New Terminal**, then run the following command from the folder containing `main.py`:

```text
python main.py
```

On some Windows installations, use:

```text
py main.py
```

The application creates `data/complaints.json` with an empty list the first time it starts.

## Sample terminal session

```text
========== CampusFix ==========
1. Register a Complaint
2. View All Complaints
3. Track Complaint by ID
4. Update Complaint Status
5. View Complaint Statistics
6. Exit
Enter your choice: 1

--- Register a Complaint ---
Student name: Asha

Complaint categories:
1. Electricity
2. Water Supply
3. Internet/Wi-Fi
4. Classroom Maintenance
5. Hostel Maintenance
6. Library
7. Other
Choose a category number: 1
Complaint description: The fan is not working.
Location (optional): Room 204

Complaint registered successfully. Your complaint ID is CF101.
```

## How data is stored

Complaints are saved as a JSON list in `data/complaints.json`, next to the program. Each list item is a dictionary containing the complaint ID, student name, category, description, location, and status. The file is loaded at startup and updated after a complaint is registered or its status is changed.

If the file is missing, CampusFix creates it. If the file contains malformed JSON or data with the wrong structure, the program displays an error and does not replace that original file. In that case, saving is refused until the file is repaired; back up the file before making any manual changes.

## Limitations

- Administrator authentication and role permissions are not implemented.
- Data is stored in a local file, not a database or shared service.
- The program is intended for one local user at a time; it does not coordinate simultaneous changes.
- There is no graphical or web interface, email notification, or automatic complaint assignment.
- Anyone with access to the project folder can read or edit its complaint data.

## Manual testing checklist

- [ ] Register a valid complaint and note its generated ID.
- [ ] Submit a blank student name; confirm the program asks again.
- [ ] Submit a blank description; confirm the program asks again.
- [ ] Enter letters and an out-of-range number for category selection; confirm they are rejected.
- [ ] View all complaints with no saved complaints; confirm a helpful empty message appears.
- [ ] Track an existing complaint using a lowercase ID.
- [ ] Track a nonexistent complaint ID.
- [ ] Update a complaint to In Progress and confirm the new status.
- [ ] Update a complaint to Resolved and confirm the new status.
- [ ] Enter letters and an out-of-range number for status selection; confirm the status is unchanged.
- [ ] View statistics with no complaints; confirm there is no division-by-zero error.
- [ ] Exit and restart; confirm the saved complaint and status remain available.
- [ ] Enter letters and an invalid number at the main menu.
- [ ] Rename or temporarily move `data/complaints.json`; restart and confirm the file is recreated as an empty list.
- [ ] Back up `data/complaints.json`, replace its contents temporarily with invalid JSON, and restart; confirm an error is shown and the original malformed contents are not overwritten. Restore the backup afterward.

## Prepare for GitHub

Review the project and test it before publishing. The `.gitignore` excludes Python cache files, virtual environments, and editor files. Complaint data is not ignored, so check `data/complaints.json` and remove any personal information before staging files. Never commit passwords, API keys, or private student information.

From the project directory, initialize and prepare a local Git repository:

```text
git init
git add main.py storage.py .gitignore README.md data/.gitkeep
git status
git commit -m "Add CampusFix complaint management CLI"
```

These commands only prepare a local commit. They do not create or upload a GitHub repository. After reviewing the staged files, create a repository on GitHub and follow GitHub's instructions to add a remote and push when you are ready.
