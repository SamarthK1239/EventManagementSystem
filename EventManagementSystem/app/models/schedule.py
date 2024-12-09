import mysql.connector
from mysql.connector import Error


class Schedule:
    def __init__(self, db_connection):
        """
        Initialize the Schedule model with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection

    def add_schedule(self, event_id, session_name, start_time, end_time, speaker_name=None, room=None):
        """
        Adds a new session to the schedule for a specific event.
        :param event_id: The ID of the event.
        :param session_name: The name of the session or activity.
        :param start_time: The start time of the session.
        :param end_time: The end time of the session.
        :param speaker_name: The name of the speaker (optional).
        :param room: The room where the session will take place (optional).
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Check for time conflicts in the same room
            if room:
                query = """
                    SELECT * FROM Schedule 
                    WHERE Room = %s AND EventID = %s AND 
                    (%s BETWEEN StartTime AND EndTime OR %s BETWEEN StartTime AND EndTime)
                """
                cursor.execute(query, (room, event_id, start_time, end_time))
                conflict = cursor.fetchone()

                if conflict:
                    return "Error: Time conflict detected in the same room."

            # Insert new session into the database
            query = """
                INSERT INTO Schedule (EventID, SessionName, StartTime, EndTime, SpeakerName, Room)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (event_id, session_name, start_time, end_time, speaker_name, room))
            self.db_connection.commit()

            return "Session added successfully."

        except Error as e:
            return f"Error adding session: {str(e)}"

    def update_schedule(self, schedule_id, **kwargs):
        """
        Updates an existing session in the schedule.
        :param schedule_id: The ID of the schedule entry to update.
        :param kwargs: Key-value pairs of fields to update (e.g., SessionName='New Name').
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Build dynamic query based on provided fields
            fields = ", ".join([f"{key} = %s" for key in kwargs.keys()])
            values = list(kwargs.values())

            query = f"UPDATE Schedule SET {fields} WHERE ScheduleID = %s"
            values.append(schedule_id)

            cursor.execute(query, tuple(values))
            self.db_connection.commit()

            if cursor.rowcount == 0:
                return "No changes made or schedule not found."

            return "Schedule updated successfully."

        except Error as e:
            return f"Error updating schedule: {str(e)}"

    def delete_schedule(self, schedule_id):
        """
        Deletes a specific session from the schedule.
        :param schedule_id: The ID of the schedule entry to delete.
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Delete schedule entry
            query = "DELETE FROM Schedule WHERE ScheduleID = %s"
            cursor.execute(query, (schedule_id,))
            self.db_connection.commit()

            if cursor.rowcount == 0:
                return "Schedule not found or already deleted."

            return "Schedule deleted successfully."

        except Error as e:
            return f"Error deleting schedule: {str(e)}"

    def get_schedule_by_event(self, event_id):
        """
        Retrieves all sessions for a specific event.
        :param event_id: The ID of the event whose schedule is to be retrieved.
        :return: A list of sessions or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch all sessions for the given event
            query = "SELECT * FROM Schedule WHERE EventID = %s ORDER BY StartTime"
            cursor.execute(query, (event_id,))
            schedules = cursor.fetchall()

            if not schedules:
                return "No schedules found for this event."

            return schedules

        except Error as e:
            return f"Error retrieving schedules: {str(e)}"

    def get_schedule_by_id(self, schedule_id):
        """
        Retrieves details of a specific session by its ID.
        :param schedule_id: The ID of the schedule entry to retrieve.
        :return: A dictionary with session details or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch session details
            query = "SELECT * FROM Schedule WHERE ScheduleID = %s"
            cursor.execute(query, (schedule_id,))
            schedule = cursor.fetchone()

            if not schedule:
                return "Schedule not found."

            return schedule

        except Error as e:
            return f"Error retrieving schedule details: {str(e)}"
