from PyQt5.QtWidgets import (QApplication, QWidget, QLabel, QVBoxLayout, QLineEdit,
                             QPushButton, QComboBox, QMessageBox, QTableWidget, QTableWidgetItem, QDialog)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon
from db_session import Sesion_BD
from models import Country
import sys
from sqlalchemy import inspect, text

class AuthenticationWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Authentication")
        self.resize(300, 200)

        # Widgets for database name, username, and password input
        self.label_db_name = QLabel("Database Name:")
        self.input_db_name = QLineEdit()

        self.label_username = QLabel("Username:")
        self.input_username = QLineEdit()

        self.label_password = QLabel("Password:")
        self.input_password = QLineEdit()
        self.input_password.setEchoMode(QLineEdit.Password)  # Hide password input

        # Submit button to trigger authentication
        self.btn_submit = QPushButton("Submit")
        self.btn_submit.clicked.connect(self.authenticate)

        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.label_db_name)
        layout.addWidget(self.input_db_name)
        layout.addWidget(self.label_username)
        layout.addWidget(self.input_username)
        layout.addWidget(self.label_password)
        layout.addWidget(self.input_password)
        layout.addWidget(self.btn_submit)
        self.setLayout(layout)

    def authenticate(self):
        # Get input values
        db_name = self.input_db_name.text().strip()
        username = self.input_username.text().strip()
        password = self.input_password.text().strip()

        try:
            # Attempt to create a session with the provided credentials
            self.session = Sesion_BD(db_name, username, password).session

            # If successful, open the main window and close the authentication window
            self.main_window = MainWindow(self.session)
            self.main_window.show()
            self.close()

        except Exception as e:
            # Show an error message if authentication fails
            QMessageBox.critical(self, "Authentication Error", f"Failed to connect to the database. Please check your credentials and try again. Error: {str(e)}")

class MainWindow(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.engine = self.session.get_bind()  # Get the engine from the session
        
        self.setWindowTitle("Database Management")
        self.resize(600, 400)
        self.setWindowIcon(QIcon("postgress_logo.png"))
        
        # Title label
        self.title = QLabel("Database Management", self)
        self.title.setAlignment(Qt.AlignCenter)
        
        # Buttons for various database operations
        self.button_add_country = QPushButton("Add Country", self)
        self.button_delete_country = QPushButton("Delete Country", self)
        self.button_view_all_tables = QPushButton("View All Tables", self)
        self.button_view_one_table = QPushButton("View One Table", self)
        
        self.initGUI()
        
    def initGUI(self):
        # Layout setup
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.title)
        self.layout.addWidget(self.button_add_country)
        self.layout.addWidget(self.button_delete_country)
        self.layout.addWidget(self.button_view_all_tables)
        self.layout.addWidget(self.button_view_one_table)
        self.setLayout(self.layout)
        
        # Connect buttons to their respective functions
        self.button_add_country.clicked.connect(self.show_add_country)
        self.button_delete_country.clicked.connect(self.show_delete_country)
        self.button_view_all_tables.clicked.connect(self.show_all_tables)
        self.button_view_one_table.clicked.connect(self.show_one_table)
        
    def show_add_country(self):
        # Show the window to add a country
        self.add_window = AddCountryWindow(self.session)
        self.add_window.show()
        
    def show_delete_country(self):
        # Show the window to delete a country
        self.delete_window = DeleteCountryWindow(self.session)
        self.delete_window.show()
    
    def show_all_tables(self):
        try:
            # Get a list of all tables in the database
            inspector = inspect(self.engine)
            tables = inspector.get_table_names()

            # Create a new window to display all the tables
            self.All_Tables_Window = QWidget()
            layout = QVBoxLayout()

            for table in tables:
                # Create a QTableWidget for each table
                table_widget = QTableWidget()
                
                # Query the table
                query_for_table = text(f"SELECT * FROM {table}")
                result = self.session.execute(query_for_table)
                
                # Set the number of columns
                table_widget.setColumnCount(len(result.keys()))
                table_widget.setHorizontalHeaderLabels(result.keys())

                # Populate the table with data
                for i, row in enumerate(result):
                    table_widget.insertRow(i)
                    for j, cell in enumerate(row):
                        table_widget.setItem(i, j, QTableWidgetItem(str(cell)))

                layout.addWidget(QLabel(f"Table: {table}"))
                layout.addWidget(table_widget)
        
            self.All_Tables_Window.setLayout(layout)
            self.All_Tables_Window.setWindowTitle("View All Tables")
            self.All_Tables_Window.resize(800, 600)
            self.All_Tables_Window.show()

        except Exception as e:
            # Show an error message if something goes wrong
            QMessageBox.critical(self, "Error", f"Error displaying all tables: {str(e)}")

    def show_one_table(self):
        # Create a dialog to get the table name
        self.dialogTable = QDialog()
        self.dialogTable.setWindowTitle("Select Table")
        
        layout = QVBoxLayout()
        
        # Dropdown to select the table
        self.table_select = QComboBox()
        tables = ['countries', 'departments', 'employees', 'job_history', 'jobs', 'locations', 'regions']
        self.table_select.addItems(tables)
        
        layout.addWidget(QLabel("Select a table"))
        layout.addWidget(self.table_select)
        
        # Button to show table
        show_button = QPushButton("Show Table")
        show_button.clicked.connect(self.display_table_selected)
        layout.addWidget(show_button)
        
        self.dialogTable.setLayout(layout)
        self.dialogTable.exec()
        
    def display_table_selected(self):
        # Get the selected table from the dropdown
        selected_table = self.table_select.currentText()
    
        try:
            # Execute a query to select all records from the chosen table
            query_for_selected_table = text(f"SELECT * FROM {selected_table}")
            result = self.session.execute(query_for_selected_table)
        
            # Create a new window to display the table data
            self.One_Table_Window = QWidget()
            layout = QVBoxLayout()
        
            # Create a QTableWidget to display the data
            table_widget = QTableWidget()
            table_widget.setColumnCount(len(result.keys()))
            table_widget.setHorizontalHeaderLabels(result.keys())

            # Populate the table with data
            for i, row in enumerate(result):
                table_widget.insertRow(i)
                for j, cell in enumerate(row):
                    table_widget.setItem(i, j, QTableWidgetItem(str(cell)))

            layout.addWidget(QLabel(f"Table: {selected_table}"))
            layout.addWidget(table_widget)
        
            self.One_Table_Window.setLayout(layout)
            self.One_Table_Window.setWindowTitle(f"View Table: {selected_table}")
            self.One_Table_Window.resize(800, 600)
            self.One_Table_Window.show()
    
        except Exception as e:
            # Show an error message if something goes wrong
            QMessageBox.critical(self, "Error", f"Error displaying table: {str(e)}")
        
        # Close the dialog after displaying the table
        self.dialogTable.close()

