from app.cli import EventManagementCLI


def main():
    """
    Entry point for the Event Management System (EMS).
    Initializes the CLI and starts the application.
    """
    try:
        # Initialize and run the CLI
        cli = EventManagementCLI()
        cli.run()
    except KeyboardInterrupt:
        print("\nExiting the system. Goodbye!")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        # Ensure resources are properly released
        if 'cli' in locals() and cli.db.connection:
            cli.db.disconnect()


if __name__ == "__main__":
    main()
