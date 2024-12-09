import os


class Config:
    """
    Configuration class for the Event Management System (EMS).
    Contains database connection details and other environment variables.
    """

    # Database configuration
    MYSQL_HOST = os.getenv("MYSQL_HOST", "localhost")
    MYSQL_PORT = int(os.getenv("MYSQL_PORT", 3306))
    MYSQL_USER = os.getenv("MYSQL_USER", "root")
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD", "password")  # Replace with your MySQL password
    MYSQL_DATABASE = os.getenv("MYSQL_DATABASE", "event_management_system")

    # Other configurations
    DEBUG = os.getenv("DEBUG", "True").lower() in ("true", "1")
    SECRET_KEY = os.getenv("SECRET_KEY", "your_secret_key")  # For session management or encryption
