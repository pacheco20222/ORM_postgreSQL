from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError, ProgrammingError

class Sesion_BD:
    def __init__(self, base_de_datos, usuario, clave):
        self.engine = create_engine(f"postgresql://{usuario}:{clave}@localhost/{base_de_datos}")
        self.Session = sessionmaker(bind=self.engine)
        self.session = None

        # Print the connection string for debugging
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
            print("Connection failed: Incorrect credentials or other connection issues.")
            raise
        except ProgrammingError:
            print("Connection failed: Database schema issue.")
            raise
        except Exception as e:
            print(f"Connection failed: {str(e)}")
            raise