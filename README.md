
# Student Management System

A web-based application built with **Python, Flask, and SQLite** to simplify student record management through an efficient and user-friendly interface.

## Features

- **Student Registration** — Add student details with input validation.
- **Record Management** — View, update, and delete student records.
- **Smart Search** — Search by roll number, name, email, or course.
- **Data Integrity** — Enforce unique roll numbers and required fields.
- **Academic Validation** — Validate academic year values from 1 to 8.
- **Persistent Storage** — Store student records in an SQLite database.

## Technology Stack

- **Backend:** Python, Flask
- **Database:** SQLite
- **Frontend:** HTML, CSS
- **Templating Engine:** Jinja2

## Installation and Setup

### 1. Clone the Repository

```bash
git clone <repository-url>
cd <project-directory>
```

### 2. Install Dependencies

```bash
pip install Flask
```

### 3. Run the Application

```bash
python app.py
```

### 4. Access the Application

Open your browser and visit:

`http://127.0.0.1:5000/`

The SQLite database is initialized automatically when the application starts.

## Project Structure

```text
student-management-system/
├── app.py
├── students.db
└── templates/
    ├── index.html
    └── form.html
```

**Developed using Python, Flask, and SQLite.**
