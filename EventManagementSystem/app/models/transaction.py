import mysql.connector
from mysql.connector import Error


class Transaction:
    def __init__(self, db_connection):
        """
        Initialize the Transaction model with a database connection.
        :param db_connection: A MySQL connection object.
        """
        self.db_connection = db_connection

    def record_transaction(self, event_id, vendor_id=None, amount=0.00, status='pending'):
        """
        Records a new financial transaction.
        :param event_id: The ID of the event associated with the transaction.
        :param vendor_id: The ID of the vendor involved in the transaction (optional).
        :param amount: The transaction amount.
        :param status: The status of the transaction ('pending', 'completed', 'failed').
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Insert the transaction into the database
            query = """
                INSERT INTO Transaction (EventID, VendorID, Amount, Status)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (event_id, vendor_id, amount, status))
            self.db_connection.commit()

            return "Transaction recorded successfully."

        except Error as e:
            return f"Error recording transaction: {str(e)}"

    def update_transaction_status(self, transaction_id, status):
        """
        Updates the status of an existing transaction.
        :param transaction_id: The ID of the transaction to update.
        :param status: The new status of the transaction ('completed', 'pending', 'failed').
        :return: Success message or error message.
        """
        try:
            cursor = self.db_connection.cursor()

            # Update the status of the transaction
            query = "UPDATE Transaction SET Status = %s WHERE TransactionID = %s"
            cursor.execute(query, (status, transaction_id))
            self.db_connection.commit()

            if cursor.rowcount == 0:
                return "Transaction not found or no changes made."

            return "Transaction status updated successfully."

        except Error as e:
            return f"Error updating transaction status: {str(e)}"

    def get_transactions_by_event(self, event_id):
        """
        Retrieves all transactions associated with a specific event.
        :param event_id: The ID of the event.
        :return: A list of transactions or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch all transactions for the given event
            query = "SELECT * FROM Transaction WHERE EventID = %s"
            cursor.execute(query, (event_id,))
            transactions = cursor.fetchall()

            if not transactions:
                return "No transactions found for this event."

            return transactions

        except Error as e:
            return f"Error retrieving transactions: {str(e)}"

    def generate_financial_report(self, event_id):
        """
        Generates a financial report for a specific event.
        :param event_id: The ID of the event.
        :return: A dictionary containing total income and expenses or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Calculate total expenses (vendor payments)
            query_expenses = "SELECT SUM(Amount) AS TotalExpenses FROM Transaction WHERE EventID = %s AND Status = 'completed'"
            cursor.execute(query_expenses, (event_id,))
            expenses_result = cursor.fetchone()
            total_expenses = expenses_result["TotalExpenses"] if expenses_result["TotalExpenses"] else 0.00

            # Calculate total income (e.g., ticket sales)
            query_income = "SELECT SUM(Amount) AS TotalIncome FROM Transaction WHERE EventID = %s AND VendorID IS NULL AND Status = 'completed'"
            cursor.execute(query_income, (event_id,))
            income_result = cursor.fetchone()
            total_income = income_result["TotalIncome"] if income_result["TotalIncome"] else 0.00

            return {
                "TotalIncome": total_income,
                "TotalExpenses": total_expenses,
                "NetProfit": total_income - total_expenses
            }

        except Error as e:
            return f"Error generating financial report: {str(e)}"

    def get_transaction_by_id(self, transaction_id):
        """
        Retrieves details of a specific transaction by its ID.
        :param transaction_id: The ID of the transaction to retrieve.
        :return: A dictionary containing transaction details or an error message.
        """
        try:
            cursor = self.db_connection.cursor(dictionary=True)

            # Fetch transaction details
            query = "SELECT * FROM Transaction WHERE TransactionID = %s"
            cursor.execute(query, (transaction_id,))
            transaction = cursor.fetchone()

            if not transaction:
                return "Transaction not found."

            return transaction

        except Error as e:
            return f"Error retrieving transaction details: {str(e)}"
