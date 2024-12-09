import mysql.connector
from mysql.connector import Error


class Feedback:
    def __init__(self, db_connection):
        """
        Initialize the Feedback model with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection

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
            cursor = self.db_connection.cursor()

            # Validate that the rating is within the valid range (1-5)
            if not (1 <= rating <= 5):
                return "Error: Rating must be between 1 and 5."

            # Insert feedback into the database
            query = """
                INSERT INTO Feedback (EventID, AttendeeID, Rating, Comments)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (event_id, attendee_id, rating, comments))
            self.db_connection.commit()

            return "Feedback submitted successfully."

        except Error as e:
            return f"Error submitting feedback: {str(e)}"

    def get_feedback_by_event(self, event_id):
        """
        Retrieves all feedback for a specific event.
        :param event_id: The ID of the event.
        :return: A list of feedback entries or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch all feedback for the given event
            query = "SELECT * FROM Feedback WHERE EventID = %s"
            cursor.execute(query, (event_id,))
            feedback_entries = cursor.fetchall()

            if not feedback_entries:
                return "No feedback found for this event."

            return feedback_entries

        except Error as e:
            return f"Error retrieving feedback: {str(e)}"

    def calculate_average_rating(self, event_id):
        """
        Calculates the average rating for a specific event.
        :param event_id: The ID of the event.
        :return: The average rating or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Calculate average rating for the given event
            query = "SELECT AVG(Rating) AS AverageRating FROM Feedback WHERE EventID = %s"
            cursor.execute(query, (event_id,))
            result = cursor.fetchone()

            if result["AverageRating"] is None:
                return "No ratings available for this event."

            return f"Average Rating: {result['AverageRating']:.2f}"

        except Error as e:
            return f"Error calculating average rating: {str(e)}"

    def get_comments_by_event(self, event_id):
        """
        Retrieves all comments provided for a specific event.
        :param event_id: The ID of the event.
        :return: A list of comments or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch all non-null comments for the given event
            query = "SELECT Comments FROM Feedback WHERE EventID = %s AND Comments IS NOT NULL"
            cursor.execute(query, (event_id,))
            comments = cursor.fetchall()

            if not comments:
                return "No comments found for this event."

            return [comment["Comments"] for comment in comments]

        except Error as e:
            return f"Error retrieving comments: {str(e)}"
