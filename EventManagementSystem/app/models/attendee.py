import mysql.connector
from mysql.connector import Error


class Attendee:
    def __init__(self, db_connection):
        """
        Initialize the Attendee model with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection

    def register_attendee(self, event_id, first_name, last_name, email):
        """
        Registers a new attendee for an event.
        :param event_id: The ID of the event the attendee is registering for.
        :param first_name: The first name of the attendee.
        :param last_name: The last name of the attendee.
        :param email: The email address of the attendee.
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Check if the event has reached maximum capacity
            cursor.execute("SELECT COUNT(*) AS RegisteredAttendees FROM Attendee WHERE EventID = %s", (event_id,))
            registered_attendees = cursor.fetchone()["RegisteredAttendees"]

            cursor.execute("SELECT MaxAttendees FROM Event WHERE EventID = %s", (event_id,))
            max_attendees = cursor.fetchone()["MaxAttendees"]

            if registered_attendees >= max_attendees:
                return "Registration failed: Event has reached maximum capacity."

            # Insert new attendee into the database
            query = """
                INSERT INTO Attendee (EventID, FirstName, LastName, Email)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (event_id, first_name, last_name, email))
            self.db_connection.commit()

            return "Registration successful."

        except Error as e:
            return f"Error during registration: {str(e)}"

    def cancel_registration(self, attendee_id):
        """
        Cancels an attendee's registration for an event.
        :param attendee_id: The ID of the attendee whose registration is to be canceled.
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Delete attendee from the database
            query = "DELETE FROM Attendee WHERE AttendeeID = %s"
            cursor.execute(query, (attendee_id,))
            self.db_connection.commit()

            if cursor.rowcount == 0:
                return "Cancellation failed: Attendee not found."

            return "Registration successfully canceled."

        except Error as e:
            return f"Error during cancellation: {str(e)}"

    def get_attendees_by_event(self, event_id):
        """
        Retrieves a list of attendees for a specific event.
        :param event_id: The ID of the event.
        :return: A list of attendees or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch attendees for the given event
            query = "SELECT * FROM Attendee WHERE EventID = %s"
            cursor.execute(query, (event_id,))
            attendees = cursor.fetchall()

            return attendees

        except Error as e:
            return f"Error retrieving attendees: {str(e)}"

    def get_attendee_by_id(self, attendee_id):
        """
        Retrieves details of a specific attendee by their ID.
        :param attendee_id: The ID of the attendee.
        :return: Attendee details or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch attendee details
            query = "SELECT * FROM Attendee WHERE AttendeeID = %s"
            cursor.execute(query, (attendee_id,))
            attendee = cursor.fetchone()

            if not attendee:
                return "Attendee not found."

            return attendee

        except Error as e:
            return f"Error retrieving attendee details: {str(e)}"
