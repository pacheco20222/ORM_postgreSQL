from sqlalchemy import Column, Integer, ForeignKey, CHAR, VARCHAR, TIMESTAMP, CheckConstraint, NUMERIC
from sqlalchemy.orm import relationship, declarative_base

# Base class for all models
Base = declarative_base()

class Region(Base):
    """
    Represents a region in the database.
    """
    __tablename__ = 'regions'

    region_id = Column(Integer, primary_key=True)  # Primary key for the region
    region_name = Column(VARCHAR(25))  # Name of the region

    # Relationship to the Country model
    countries = relationship("Country", back_populates="region")

class Country(Base):
    """
    Represents a country in the database.
    """
    __tablename__ = 'countries'

    country_id = Column(CHAR(2), primary_key=True)  # Primary key for the country
    country_name = Column(VARCHAR(40))  # Name of the country
    region_id = Column(Integer, ForeignKey('regions.region_id'))  # Foreign key to the region

    # Relationships to the Region and Location models
    region = relationship("Region", back_populates="countries")
    locations = relationship("Location", back_populates="country")

class Location(Base):
    """
    Represents a location in the database.
    """
    __tablename__ = 'locations'

    location_id = Column(Integer, primary_key=True)  # Primary key for the location
    street_address = Column(VARCHAR(40))  # Street address of the location
    postal_code = Column(VARCHAR(12))  # Postal code of the location
    city = Column(VARCHAR(30), nullable=False)  # City of the location
    state_province = Column(VARCHAR(25))  # State or province of the location
    country_id = Column(CHAR(2), ForeignKey('countries.country_id'))  # Foreign key to the country

    # Relationships to the Country and Department models
    country = relationship("Country", back_populates="locations")
    departments = relationship("Department", back_populates="location")

class Department(Base):
    """
    Represents a department in the database.
    """
    __tablename__ = 'departments'

    department_id = Column(Integer, primary_key=True)  # Primary key for the department
    department_name = Column(VARCHAR(30), nullable=False)  # Name of the department
    manager_id = Column(Integer, ForeignKey('employees.employee_id'))  # Foreign key to the manager (employee)
    location_id = Column(Integer, ForeignKey('locations.location_id'))  # Foreign key to the location

    # Relationships to the Location and Employee models
    location = relationship("Location", back_populates="departments")
    employees = relationship("Employee", back_populates="department", foreign_keys="[Employee.department_id]")

class Job(Base):
    """
    Represents a job in the database.
    """
    __tablename__ = 'jobs'

    job_id = Column(VARCHAR(10), primary_key=True)  # Primary key for the job
    job_title = Column(VARCHAR(35), nullable=False)  # Title of the job
    min_salary = Column(NUMERIC(6))  # Minimum salary for the job
    max_salary = Column(NUMERIC(6))  # Maximum salary for the job

    # Relationships to the Employee and JobHistory models
    employees = relationship("Employee", back_populates="job")
    job_history = relationship("JobHistory", back_populates="job")

class Employee(Base):
    """
    Represents an employee in the database.
    """
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True)  # Primary key for the employee
    first_name = Column(VARCHAR(20))  # First name of the employee
    last_name = Column(VARCHAR(25), nullable=False)  # Last name of the employee
    email = Column(VARCHAR(25), nullable=False, unique=True)  # Email of the employee
    phone_number = Column(VARCHAR(20))  # Phone number of the employee
    hire_date = Column(TIMESTAMP, nullable=False)  # Hire date of the employee
    job_id = Column(VARCHAR(10), ForeignKey('jobs.job_id'), nullable=False)  # Foreign key to the job
    salary = Column(NUMERIC(8, 2), CheckConstraint('salary > 0'))  # Salary of the employee
    commission_pct = Column(NUMERIC(2, 2))  # Commission percentage of the employee
    manager_id = Column(Integer, ForeignKey('employees.employee_id'))  # Foreign key to the manager (employee)
    department_id = Column(Integer, ForeignKey('departments.department_id'))  # Foreign key to the department

    # Relationships to the Job, Department, and JobHistory models
    job = relationship("Job", back_populates="employees")
    department = relationship("Department", back_populates="employees", foreign_keys=[department_id])
    job_history = relationship("JobHistory", back_populates="employee")
    subordinates = relationship("Employee", backref='manager', remote_side=[employee_id])

class JobHistory(Base):
    """
    Represents the job history of an employee in the database.
    """
    __tablename__ = 'job_history'

    employee_id = Column(Integer, ForeignKey('employees.employee_id'), primary_key=True)  # Primary key (employee ID)
    start_date = Column(TIMESTAMP, primary_key=True)  # Primary key (start date)
    end_date = Column(TIMESTAMP, nullable=False)  # End date of the job history
    job_id = Column(VARCHAR(10), ForeignKey('jobs.job_id'), nullable=False)  # Foreign key to the job
    department_id = Column(Integer, ForeignKey('departments.department_id'))  # Foreign key to the department

    # Relationships to the Employee and Job models
    employee = relationship("Employee", back_populates="job_history")
    job = relationship("Job", back_populates="job_history")