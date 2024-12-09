from app.models.schedule import Schedule
from app.models.event import Event


class ScheduleService:
    """
    Service layer for handling schedule-related business logic.
    """

    def __init__(self, db_connection):
        """
        Initialize the ScheduleService with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection
        self.schedule_model = Schedule(db_connection)
        self.event_model = Event(db_connection)

    def add_schedule(self, event_id, session_name, start_time, end_time, speaker_name=None, room=None):
        """
        Adds a new session to the schedule for a specific event after validating time conflicts.
        :param event_id: The ID of the event.
        :param session_name: The name of the session or activity.
        :param start_time: The start time of the session.
        :param end_time: The end time of the session.
        :param speaker_name: Optional name of the speaker.
        :param room: Optional room or location of the session.
        :return: Success message or error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Check for time conflicts in the same room
            if room:
                existing_schedules = self.schedule_model.get_schedule_by_event(event_id)
                for schedule in existing_schedules:
                    if schedule["Room"] == room and (
                            (schedule["StartTime"] <= start_time < schedule["EndTime"]) or
                            (schedule["StartTime"] < end_time <= schedule["EndTime"])
                    ):
                        return f"Error: Time conflict detected in room {room}."

            # Add the session to the schedule
            result = self.schedule_model.add_schedule(event_id, session_name, start_time, end_time, speaker_name, room)
            return result

        except Exception as e:
            return f"Error adding schedule: {str(e)}"

    def update_schedule(self, schedule_id, **kwargs):
        """
        Updates an existing session in the schedule.
        :param schedule_id: The ID of the schedule entry to update.
        :param kwargs: Key-value pairs of fields to update (e.g., SessionName='New Name').
        :return: Success message or error message.
        """
        try:
            # Check if the schedule exists
            schedule = self.schedule_model.get_schedule_by_id(schedule_id)
            if not schedule:
                return "Error: Schedule not found."

            # Update the session details
            result = self.schedule_model.update_schedule(schedule_id, **kwargs)
            return result

        except Exception as e:
            return f"Error updating schedule: {str(e)}"

    def delete_schedule(self, schedule_id):
        """
        Deletes a specific session from the schedule.
        :param schedule_id: The ID of the schedule entry to delete.
        :return: Success message or error message.
        """
        try:
            # Check if the schedule exists
            schedule = self.schedule_model.get_schedule_by_id(schedule_id)
            if not schedule:
                return "Error: Schedule not found."

            # Delete the session
            result = self.schedule_model.delete_schedule(schedule_id)
            return result

        except Exception as e:
            return f"Error deleting schedule: {str(e)}"

    def get_schedule_for_event(self, event_id):
        """
        Retrieves all sessions for a specific event.
        :param event_id: The ID of the event whose schedule is to be retrieved.
        :return: A list of sessions or an error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Retrieve all sessions for this event
            schedules = self.schedule_model.get_schedule_by_event(event_id)
            if not schedules:
                return "No schedules found for this event."

            return schedules

        except Exception as e:
            return f"Error retrieving schedules for event: {str(e)}"

    def get_schedule_details(self, schedule_id):
        """
        Retrieves details of a specific session by its ID.
        :param schedule_id: The ID of the session to retrieve.
        :return: A dictionary containing session details or an error message.
        """
        try:
            # Retrieve session details by ID
            schedule = self.schedule_model.get_schedule_by_id(schedule_id)
            if not schedule:
                return "Error: Schedule not found."

            return schedule

        except Exception as e:
            return f"Error retrieving session details: {str(e)}"
