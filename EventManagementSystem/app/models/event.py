import mysql.connector
from mysql.connector import Error


class Event:
    def __init__(self, db_connection):
        """
        Initialize the Event model with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection

    def create_event(self, user_id, event_name, event_date, venue_id, max_attendees=0, budget=0.00):
        """
        Creates a new event in the database.
        :param user_id: The ID of the user (organizer) creating the event.
        :param event_name: The name of the event.
        :param event_date: The date of the event.
        :param venue_id: The ID of the venue for the event.
        :param max_attendees: The maximum number of attendees allowed (default is 0).
        :param budget: The budget allocated for the event (default is 0.00).
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Check if the venue is available
            cursor.execute("SELECT AvailabilityStatus FROM Venue WHERE VenueID = %s", (venue_id,))
            venue = cursor.fetchone()

            if not venue or venue["AvailabilityStatus"] != "available":
                return "Venue is not available for booking."

            # Insert new event into the database
            query = """
                INSERT INTO Event (UserID, EventName, EventDate, EventVenue, MaxAttendees, Budget)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (user_id, event_name, event_date, venue_id, max_attendees, budget))
            self.db_connection.commit()

            # Mark venue as booked
            cursor.execute("UPDATE Venue SET AvailabilityStatus = 'booked' WHERE VenueID = %s", (venue_id,))
            self.db_connection.commit()

            return "Event created successfully."

        except Error as e:
            return f"Error creating event: {str(e)}"

    def update_event(self, event_id, **kwargs):
        """
        Updates an existing event's details.
        :param event_id: The ID of the event to update.
        :param kwargs: Key-value pairs of fields to update (e.g., EventName='New Name').
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Build dynamic query based on provided fields
            fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
            values = list(kwargs.values())

            query = f"UPDATE Event SET {fields} WHERE EventID = %s"
            values.append(event_id)

            cursor.execute(query, tuple(values))
            self.db_connection.commit()

            if cursor.rowcount == 0:
                return "No changes made or event not found."

            return "Event updated successfully."

        except Error as e:
            return f"Error updating event: {str(e)}"

    def delete_event(self, event_id):
        """
        Deletes an existing event and its associated data.
        :param event_id: The ID of the event to delete.
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Delete associated schedules and attendees first
            cursor.execute("DELETE FROM Schedule WHERE EventID = %s", (event_id,))
            cursor.execute("DELETE FROM Attendee WHERE EventID = %s", (event_id,))

            # Delete the main event
            query = "DELETE FROM Event WHERE EventID = %s"
            cursor.execute(query, (event_id,))

            self.db_connection.commit()

            if cursor.rowcount == 0:
                return "Event not found or already deleted."

            return "Event deleted successfully."

        except Error as e:
            return f"Error deleting event: {str(e)}"

    def get_event_by_id(self, event_id):
        """
        Retrieves details of a specific event by its ID.
        :param event_id: The ID of the event to retrieve.
        :return: A dictionary with event details or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            query = "SELECT * FROM Event WHERE EventID = %s"
            cursor.execute(query, (event_id,))

            event = cursor.fetchone()

            if not event:
                return "Event not found."

            return event

        except Error as e:
            return f"Error retrieving event details: {str(e)}"

    def get_events_by_user(self, user_id):
        """
        Retrieves a list of events organized by a specific user.
        :param user_id: The ID of the user (organizer).
        :return: A list of events or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            query = "SELECT * FROM Event WHERE UserID = %s"
            cursor.execute(query, (user_id,))

            events = cursor.fetchall()

            return events

        except Error as e:
            return f"Error retrieving events for user: {str(e)}"

    def get_all_events(self):
        """
        Retrieves all events in the system.
        :return: A list of all events or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            query = "SELECT * FROM Event"
            cursor.execute(query)

            events = cursor.fetchall()

            return events

        except Error as e:
            return f"Error retrieving all events: {str(e)}"
