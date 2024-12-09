import mysql.connector
from mysql.connector import Error


class Venue:
    def __init__(self, db_connection):
        """
        Initialize the Venue model with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection

    def add_venue(self, venue_name, location, capacity, cost_per_day):
        """
        Adds a new venue to the system.
        :param venue_name: The name of the venue.
        :param location: The physical address of the venue.
        :param capacity: The maximum number of people the venue can hold.
        :param cost_per_day: The cost to rent the venue per day.
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Insert new venue into the database
            query = """
                INSERT INTO Venue (VenueName, Location, Capacity, CostPerDay, AvailabilityStatus)
                VALUES (%s, %s, %s, %s, 'available')
            """
            cursor.execute(query, (venue_name, location, capacity, cost_per_day))
            self.db_connection.commit()

            return "Venue added successfully."

        except Error as e:
            return f"Error adding venue: {str(e)}"

    def get_available_venues(self):
        """
        Retrieves all venues that are currently available.
        :return: A list of available venues or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch all available venues
            query = "SELECT * FROM Venue WHERE AvailabilityStatus = 'available'"
            cursor.execute(query)
            venues = cursor.fetchall()

            if not venues:
                return "No available venues found."

            return venues

        except Error as e:
            return f"Error retrieving available venues: {str(e)}"

    def assign_venue_to_event(self, venue_id, event_id):
        """
        Assigns a venue to an event and marks it as booked.
        :param venue_id: The ID of the venue to assign.
        :param event_id: The ID of the event to assign the venue to.
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Check if the venue is available
            query_check = "SELECT AvailabilityStatus FROM Venue WHERE VenueID = %s"
            cursor.execute(query_check, (venue_id,))
            result = cursor.fetchone()

            if not result or result[0] != 'available':
                return "Error: Venue is not available."

            # Assign the venue to the event and mark it as booked
            query_assign_event = "UPDATE Event SET EventVenue = %s WHERE EventID = %s"
            query_update_venue = "UPDATE Venue SET AvailabilityStatus = 'booked' WHERE VenueID = %s"

            cursor.execute(query_assign_event, (venue_id, event_id))
            cursor.execute(query_update_venue, (venue_id,))
            self.db_connection.commit()

            return "Venue assigned to event successfully."

        except Error as e:
            return f"Error assigning venue to event: {str(e)}"

    def release_venue(self, venue_id):
        """
        Marks a venue as available again after it has been used or unassigned from an event.
        :param venue_id: The ID of the venue to release.
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Update the availability status of the venue
            query = "UPDATE Venue SET AvailabilityStatus = 'available' WHERE VenueID = %s"
            cursor.execute(query, (venue_id,))
            self.db_connection.commit()

            if cursor.rowcount == 0:
                return "Venue not found or already available."

            return "Venue released successfully."

        except Error as e:
            return f"Error releasing venue: {str(e)}"

    def get_venue_by_id(self, venue_id):
        """
        Retrieves details of a specific venue by its ID.
        :param venue_id: The ID of the venue to retrieve.
        :return: A dictionary containing venue details or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch venue details by ID
            query = "SELECT * FROM Venue WHERE VenueID = %s"
            cursor.execute(query, (venue_id,))
            venue = cursor.fetchone()

            if not venue:
                return "Venue not found."

            return venue

        except Error as e:
            return f"Error retrieving venue details: {str(e)}"
