import mysql.connector
from mysql.connector import Error


class Vendor:
    def __init__(self, db_connection):
        """
        Initialize the Vendor model with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection

    def add_vendor(self, vendor_name, service_type, contract_details=None):
        """
        Adds a new vendor to the system.
        :param vendor_name: The name of the vendor.
        :param service_type: The type of service provided by the vendor (e.g., catering, AV equipment).
        :param contract_details: Optional contract details for the vendor.
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Insert new vendor into the database
            query = """
                INSERT INTO Vendor (VendorName, ServiceType, ContractDetails)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (vendor_name, service_type, contract_details))
            self.db_connection.commit()

            return "Vendor added successfully."

        except Error as e:
            return f"Error adding vendor: {str(e)}"

    def assign_vendor_to_event(self, event_id, vendor_id):
        """
        Links a vendor to an event using the EventVendor junction table.
        :param event_id: The ID of the event.
        :param vendor_id: The ID of the vendor.
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Insert record into EventVendor junction table
            query = """
                INSERT INTO EventVendor (EventID, VendorID)
                VALUES (%s, %s)
            """
            cursor.execute(query, (event_id, vendor_id))
            self.db_connection.commit()

            return "Vendor assigned to event successfully."

        except Error as e:
            return f"Error assigning vendor to event: {str(e)}"

    def update_vendor_payment_status(self, vendor_id, status):
        """
        Updates the payment status of a vendor.
        :param vendor_id: The ID of the vendor.
        :param status: The new payment status ('paid', 'unpaid', 'partial').
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Update payment status for the given vendor
            query = "UPDATE Vendor SET PaymentStatus = %s WHERE VendorID = %s"
            cursor.execute(query, (status, vendor_id))
            self.db_connection.commit()

            if cursor.rowcount == 0:
                return "Vendor not found or no changes made."

            return "Vendor payment status updated successfully."

        except Error as e:
            return f"Error updating payment status: {str(e)}"

    def get_vendors_by_event(self, event_id):
        """
        Retrieves all vendors associated with a specific event.
        :param event_id: The ID of the event.
        :return: A list of vendors or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch vendors linked to the given event
            query = """
                SELECT V.VendorID, V.VendorName, V.ServiceType, V.PaymentStatus 
                FROM Vendor V
                JOIN EventVendor EV ON V.VendorID = EV.VendorID
                WHERE EV.EventID = %s
            """
            cursor.execute(query, (event_id,))
            vendors = cursor.fetchall()

            if not vendors:
                return "No vendors found for this event."

            return vendors

        except Error as e:
            return f"Error retrieving vendors for event: {str(e)}"

    def get_vendor_by_id(self, vendor_id):
        """
        Retrieves details of a specific vendor by their ID.
        :param vendor_id: The ID of the vendor to retrieve.
        :return: A dictionary containing vendor details or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch vendor details by ID
            query = "SELECT * FROM Vendor WHERE VendorID = %s"
            cursor.execute(query, (vendor_id,))
            vendor = cursor.fetchone()

            if not vendor:
                return "Vendor not found."

            return vendor

        except Error as e:
            return f"Error retrieving vendor details: {str(e)}"
