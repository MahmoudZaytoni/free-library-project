# Free Library Project

Free Library Project is a web-based application that allows users to browse and search books, and download or add them to their favorites. The application also includes an authentication system with a login and sign-up feature for users. The project is developed using Python Flask framework and uses SQLAlchemy as the Object-Relational Mapping (ORM) tool to interface with the database.

## Features

- User Authentication: Users must have an account to access the library.
- Book Browsing: Users can browse books and search by title.
- Book Filtering: Users can filter books by category.
- Book Downloading: Users can download books.
- Book Favoriting: Users can add books to their favorites.
- Admin Panel: Admins can add, modify, or delete books, categories, and authors.

## Database Relationships

The Free Library Project uses a SQLite database with the following relationships between tables:

1. Users and Books: Many-to-many relationship for user favorites.

2. Books and Categories: One-to-many relationship for book categories.

3. Books and Authors: One-to-many relationship for book authors.

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/MahmoudZaytoni/free-library-project

2. Navigate to the project directory:
   ```bash 
   cd free-library-project

3. Create and activate a virtual environment:

   ```bash
   python -m venv env
   source env/bin/activate (for Linux/Mac) or env\Scripts\activate.bat (for Windows)

4. Install the required dependencies:
  
   ```bash
   pip install -r requirements.txt
  
5. Run the main.py file

   ```bash
   python3 main.py

## Usage

1. Navigate to http://localhost:5000 in your web browser.
2. Register an account or log in if you already have one.
3. To access the admin panel, go to `http://localhost:5000/admin/book` and log in with an admin account.
4. Admins can add, modify or delete books, categories and authors by accessing the admin panel.

Note: This project is focused on the backend functionality and does not include a fully developed frontend.