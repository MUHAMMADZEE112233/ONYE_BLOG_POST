# My Blog Application

## Overview
My Blog is a web application built with Django that allows users to register, log in, create and manage blog posts, and comment on posts. The application includes features like profile management, blog post categorization, and comment moderation.

## Features
- User registration and authentication
- Profile management
- Create and edit blog posts
- Categorize blog posts
- Add comments on blog posts
- Pagination for blog posts
- Filter blog posts by category

## Technologies Used
- Django
- Bootstrap 4
- SQLite (default database)
- jQuery

## Getting Started

### Prerequisites
- Python 3.8+
- Django 3.2+
- Virtualenv (optional but recommended)

### Installation

1. **Clone the repository:**
    ```bash
    git clone https://github.com/MUHAMMADZEE112233/ONYE_BLOG_POST
    ```

2. **Create and activate a virtual environment:**
    ```bash
    python3 -m venv env
    source env/bin/activate
    ```

3. **Install the required dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4. **Apply migrations:**
    ```bash
    python manage.py migrate
    ```

5. **Create a superuser:**
    ```bash
    python manage.py createsuperuser
    ```

6. **Run the development server:**
    ```bash
    python manage.py runserver
    ```

7. **Access the application:**
    Open your browser and go to `http://127.0.0.1:8000/`.

## Running Tests
To run the tests, use the following command:
```bash
python manage.py test