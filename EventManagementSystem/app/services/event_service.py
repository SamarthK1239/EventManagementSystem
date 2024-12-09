from app.models.event import Event
from app.models.venue import Venue


class EventService:
    """
    Service layer for handling event-related business logic.
    """

    def __init__(self, db_connection):
        """
        Initialize the EventService with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection
        self.event_model = Event(db_connection)
        self.venue_model = Venue(db_connection)

    def create_event(self, user_id, event_name, event_date, venue_id, max_attendees=0, budget=0.00):
        """
        Creates a new event after validating venue availability and input data.
        :param user_id: The ID of the user (organizer) creating the event.
        :param event_name: The name of the event.
        :param event_date: The date of the event.
        :param venue_id: The ID of the venue for the event.
        :param max_attendees: Maximum number of attendees allowed for the event.
        :param budget: Budget allocated for the event.
        :return: Success message or error message.
        """
        try:
            # Check if the venue is available
            venue = self.venue_model.get_venue_by_id(venue_id)
            if not venue:
                return "Error: Venue not found."
            if venue["AvailabilityStatus"] != "available":
                return "Error: Venue is not available."

            # Create the event
            result = self.event_model.create_event(user_id, event_name, event_date, venue_id, max_attendees, budget)
            return result

        except Exception as e:
            return f"Error creating event: {str(e)}"

    def update_event(self, event_id, **kwargs):
        """
        Updates an existing event's details.
        :param event_id: The ID of the event to update.
        :param kwargs: Key-value pairs of fields to update (e.g., EventName='New Name').
        :return: Success message or error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Update the event
            result = self.event_model.update_event(event_id, **kwargs)
            return result

        except Exception as e:
            return f"Error updating event: {str(e)}"

    def delete_event(self, event_id):
        """
        Deletes an existing event and its associated data (e.g., schedules and attendees).
        :param event_id: The ID of the event to delete.
        :return: Success message or error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Delete the event
            result = self.event_model.delete_event(event_id)

            # Release associated venue
            if "EventVenue" in event and event["EventVenue"]:
                self.venue_model.release_venue(event["EventVenue"])

            return result

        except Exception as e:
            return f"Error deleting event: {str(e)}"

    def get_event_details(self, event_id):
        """
        Retrieves details of a specific event by its ID.
        :param event_id: The ID of the event to retrieve.
        :return: A dictionary containing event details or an error message.
        """
        try:
            # Retrieve the event details
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            return event

        except Exception as e:
            return f"Error retrieving event details: {str(e)}"

    def get_events_by_user(self, user_id):
        """
        Retrieves all events organized by a specific user.
        :param user_id: The ID of the user (organizer).
        :return: A list of events or an error message.
        """
        try:
            # Retrieve events created by this user
            events = self.event_model.get_events_by_user(user_id)
            if not events:
                return "No events found for this user."

            return events

        except Exception as e:
            return f"Error retrieving events for user: {str(e)}"

    def get_all_events(self):
        """
        Retrieves all events in the system.
        :return: A list of all events or an error message.
        """
        try:
            # Retrieve all events
            events = self.event_model.get_all_events()
            if not events:
                return "No events found."

            return events

        except Exception as e:
            return f"Error retrieving all events: {str(e)}"
