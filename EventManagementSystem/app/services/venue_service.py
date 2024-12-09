from app.models.venue import Venue
from app.models.event import Event


class VenueService:
    """
    Service layer for handling venue-related business logic.
    """

    def __init__(self, db_connection):
        """
        Initialize the VenueService with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection
        self.venue_model = Venue(db_connection)
        self.event_model = Event(db_connection)

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
            result = self.venue_model.add_venue(venue_name, location, capacity, cost_per_day)
            return result
        except Exception as e:
            return f"Error adding venue: {str(e)}"

    def get_available_venues(self):
        """
        Retrieves all venues that are currently available.
        :return: A list of available venues or an error message.
        """
        try:
            venues = self.venue_model.get_available_venues()
            if not venues:
                return "No available venues found."

            return venues
        except Exception as e:
            return f"Error retrieving available venues: {str(e)}"

    def assign_venue_to_event(self, event_id, venue_id):
        """
        Assigns a venue to an event after validating availability and capacity.
        :param event_id: The ID of the event.
        :param venue_id: The ID of the venue to assign.
        :return: Success message or error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Check if the venue exists and is available
            venue = self.venue_model.get_venue_by_id(venue_id)
            if not venue:
                return "Error: Venue not found."
            if venue["AvailabilityStatus"] != "available":
                return "Error: Venue is not available."

            # Check if the venue capacity is sufficient for the event
            if event["MaxAttendees"] > venue["Capacity"]:
                return "Error: Venue capacity is insufficient for this event."

            # Assign the venue to the event and mark it as booked
            result = self.venue_model.assign_venue_to_event(venue_id, event_id)
            return result
        except Exception as e:
            return f"Error assigning venue to event: {str(e)}"

    def release_venue(self, venue_id):
        """
        Marks a previously booked venue as available again.
        :param venue_id: The ID of the venue to release.
        :return: Success message or error message.
        """
        try:
            # Check if the venue exists
            venue = self.venue_model.get_venue_by_id(venue_id)
            if not venue:
                return "Error: Venue not found."

            # Release the venue
            result = self.venue_model.release_venue(venue_id)
            return result
        except Exception as e:
            return f"Error releasing venue: {str(e)}"

    def get_venue_details(self, venue_id):
        """
        Retrieves details of a specific venue by its ID.
        :param venue_id: The ID of the venue to retrieve.
        :return: A dictionary containing venue details or an error message.
        """
        try:
            # Retrieve details of the specified venue
            venue = self.venue_model.get_venue_by_id(venue_id)
            if not venue:
                return "Error: Venue not found."

            return venue
        except Exception as e:
            return f"Error retrieving venue details: {str(e)}"
