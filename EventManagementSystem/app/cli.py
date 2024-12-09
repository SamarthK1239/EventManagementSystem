import sys
from EventManagementSystem.app.database import Database
from EventManagementSystem.app.services.user_service import UserService
from EventManagementSystem.app.services.event_service import EventService
from EventManagementSystem.app.services.attendee_service import AttendeeService
from EventManagementSystem.app.services.schedule_service import ScheduleService
from EventManagementSystem.app.services.venue_service import VenueService
from EventManagementSystem.app.services.vendor_service import VendorService
from EventManagementSystem.app.services.transaction_service import TransactionService
from EventManagementSystem.app.services.feedback_service import FeedbackService


class EventManagementCLI:
    """
    Command Line Interface for the Event Management System.
    """

    def __init__(self):
        self.db = Database()
        self.connection = self.db.connect()

        # Initialize services
        self.user_service = UserService(self.connection)
        self.event_service = EventService(self.connection)
        self.attendee_service = AttendeeService(self.connection)
        self.schedule_service = ScheduleService(self.connection)
        self.venue_service = VenueService(self.connection)
        self.vendor_service = VendorService(self.connection)
        self.transaction_service = TransactionService(self.connection)
        self.feedback_service = FeedbackService(self.connection)

    def run(self):
        """
        Main loop for the CLI.
        """
        print("Welcome to the Event Management System!")
        while True:
            print("\nMain Menu:")
            print("1. User Management")
            print("2. Event Management")
            print("3. Attendee Management")
            print("4. Schedule Management")
            print("5. Venue Management")
            print("6. Vendor Management")
            print("7. Transactions")
            print("8. Feedback Management")  # Added option for Feedback Management
            print("9. Exit")

            choice = input("Enter your choice: ")
            if choice == "1":
                self.user_management()
            elif choice == "2":
                self.event_management()
            elif choice == "3":
                self.attendee_management()
            elif choice == "4":
                self.schedule_management()
            elif choice == "5":
                self.venue_management()
            elif choice == "6":
                self.vendor_management()
            elif choice == "7":
                self.transactions()
            elif choice == "8":
                self.feedback_management()  # Added call to feedback_management
            elif choice == "9":
                print("Exiting the system. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")

    def user_management(self):
        """
        Handles user-related operations.
        """
        print("\nUser Management:")
        print("1. Register User")
        print("2. Authenticate User")
        print("3. View All Users")

        choice = input("Enter your choice: ")
        if choice == "1":
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Email: ")
            password = input("Password: ")
            role = input("Role (admin/organizer): ").strip().lower() or "organizer"
            result = self.user_service.register_user(first_name, last_name, email, password, role)
            print(format_output(result))
        elif choice == "2":
            email = input("Email: ")
            password = input("Password: ")
            result = self.user_service.authenticate_user(email, password)
            print(format_output(result))
        elif choice == "3":
            users = self.user_service.get_all_users()
            print(format_output(users))

    def event_management(self):
        """
        Handles event-related operations.
        """
        print("\nEvent Management:")
        print("1. Create Event")
        print("2. Update Event")
        print("3. Delete Event")
        print("4. View All Events")

        choice = input("Enter your choice: ")
        if choice == "1":
            user_id = int(input("Organizer User ID: "))
            event_name = input("Event Name: ")
            event_date = input("Event Date (YYYY-MM-DD): ")
            venue_id = int(input("Venue ID: "))
            max_attendees = int(input("Max Attendees: "))
            budget = float(input("Budget: "))
            result = self.event_service.create_event(user_id, event_name, event_date, venue_id, max_attendees, budget)
            print(format_output(result))
        elif choice == "2":
            event_id = int(input("Event ID: "))
            updates = {}
            updates["EventName"] = input("New Event Name (leave blank to skip): ") or None
            updates["MaxAttendees"] = int(input("New Max Attendees (leave blank to skip): ") or 0)
            result = self.event_service.update_event(event_id, **{k: v for k, v in updates.items() if v})
            print(format_output(result))
        elif choice == "3":
            event_id = int(input("Event ID to delete: "))
            result = self.event_service.delete_event(event_id)
            print(format_output(result))
        elif choice == "4":
            events = self.event_service.get_all_events()
            print(format_output(events))
        else:
            print("Invalid choice. Please try again.")

    def attendee_management(self):
        """
        Handles attendee-related operations.
        """
        print("\nAttendee Management:")
        print("1. Register Attendee")
        print("2. Cancel Registration")
        print("3. View Attendees for an Event")

        choice = input("Enter your choice: ")
        if choice == "1":
            event_id = int(input("Event ID: "))
            first_name = input("First Name: ")
            last_name = input("Last Name: ")
            email = input("Email: ")
            result = self.attendee_service.register_attendee(event_id, first_name, last_name, email)
            print(format_output(result))
        elif choice == "2":
            attendee_id = int(input("Attendee ID to cancel registration for: "))
            result = self.attendee_service.cancel_registration(attendee_id)
            print(format_output(result))
        elif choice == "3":
            event_id = int(input("Event ID to view attendees for: "))
            attendees = self.attendee_service.get_attendees_for_event(event_id)
            print(format_output(attendees))
        else:
            print("Invalid choice. Please try again.")

    def schedule_management(self):
        """
        Handles schedule-related operations.
        """
        print("\nSchedule Management:")
        print("1. Add Session")
        print("2. Update Session")
        print("3. Delete Session")
        print("4. View Schedule for an Event")

        choice = input("Enter your choice: ")
        if choice == "1":
            event_id = int(input("Event ID: "))
            session_name = input("Session Name: ")
            start_time = input("Start Time (YYYY-MM-DD HH:MM:SS): ")
            end_time = input("End Time (YYYY-MM-DD HH:MM:SS): ")
            speaker_name = input("Speaker Name (optional): ") or None
            room = input("Room (optional): ") or None
            result = self.schedule_service.add_schedule(event_id, session_name, start_time, end_time, speaker_name,
                                                        room)
            print(format_output(result))
        elif choice == "2":
            schedule_id = int(input("Schedule ID to update: "))
            updates = {}
            updates["SessionName"] = input("New Session Name (leave blank to skip): ") or None
            updates["StartTime"] = input("New Start Time (YYYY-MM-DD HH:MM:SS, leave blank to skip): ") or None
            updates["EndTime"] = input("New End Time (YYYY-MM-DD HH:MM:SS, leave blank to skip): ") or None
            updates["SpeakerName"] = input("New Speaker Name (leave blank to skip): ") or None
            updates["Room"] = input("New Room (leave blank to skip): ") or None
            result = self.schedule_service.update_schedule(schedule_id, **{k: v for k, v in updates.items() if v})
            print(format_output(result))
        elif choice == "3":
            schedule_id = int(input("Schedule ID to delete: "))
            result = self.schedule_service.delete_schedule(schedule_id)
            print(format_output(result))
        elif choice == "4":
            event_id = int(input("Event ID to view schedule for: "))
            schedules = self.schedule_service.get_schedule_for_event(event_id)
            print(format_output(schedules))
        else:
            print("Invalid choice. Please try again.")

    def venue_management(self):
        """
        Handles venue-related operations.
        """
        print("\nVenue Management:")
        print("1. Add Venue")
        print("2. View Available Venues")
        print("3. Assign Venue to Event")
        print("4. Release Venue")

        choice = input("Enter your choice: ")
        if choice == "1":
            venue_name = input("Venue Name: ")
            location = input("Location: ")
            capacity = int(input("Capacity: "))
            cost_per_day = float(input("Cost Per Day: "))
            result = self.venue_service.add_venue(venue_name, location, capacity, cost_per_day)
            print(format_output(result))
        elif choice == "2":
            venues = self.venue_service.get_available_venues()
            print(format_output(venues))
        elif choice == "3":
            event_id = int(input("Event ID: "))
            venue_id = int(input("Venue ID to assign: "))
            result = self.venue_service.assign_venue_to_event(event_id, venue_id)
            print(format_output(result))
        elif choice == "4":
            venue_id = int(input("Venue ID to release: "))
            result = self.venue_service.release_venue(venue_id)
            print(format_output(result))
        else:
            print("Invalid choice. Please try again.")

    def vendor_management(self):
        """
        Handles vendor-related operations.
        """
        print("\nVendor Management:")
        print("1. Add Vendor")
        print("2. Assign Vendor to Event")
        print("3. Update Vendor Payment Status")
        print("4. View Vendors for an Event")

        choice = input("Enter your choice: ")
        if choice == "1":
            vendor_name = input("Vendor Name: ")
            service_type = input("Service Type (e.g., Catering, AV Equipment): ")
            contract_details = input("Contract Details (optional): ") or None
            result = self.vendor_service.add_vendor(vendor_name, service_type, contract_details)
            print(format_output(result))
        elif choice == "2":
            event_id = int(input("Event ID: "))
            vendor_id = int(input("Vendor ID to assign: "))
            result = self.vendor_service.assign_vendor_to_event(event_id, vendor_id)
            print(format_output(result))
        elif choice == "3":
            vendor_id = int(input("Vendor ID to update payment status for: "))
            status = input("New Payment Status ('paid', 'unpaid', 'partial'): ").strip().lower()
            result = self.vendor_service.update_vendor_payment_status(vendor_id, status)
            print(format_output(result))
        elif choice == "4":
            event_id = int(input("Event ID to view vendors for: "))
            vendors = self.vendor_service.get_vendors_for_event(event_id)
            print(format_output(vendors))
        else:
            print("Invalid choice. Please try again.")

    def transactions(self):
        """
        Handles transaction-related operations.
        """
        print("\nTransactions:")
        print("1. Record Transaction")
        print("2. Update Transaction Status")
        print("3. View Transactions for an Event")
        print("4. Generate Financial Report")

        choice = input("Enter your choice: ")
        if choice == "1":
            event_id = int(input("Event ID: "))
            vendor_id_input = input("Vendor ID (leave blank if not applicable): ")
            vendor_id = int(vendor_id_input) if vendor_id_input else None
            amount = float(input("Transaction Amount: "))
            status = input("Transaction Status ('pending', 'completed', 'failed'): ").strip().lower()
            result = self.transaction_service.record_transaction(event_id, vendor_id, amount, status)
            print(result)
        elif choice == "2":
            transaction_id = int(input("Transaction ID to update: "))
            status = input("New Transaction Status ('pending', 'completed', 'failed'): ").strip().lower()
            result = self.transaction_service.update_transaction_status(transaction_id, status)
            print(result)
        elif choice == "3":
            event_id = int(input("Event ID to view transactions for: "))
            transactions = self.transaction_service.get_transactions_for_event(event_id)
            if isinstance(transactions, str):
                print(transactions)  # Error message
            else:
                for transaction in transactions:
                    print(transaction)
        elif choice == "4":
            event_id = int(input("Event ID to generate financial report for: "))
            report = self.transaction_service.generate_financial_report(event_id)
            if isinstance(report, str):
                print(report)  # Error message
            else:
                print(f"Total Expenses: {report['TotalExpenses']}")
        else:
            print("Invalid choice. Please try again.")

    def feedback_management(self):
        """
        Handles feedback-related operations.
        """
        print("\nFeedback Management:")
        print("1. Submit Feedback")
        print("2. View Feedback for an Event")

        choice = input("Enter your choice: ")
        if choice == "1":
            event_id = int(input("Event ID: "))
            attendee_id = int(input("Attendee ID: "))
            rating = int(input("Rating (1-5): "))
            comments = input("Comments (optional): ") or None
            result = self.feedback_service.submit_feedback(event_id, attendee_id, rating, comments)
            print(result)
        elif choice == "2":
            event_id = int(input("Event ID to view feedback for: "))
            feedbacks = self.feedback_service.get_feedback_by_event(event_id)
            if isinstance(feedbacks, str):
                print(feedbacks)  # Error message
            else:
                for feedback in feedbacks:
                    print(feedback)
                avg_rating = self.feedback_service.calculate_average_rating(event_id)
                if isinstance(avg_rating, str):
                    print(avg_rating)  # Error message
                else:
                    print(f"Average Rating: {avg_rating}")
        else:
            print("Invalid choice. Please try again.")

    def analytics_and_reports(self):
        """
        Handles analytical reports and insights.
        """
        print("\nAnalytics and Reports:")
        print("1. Total Attendees Per Event")
        print("2. Revenue Report by Vendor")

        choice = input("Enter your choice: ")
        if choice == "1":
            attendees_report = self.analytics_service.get_total_attendees_per_event()
            if isinstance(attendees_report, str):
                print(attendees_report)  # Error message
            else:
                for report in attendees_report:
                    print(report)
        elif choice == "2":
            revenue_report = self.analytics_service.get_revenue_report_by_vendor()
            if isinstance(revenue_report, str):
                print(revenue_report)  # Error message
            else:
                for report in revenue_report:
                    print(report)
        else:
            print("Invalid choice. Please try again.")


def format_output(data):
    """
    Formats the output data into a readable string.
    :param data: The data to format (dictionary or list of dictionaries).
    :return: A formatted string.
    """
    if isinstance(data, dict):
        return '\n'.join([f"{key}: {value}" for key, value in data.items()])
    elif isinstance(data, list):
        return '\n\n'.join([format_output(item) for item in data])
    else:
        return str(data)