class AddCountryWindow(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Add Country")
        self.resize(300, 200)
        
        # Widgets for country ID, name, and region ID input
        self.label_id_country = QLabel("Country ID:")
        self.input_id_country = QLineEdit()
        
        self.label_country_name = QLabel("Country Name:")
        self.input_country_name = QLineEdit()
        
        self.label_id_region = QLabel("Region ID:")
        self.dropdown_id_region = QComboBox()
        self.dropdown_id_region.addItems(["1: Europe", "2: Americas", "3: Asia", "4: Middle East and Africa"])
        
        self.submit_button = QPushButton("Add")
        self.submit_button.clicked.connect(self.add_country)
        
        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.label_id_country)
        layout.addWidget(self.input_id_country)
        layout.addWidget(self.label_country_name)
        layout.addWidget(self.input_country_name)
        layout.addWidget(self.label_id_region)
        layout.addWidget(self.dropdown_id_region)
        layout.addWidget(self.submit_button)
        
        self.setLayout(layout)
        
    def add_country(self):
        try:
            # Get input values
            country_id = self.input_id_country.text().strip().upper()
            country_name = self.input_country_name.text().strip().title()
            region_id = int(self.dropdown_id_region.currentText().split(":")[0])
            
            if not country_id or not country_name:
                raise ValueError("Country ID and Country Name are required")
            
            # Create a new Country object and add it to the session
            country = Country(country_id=country_id, country_name=country_name, region_id=region_id)
            self.session.add(country)
            self.session.commit()
            
            # Show success message and close the window
            QMessageBox.information(self, "Success", f"Country with ID {country_id} added successfully")
            self.close()
        
        except Exception as e:
            if "IntegrityError" in str(e):
                self.session.rollback()
                QMessageBox.critical(self, "Error", "Error adding country. Country ID already exists.")
            else:
                QMessageBox.critical(self, "Error", f"Error adding country: {str(e)}")
            self.session.rollback()
        except ValueError as ve:
            QMessageBox.warning(self, "Warning", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error adding country: {str(e)}")

class DeleteCountryWindow(QWidget):
    def __init__(self, session):
        super().__init__()
        self.session = session
        self.setWindowTitle("Delete Country")
        self.resize(300, 200)
        
        # Widgets for country ID input
        self.label_id_country = QLabel("Country ID:")
        self.input_id_country = QLineEdit()
        
        self.delete_button = QPushButton("Delete")
        self.delete_button.clicked.connect(self.delete_country)
        
        # Layout setup
        layout = QVBoxLayout()
        layout.addWidget(self.label_id_country)
        layout.addWidget(self.input_id_country)
        layout.addWidget(self.delete_button)
        
        self.setLayout(layout)
        
    def delete_country(self):
        try:
            # Get the country ID from input
            country_id = self.input_id_country.text().strip().upper()
            
            if not country_id:
                raise ValueError("Country ID is required")
            
            # Query the country by ID
            country = self.session.query(Country).filter_by(country_id=country_id).first()
            
            if not country:
                raise ValueError("No country found with that ID")
            
            # Delete the country and commit the transaction
            self.session.delete(country)
            self.session.commit()
            
            # Show success message and close the window
            QMessageBox.information(self, "Success", f"Country with ID {country_id} deleted successfully")
            self.close()
        
        except ValueError as ve:
            QMessageBox.warning(self, "Warning", str(ve))
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error deleting country: {str(e)}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    auth_window = AuthenticationWindow()
    auth_window.show()
    sys.exit(app.exec_())