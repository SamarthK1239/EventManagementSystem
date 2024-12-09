from app.models.feedback import Feedback
from app.models.event import Event
from app.models.attendee import Attendee

class FeedbackService:
    """
    Service layer for handling feedback-related business logic.
    """

    def __init__(self, db_connection):
        """
        Initialize the FeedbackService with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection
        self.feedback_model = Feedback(db_connection)
        self.event_model = Event(db_connection)
        self.attendee_model = Attendee(db_connection)

    def submit_feedback(self, event_id, attendee_id, rating, comments=None):
        """
        Submits feedback for an event by an attendee.
        :param event_id: The ID of the event.
        :param attendee_id: The ID of the attendee submitting the feedback.
        :param rating: The rating given by the attendee (1-5).
        :param comments: Optional comments provided by the attendee.
        :return: Success message or error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Check if the attendee exists and is registered for the event
            attendee = self.attendee_model.get_attendee_by_id(attendee_id)
            if not attendee or attendee["EventID"] != event_id:
                return "Error: Attendee not registered for this event."

            # Validate rating
            if not (1 <= rating <= 5):
                return "Error: Rating must be between 1 and 5."

            # Submit feedback
            result = self.feedback_model.submit_feedback(event_id, attendee_id, rating, comments)
            return result

        except Exception as e:
            return f"Error submitting feedback: {str(e)}"

    def get_feedback_by_event(self, event_id):
        """
        Retrieves all feedback for a specific event.
        :param event_id: The ID of the event.
        :return: A list of feedback entries or an error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Retrieve feedback
            feedback_entries = self.feedback_model.get_feedback_by_event(event_id)
            if not feedback_entries:
                return "No feedback found for this event."

            return feedback_entries

        except Exception as e:
            return f"Error retrieving feedback: {str(e)}"

    def calculate_average_rating(self, event_id):
        """
        Calculates the average rating for a specific event.
        :param event_id: The ID of the event.
        :return: The average rating or an error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Calculate average rating
            avg_rating = self.feedback_model.calculate_average_rating(event_id)
            if isinstance(avg_rating, str):
                return avg_rating  # Error message from model

            return f"{avg_rating:.2f}"

        except Exception as e:
            return f"Error calculating average rating: {str(e)}"