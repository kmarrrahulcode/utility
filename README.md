# Student Registration System

A basic web application for registering students with SQLite backend built using Flask.

## Features

- Student registration form with validation
- View all registered students in a table format
- Individual student detail view
- Delete student functionality
- Responsive design with modern UI
- SQLite database for data persistence

## Project Structure

```
utility/
├── app.py                 # Flask application main file
├── init_db.py             # Database initialization script
├── requirements.txt       # Python dependencies
├── students.db            # SQLite database file (created automatically)
├── static/
│   └── css/
│       └── style.css      # CSS styles
└── templates/
    ├── register.html      # Student registration form
    ├── students.html      # Students list page
    └── student_detail.html # Individual student details page
```

## Installation

1. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Initialize the database:
   ```bash
   python init_db.py
   ```

3. Run the application:
   ```bash
   python app.py
   ```

4. Open your browser and navigate to `http://localhost:5000`

## Usage

- **Register Student**: Fill out the registration form with student details
- **View Students**: See all registered students in a table format
- **Student Details**: Click on any student name to view detailed information
- **Delete Student**: Remove students from the database (with confirmation)

## Database Schema

The `students` table contains the following fields:
- `id`: Primary key (auto-increment)
- `first_name`: Student's first name (required)
- `last_name`: Student's last name (required)
- `email`: Student's email address (required, unique)
- `phone`: Student's phone number (optional)
- `date_of_birth`: Student's date of birth (optional)
- `address`: Student's address (optional)
- `registration_date`: When the student was registered (auto-generated)

## API Endpoints

- `/api/students` - Get all students in JSON format

## Technologies Used

- **Backend**: Flask (Python web framework)
- **Database**: SQLite
- **Frontend**: HTML5, CSS3
- **Styling**: Custom CSS with responsive design

## License

This project is open source and available under the MIT License.