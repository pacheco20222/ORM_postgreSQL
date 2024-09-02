from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, ProgrammingError

class Sesion_BD:
    def __init__(self, base_de_datos, usuario, clave):
        # Create a connection string using the provided database name, user, and password
        self.engine = create_engine(f"postgresql://{usuario}:{clave}@localhost/{base_de_datos}")
        
        # Create a configured "Session" class
        self.Session = sessionmaker(bind=self.engine)
        
        # Initialize the session attribute to None
        self.session = None

        # Print the connection string for debugging purposes
        print(f"Connection String: postgresql://{usuario}:{clave}@localhost/{base_de_datos}")

        try:
            # Test the connection with a known query
            with self.engine.connect() as connection:
                # Execute a simple query that should fail if the credentials are wrong
                connection.execute(text("SELECT 1"))
            
            # Create the session only if the connection is successful
            self.session = self.Session()
            print("Connection successful")
        
        except OperationalError:
            # Handle errors related to incorrect credentials or other connection issues
            print("Connection failed: Incorrect credentials or other connection issues.")
            raise
        
        except ProgrammingError:
            # Handle errors related to database schema issues
            print("Connection failed: Database schema issue.")
            raise
        
        except Exception as e:
            # Handle any other exceptions that may occur
            print(f"Connection failed: {str(e)}")
            raise