import mysql.connector
from mysql.connector import Error
import bcrypt


class User:
    def __init__(self, db_connection):
        """
        Initialize the User model with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection

    def register_user(self, first_name, last_name, email, password, role='organizer'):
        """
        Registers a new user in the system.
        :param first_name: The first name of the user.
        :param last_name: The last name of the user.
        :param email: The email address of the user.
        :param password: The plaintext password of the user.
        :param role: The role of the user ('admin' or 'organizer'). Default is 'organizer'.
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Check if email already exists
            query = "SELECT Email FROM User WHERE Email = %s"
            cursor.execute(query, (email,))
            if cursor.fetchone():
                return "Error: Email is already registered."

            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Insert new user into the database
            query = """
                INSERT INTO User (FirstName, LastName, Email, Password, Role)
                VALUES (%s, %s, %s, %s, %s)
            """
            cursor.execute(query, (first_name, last_name, email, hashed_password.decode('utf-8'), role))
            self.db_connection.commit()

            return "User registered successfully."

        except Error as e:
            return f"Error registering user: {str(e)}"

    def authenticate_user(self, email, password):
        """
        Authenticates a user based on their email and password.
        :param email: The email address of the user.
        :param password: The plaintext password provided by the user.
        :return: User details (ID and role) if authentication is successful; error message otherwise.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Retrieve stored hashed password and user details
            query = "SELECT UserID, Role, Password FROM User WHERE Email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if not user:
                return "Error: Email not found."

            # Verify the provided password against the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), user['Password'].encode('utf-8')):
                return {"UserID": user["UserID"], "Role": user["Role"]}

            return "Error: Invalid password."

        except Error as e:
            return f"Error authenticating user: {str(e)}"

    def get_user_by_id(self, user_id):
        """
        Retrieves details of a specific user by their ID.
        :param user_id: The ID of the user to retrieve.
        :return: A dictionary containing user details or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch user details by ID
            query = "SELECT UserID, FirstName, LastName, Email, Role FROM User WHERE UserID = %s"
            cursor.execute(query, (user_id,))
            user = cursor.fetchone()

            if not user:
                return "User not found."

            return user

        except Error as e:
            return f"Error retrieving user details: {str(e)}"

    def get_all_users(self):
        """
        Retrieves all users in the system.
        :return: A list of dictionaries containing all users or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch all users from the database
            query = "SELECT UserID, FirstName, LastName, Email, Role FROM User"
            cursor.execute(query)
            users = cursor.fetchall()

            if not users:
                return "No users found."

            return users

        except Error as e:
            return f"Error retrieving users: {str(e)}"

    def get_user_by_email(self, email):
        """
        Retrieves a user by their email address.
        :param email: The email address of the user to retrieve.
        :return: A dictionary containing user details or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch user details by email
            query = "SELECT UserID, FirstName, LastName, Email, Role, Password FROM User WHERE Email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if not user:
                return None

            return user

        except Error as e:
            return f"Error retrieving user: {str(e)}"
