# Netflix Titles Data

This repository contains data and instructions for working with Netflix titles in a Django application. The data is stored as a JSON fixture and can be imported into a database using Django's management commands.

## Project Structure

```
netflix_titles/
├── fixtures/
│   └── netflix_titles_fixture.json  # JSON fixture with Netflix titles data
├── models.py                        # Django models defining the NetflixTitle schema
├── migrations/                      # Django migrations for the app
├── admin.py                         # Admin configuration for managing Netflix titles
```

---

## Prerequisites

1. **Python**: Ensure Python 3.8+ is installed.
2. **Django**: Install Django by running:
   ```bash
   pip install django
   ```
3.	Database Setup: A database (e.g., SQLite, PostgreSQL) should be configured in your settings.py.

---

## Setup Instructions

1. **Clone the repository**:
2. **Navigate to the project directory**:
   ```bash
   cd netflix_titles
   ```
3. **Run Migrations**:
   ```bash
    python manage.py migrate
    ```
4. **Load the Netflix titles data**:
   ```bash
   python manage.py loaddata fixtures/netflix_titles_fixture.json
   ```