from sqlalchemy import Column, Integer, ForeignKey, CHAR, VARCHAR, TIMESTAMP, CheckConstraint, NUMERIC
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()

class Region(Base):
    __tablename__ = 'regions'

    region_id = Column(Integer, primary_key=True)
    region_name = Column(VARCHAR(25))

    countries = relationship("Country", back_populates="region")

class Country(Base):
    __tablename__ = 'countries'

    country_id = Column(CHAR(2), primary_key=True)
    country_name = Column(VARCHAR(40))
    region_id = Column(Integer, ForeignKey('regions.region_id'))

    region = relationship("Region", back_populates="countries")
    locations = relationship("Location", back_populates="country")

class Location(Base):
    __tablename__ = 'locations'

    location_id = Column(Integer, primary_key=True)
    street_address = Column(VARCHAR(40))
    postal_code = Column(VARCHAR(12))
    city = Column(VARCHAR(30), nullable=False)
    state_province = Column(VARCHAR(25))
    country_id = Column(CHAR(2), ForeignKey('countries.country_id'))

    country = relationship("Country", back_populates="locations")
    departments = relationship("Department", back_populates="location")

class Department(Base):
    __tablename__ = 'departments'

    department_id = Column(Integer, primary_key=True)
    department_name = Column(VARCHAR(30), nullable=False)
    manager_id = Column(Integer, ForeignKey('employees.employee_id'))
    location_id = Column(Integer, ForeignKey('locations.location_id'))
    location = relationship("Location", back_populates="departments")
    employees = relationship("Employee", back_populates="department", foreign_keys="[Employee.department_id]")

class Job(Base):
    __tablename__ = 'jobs'

    job_id = Column(VARCHAR(10), primary_key=True)
    job_title = Column(VARCHAR(35), nullable=False)
    min_salary = Column(NUMERIC(6))
    max_salary = Column(NUMERIC(6))

    employees = relationship("Employee", back_populates="job")
    job_history = relationship("JobHistory", back_populates="job")

class Employee(Base):
    __tablename__ = 'employees'

    employee_id = Column(Integer, primary_key=True)
    first_name = Column(VARCHAR(20))
    last_name = Column(VARCHAR(25), nullable=False)
    email = Column(VARCHAR(25), nullable=False, unique=True)
    phone_number = Column(VARCHAR(20))
    hire_date = Column(TIMESTAMP, nullable=False)
    job_id = Column(VARCHAR(10), ForeignKey('jobs.job_id'), nullable=False)
    salary = Column(NUMERIC(8, 2), CheckConstraint('salary > 0'))
    commission_pct = Column(NUMERIC(2, 2))
    manager_id = Column(Integer, ForeignKey('employees.employee_id'))
    department_id = Column(Integer, ForeignKey('departments.department_id'))

    job = relationship("Job", back_populates="employees")
    department = relationship("Department", back_populates="employees", foreign_keys=[department_id])
    job_history = relationship("JobHistory", back_populates="employee")
    subordinates = relationship("Employee", backref='manager', remote_side=[employee_id])

class JobHistory(Base):
    __tablename__ = 'job_history'

    employee_id = Column(Integer, ForeignKey('employees.employee_id'), primary_key=True)
    start_date = Column(TIMESTAMP, primary_key=True)
    end_date = Column(TIMESTAMP, nullable=False)
    job_id = Column(VARCHAR(10), ForeignKey('jobs.job_id'), nullable=False)
    department_id = Column(Integer, ForeignKey('departments.department_id'))

    employee = relationship("Employee", back_populates="job_history")
    job = relationship("Job", back_populates="job_history")