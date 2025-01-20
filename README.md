# netflix_titles

A Django-powered application for managing and exploring Netflix titles. 
This project includes advanced filtering, sorting, and a RESTful API for seamless integration.

Aim of this project is to create a sandbox environment to test out different search and filter providers for Django project.

## Features

- **Explore Titles**: Search and filter titles by name, type, release year, and country.
- **RESTful API**: Built with Django REST Framework for robust API endpoints.
- **Admin Management**: Fully integrated admin interface for managing Netflix titles.
- **Scalable Architecture**: Designed to handle large datasets efficiently.

---

## Project Structure

```
netflix/                             # Django project root
netflix_titles/
├── fixtures/
│   └── netflix_titles_fixture.json  # JSON fixture with Netflix titles data
├── models.py                        # Django models defining the NetflixTitle schema
├── migrations/                      # Django migrations for the app
├── admin.py                         # Admin configuration for managing Netflix titles
.env                                 # Environment variables
docker-compose.yml                   # Docker Compose configuration
```

---

## Installation

### Prerequisites
- Python 3.8+
- pip
- Virtual environment (recommended)

### Setup

1. Clone the Repository:
   ```bash
   git clone https://github.com/matejhocevar/netflix_titles.git
   cd netflix_titles
   ```
2.	Set Up a Virtual Environment:
   ```bash
   python -m venv venv
   source venv/bin/activate
   ```
3. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```
4. Configure Environment Variables:
Create a .env file in the project root:
   ```bash
    SECRET_KEY=your-secret-key
    DEBUG=True
    DATABASE_URL=sqlite:///db.sqlite3
   ```
5. Apply Migrations:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
6. Create a Superuser:
   ```bash
    python manage.py createsuperuser
    ```
7. Load Sample Data:
   ```bash
    python manage.py loaddata fixtures/netflix_titles_fixture.json
    ```
8. Run the Development Server:
    ```bash
    python manage.py runserver
    ```

---

## Usage

### Admin Interface
- Access the admin interface at `http://0.0.0.0:8000/admin/` and log in with your superuser credentials.

### RESTful API

- **List Titles**: `/api/titles`
- Supports query paramers for filtering (title, type, release_year, country) and sorting (title, release_year).
- **Retrieve Title**: `/api/titles/<id>`
- **Create Title**: `/api/titles` with standard REST operations (POST, PUT, PATCH, DELETE).