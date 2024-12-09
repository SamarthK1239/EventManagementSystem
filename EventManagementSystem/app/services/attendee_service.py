from app.models.attendee import Attendee
from app.models.event import Event


class AttendeeService:
    """
    Service layer for handling attendee-related business logic.
    """

    def __init__(self, db_connection):
        """
        Initialize the AttendeeService with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection
        self.attendee_model = Attendee(db_connection)
        self.event_model = Event(db_connection)

    def register_attendee(self, event_id, first_name, last_name, email):
        """
        Registers an attendee for an event if capacity allows.
        :param event_id: The ID of the event.
        :param first_name: The first name of the attendee.
        :param last_name: The last name of the attendee.
        :param email: The email address of the attendee.
        :return: Success message or error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Check if the event has reached its maximum capacity
            registered_attendees = self.attendee_model.get_attendees_by_event(event_id)
            if len(registered_attendees) >= event["MaxAttendees"]:
                return "Error: Event has reached its maximum capacity."

            # Register the attendee
            result = self.attendee_model.register_attendee(event_id, first_name, last_name, email)
            return result

        except Exception as e:
            return f"Error registering attendee: {str(e)}"

    def cancel_registration(self, attendee_id):
        """
        Cancels an attendee's registration for an event.
        :param attendee_id: The ID of the attendee to cancel.
        :return: Success message or error message.
        """
        try:
            # Cancel the registration
            result = self.attendee_model.cancel_registration(attendee_id)
            return result

        except Exception as e:
            return f"Error canceling registration: {str(e)}"

    def get_attendees_for_event(self, event_id):
        """
        Retrieves a list of attendees registered for a specific event.
        :param event_id: The ID of the event.
        :return: A list of attendees or an error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Retrieve attendees
            attendees = self.attendee_model.get_attendees_by_event(event_id)
            return attendees

        except Exception as e:
            return f"Error retrieving attendees: {str(e)}"

    def get_attendee_details(self, attendee_id):
        """
        Retrieves details of a specific attendee by their ID.
        :param attendee_id: The ID of the attendee to retrieve.
        :return: A dictionary containing attendee details or an error message.
        """
        try:
            # Retrieve attendee details
            attendee = self.attendee_model.get_attendee_by_id(attendee_id)
            if not attendee:
                return "Error: Attendee not found."

            return attendee

        except Exception as e:
            return f"Error retrieving attendee details: {str(e)}"
