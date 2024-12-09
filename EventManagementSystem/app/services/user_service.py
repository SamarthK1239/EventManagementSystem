from app.models.user import User
import bcrypt


class UserService:
    """
    Service layer for handling user-related business logic.
    """

    def __init__(self, db_connection):
        """
        Initialize the UserService with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection
        self.user_model = User(db_connection)

    def register_user(self, first_name, last_name, email, password, role='organizer'):
        """
        Registers a new user in the system after validating input data.
        :param first_name: The first name of the user.
        :param last_name: The last name of the user.
        :param email: The email address of the user.
        :param password: The plaintext password of the user.
        :param role: The role of the user ('admin' or 'organizer'). Default is 'organizer'.
        :return: Success message or error message.
        """
        try:
            # Check if email is already registered
            existing_user = self.user_model.get_user_by_email(email)
            if existing_user is not None:
                return "Error: Email is already registered."

            # Hash the password using bcrypt
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Register the user
            result = self.user_model.register_user(first_name, last_name, email, hashed_password.decode('utf-8'), role)
            return result

        except Exception as e:
            return f"Error registering user: {str(e)}"

    def authenticate_user(self, email, password):
        """
        Authenticates a user based on their email and password.
        :param email: The email address of the user.
        :param password: The plaintext password provided by the user.
        :return: User details (ID and role) if authentication is successful; error message otherwise.
        """
        try:
            # Retrieve user details by email
            user = self.user_model.get_user_by_email(email)
            if not user:
                return "Error: Email not found."

            # Verify the provided password against the stored hash
            if bcrypt.checkpw(password.encode('utf-8'), user['Password'].encode('utf-8')):
                return {"UserID": user["UserID"], "Role": user["Role"]}

            return "Error: Invalid password."

        except Exception as e:
            return f"Error authenticating user: {str(e)}"

    def get_user_details(self, user_id):
        """
        Retrieves details of a specific user by their ID.
        :param user_id: The ID of the user to retrieve.
        :return: A dictionary containing user details or an error message.
        """
        try:
            # Retrieve user details by ID
            user = self.user_model.get_user_by_id(user_id)
            if not user:
                return "Error: User not found."

            return user

        except Exception as e:
            return f"Error retrieving user details: {str(e)}"

    def get_all_users(self):
        """
        Retrieves all users in the system.
        :return: A list of dictionaries containing all users or an error message.
        """
        try:
            # Retrieve all users
            users = self.user_model.get_all_users()
            if not users:
                return "No users found."

            return users

        except Exception as e:
            return f"Error retrieving users: {str(e)}"
