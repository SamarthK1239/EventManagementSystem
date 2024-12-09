from app.models.transaction import Transaction
from app.models.event import Event
from app.models.vendor import Vendor


class TransactionService:
    """
    Service layer for handling transaction-related business logic.
    """

    def __init__(self, db_connection):
        """
        Initialize the TransactionService with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection
        self.transaction_model = Transaction(db_connection)
        self.event_model = Event(db_connection)
        self.vendor_model = Vendor(db_connection)

    def record_transaction(self, event_id, vendor_id=None, amount=0.00, status='pending'):
        """
        Records a new financial transaction for an event or vendor.
        :param event_id: The ID of the event associated with the transaction.
        :param vendor_id: The ID of the vendor involved in the transaction (optional).
        :param amount: The transaction amount.
        :param status: The status of the transaction ('pending', 'completed', 'failed').
        :return: Success message or error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # If vendor is specified, check if the vendor exists
            if vendor_id:
                vendor = self.vendor_model.get_vendor_by_id(vendor_id)
                if not vendor:
                    return "Error: Vendor not found."

            # Record the transaction
            result = self.transaction_model.record_transaction(event_id, vendor_id, amount, status)
            return result

        except Exception as e:
            return f"Error recording transaction: {str(e)}"

    def update_transaction_status(self, transaction_id, status):
        """
        Updates the status of an existing transaction.
        :param transaction_id: The ID of the transaction to update.
        :param status: The new status of the transaction ('completed', 'pending', 'failed').
        :return: Success message or error message.
        """
        try:
            # Check if the transaction exists
            transaction = self.transaction_model.get_transaction_by_id(transaction_id)
            if not transaction:
                return "Error: Transaction not found."

            # Update the transaction status
            result = self.transaction_model.update_transaction_status(transaction_id, status)
            return result

        except Exception as e:
            return f"Error updating transaction status: {str(e)}"

    def get_transactions_for_event(self, event_id):
        """
        Retrieves all transactions associated with a specific event.
        :param event_id: The ID of the event.
        :return: A list of transactions or an error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Retrieve transactions for this event
            transactions = self.transaction_model.get_transactions_by_event(event_id)
            if not transactions:
                return "No transactions found for this event."

            return transactions

        except Exception as e:
            return f"Error retrieving transactions for event: {str(e)}"

    def generate_financial_report(self, event_id):
        """
        Generates a financial report for a specific event.
        :param event_id: The ID of the event.
        :return: A dictionary containing total income, expenses, and net profit or an error message.
        """
        try:
            # Check if the event exists
            event = self.event_model.get_event_by_id(event_id)
            if not event:
                return "Error: Event not found."

            # Generate financial report
            report = self.transaction_model.generate_financial_report(event_id)
            return report

        except Exception as e:
            return f"Error generating financial report: {str(e)}"

    def get_transaction_details(self, transaction_id):
        """
        Retrieves details of a specific transaction by its ID.
        :param transaction_id: The ID of the transaction to retrieve.
        :return: A dictionary containing transaction details or an error message.
        """
        try:
            # Retrieve transaction details by ID
            transaction = self.transaction_model.get_transaction_by_id(transaction_id)
            if not transaction:
                return "Error: Transaction not found."

            return transaction

        except Exception as e:
            return f"Error retrieving transaction details: {str(e)}"
