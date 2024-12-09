import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os
from pathlib import Path


class Database:
    """
    Database class for managing the MySQL connection and executing queries.
    """

    def __init__(self):
        """
        Initialize the Database class and set up the connection object.
        """
        self.connection = None


    def connect(self):
        """
        Establishes a connection to the MySQL database using configuration settings.
        :return: A MySQL connection object or None if the connection fails.
        """
        try:
            path = Path("app/environment_variables/.env")
            load_dotenv(dotenv_path=path)

            host = os.getenv('host')
            port = os.getenv('port')
            user = os.getenv('user')
            password = os.getenv('password')
            database = os.getenv('database')

            if not all([host, port, user, password, database]):
                raise ValueError("One or more environment variables are missing.")

            self.connection = mysql.connector.connect(
                host=host,
                port=int(port),
                user=user,
                password=password,
                database=database,
            )
            if self.connection.is_connected():
                print("Connected to the database successfully.")
                return self.connection
        except Error as e:
            print(f"Error connecting to the database: {e}")
            return None
        except ValueError as ve:
            print(f"Configuration error: {ve}")
            return None

    def disconnect(self):
        """
        Closes the database connection if it is open.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query, params=None):
        """
        Executes a single SQL query (INSERT, UPDATE, DELETE).
        :param query: The SQL query to execute.
        :param params: Optional parameters for parameterized queries.
        :return: Success message or error message.
        """
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            return "Query executed successfully."
        except Error as e:
            print(f"Error executing query: {e}")
            return f"Error: {str(e)}"

    def fetch_one(self, query, params=None):
        """
        Executes a SELECT query and fetches a single result.
        :param query: The SQL query to execute.
        :param params: Optional parameters for parameterized queries.
        :return: A dictionary containing the result or an error message.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            result = cursor.fetchone()
            return result
        except Error as e:
            print(f"Error fetching data: {e}")
            return f"Error: {str(e)}"

    def fetch_all(self, query, params=None):
        """
        Executes a SELECT query and fetches all results.
        :param query: The SQL query to execute.
        :param params: Optional parameters for parameterized queries.
        :return: A list of dictionaries containing the results or an error message.
        """
        try:
            cursor = self.connection.cursor(dictionary=True)
            cursor.execute(query, params)
            results = cursor.fetchall()
            return results
        except Error as e:
            print(f"Error fetching data: {e}")
            return f"Error: {str(e)}"
