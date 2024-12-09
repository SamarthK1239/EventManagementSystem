from app.models.vendor import Vendor
from app.models.event import Event


class VendorService:
    """
    Service layer for handling vendor-related business logic.
    """

    def __init__(self, db_connection):
        """
        Initialize the VendorService with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection
        self.vendor_model = Vendor(db_connection)
        self.event_model = Event(db_connection)

    def add_vendor(self, vendor_name, service_type, contract_details=None):
        """
        Adds a new vendor to the system.
        :param vendor_name: The name of the vendor.
        :param service_type: The type of service provided by the vendor (e.g., catering, AV equipment).
        :param contract_details: Optional contract terms and conditions for the vendor.
        :return: Success message or error message.
        """
        try:
            result = self.vendor_model.add_vendor(vendor_name, service_type, contract_details)
            return result
        except Exception as e:
            return f"Error adding vendor: {str(e)}"

    def assign_vendor_to_event(self, event_id, vendor_id):
        """
        Assigns a vendor to an event by linking them in the EventVendor table.
        :param event_id: The ID of the event.
        :param vendor_id: The ID of the vendor.
        :return: Success message or error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Check if the vendor exists
            vendor = self.vendor_model.get_vendor_by_id(vendor_id)
            if not vendor:
                return "Error: Vendor not found."

            # Assign the vendor to the event
            result = self.vendor_model.assign_vendor_to_event(event_id, vendor_id)
            return result

        except Exception as e:
            return f"Error assigning vendor to event: {str(e)}"

    def update_vendor_payment_status(self, vendor_id, status):
        """
        Updates the payment status of a specific vendor.
        :param vendor_id: The ID of the vendor.
        :param status: The new payment status ('paid', 'unpaid', 'partial').
        :return: Success message or error message.
        """
        try:
            # Check if the vendor exists
            vendor = self.vendor_model.get_vendor_by_id(vendor_id)
            if not vendor:
                return "Error: Vendor not found."

            # Update payment status
            result = self.vendor_model.update_vendor_payment_status(vendor_id, status)
            return result

        except Exception as e:
            return f"Error updating payment status: {str(e)}"

    def get_vendors_for_event(self, event_id):
        """
        Retrieves all vendors associated with a specific event.
        :param event_id: The ID of the event.
        :return: A list of vendors or an error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Retrieve vendors for this event
            vendors = self.vendor_model.get_vendors_by_event(event_id)
            if not vendors:
                return "No vendors found for this event."

            return vendors

        except Exception as e:
            return f"Error retrieving vendors for event: {str(e)}"

    def get_vendor_details(self, vendor_id):
        """
        Retrieves details of a specific vendor by their ID.
        :param vendor_id: The ID of the vendor to retrieve.
        :return: A dictionary containing vendor details or an error message.
        """
        try:
            # Retrieve details of the specified vendor
            vendor = self.vendor_model.get_vendor_by_id(vendor_id)
            if not vendor:
                return "Error: Vendor not found."

            return vendor

        except Exception as e:
            return f"Error retrieving vendor details: {str(e)}"
