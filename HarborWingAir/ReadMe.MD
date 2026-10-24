
# HarborWing Air Database Management System

## Project Description

HarborWing Air is a sample airline database management system created for the IT8 Midterm Drill. It stores information about passengers, reservations, payments, airports, flight schedules, and flight costs.

## Objectives

- Design a relational database using MySQL.
- Create tables with primary keys and foreign keys.
- Use linking tables to connect reservations with payments and flight legs.
- Generate sample data using Python Faker.
- Perform SQL queries to retrieve information from the database.
- Demonstrate basic reservation CRUD operations using Flask.

## Technologies Used

- MySQL
- MySQL Workbench
- Python
- Flask
- Faker
- mysql-connector-python
- Visual Studio Code

## Main Project Files

- `app.py` - Flask application for reservation management.
- `db_config.py` - MySQL database connection settings.
- `seed_data.py` - Script for generating sample database records.
- `harborwing_queries.sql` - SQL queries for the project.
- `requirements.txt` - Required Python packages.
- `HarborWing_Air.mwb` - MySQL Workbench database model.
- `HarborWing_Air.png` - Exported database relationship diagram.
- `templates/index.html` - Reservation management webpage.

## Database Setup

1. Install and open MySQL Server and MySQL Workbench.
2. Create the `harborwing_air` database and its required tables using the project SQL files.
3. Update the database connection settings in `db_config.py`.
4. Install the required Python packages:

   `py -3.11 -m pip install -r requirements.txt`

5. Run the sample data script:

   `py -3.11 seed_data.py`

6. Start the Flask application:

   `py -3.11 app.py`

7. Open `http://127.0.0.1:5000` in your browser.

## Sample Data

The project uses Python Faker to generate fictional records for testing. Run the seed script only after creating the database tables. If you run it again, check whether the script resets or duplicates existing data.

## Features

- View reservations.
- Add reservations.
- Update reservation party size.
- Delete reservations.

## Limitations

This is an educational project using sample data. It is not a complete airline booking system and does not process real airline tickets or payments.

## Author

Student project for IT8 Midterm Drill.
