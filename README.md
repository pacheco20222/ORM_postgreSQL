# Database Management Application

## Overview
This application provides a graphical user interface (GUI) for managing a PostgreSQL database. It allows users to authenticate, view, add, and delete records in various tables.

## Features
- Authentication with PostgreSQL database.
- View all tables and their records.
- Add and delete records in the `countries` table.
- Extendable to other tables for CRUD operations.

## Requirements
- Python 3.x
- PyQt5
- SQLAlchemy
- PostgreSQL
- psycopg2
- python Virtual Environment

## Installation
1. Clone the repository:
   

2. Create and Activate a virtual environment:
- On Linux/Mac:
    ```bash 
    python3 -m venv venv
    source venv/bin/activate

- On Windows:
    ```bash
    python -m venv venv
    .\venv\Scripts\activate

3. Install the required packages (could be pip3 or pip)
    ```bash
    pip install -r requirements.txt


## Usage
1. Postgress Should be installed, and this code uses the HR_POSTGRESTSQL.sql file to create the database, not only that but it is meant for localhost.

2. Run the Application
    ```bash
    python3 main.py

3. Authenticate with your database credentials

4. Use the GUI to manage your database

## File Structure

main.py: Entry point of the application.

gui.py: Contains the GUI components.

db_session.py: Manages the database session.

models.py: Defines the SQLAlchemy models.

Extending the Application

To add CRUD operations for other tables:

Define the table model in models.py.

Create corresponding GUI components in gui.py.

Connect the GUI components to the database session.