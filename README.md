# EventManagementSystem

## Required Environments/Prerequisites

The required items to run this application are:

- MySQL server + Workbench (makes setup easier)
- Python 3.x (preferably 3.12 or later)
    - Required Packages
        - bcrypt
        - python-dotenv
        - mysql-connector-python
- If the MySQL instance is being set up as a remotely accessible database server, then an internet connection is also required. However, the application has not been extensively tested to support this use case.

## Deploying an instance of this Event Management System

Deployment can largely be broken down into two steps:

1. Database Setup and Initialization
    1. This step only needs to be carried out once
    2. Some tables (listed below) need to be populated with relevant data before the system is ready for use.
2. Application Installation
    1. This step needs to be carried out individually for each computer that needs to use the Event Management System.

### 1. Database Setup and Initialization

The database can be created with this script, which creates tables in an order that ensures that no table is created referencing foreign keys or constraints that have not yet been created:

```sql
CREATE TABLE User (
    UserID INT AUTO_INCREMENT PRIMARY KEY,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Email VARCHAR(255) UNIQUE NOT NULL,
    Role ENUM('admin', 'organizer') DEFAULT 'organizer',
    Password VARCHAR(255) NOT NULL
);

CREATE TABLE Venue (
    VenueID INT AUTO_INCREMENT PRIMARY KEY,
    VenueName VARCHAR(255) NOT NULL,
    Location VARCHAR(255) NOT NULL,
    Capacity INT NOT NULL,
    CostPerDay DECIMAL(10,2) DEFAULT 0.00,
    AvailabilityStatus ENUM('available', 'booked') DEFAULT 'available'
);

CREATE TABLE Event (
    EventID INT AUTO_INCREMENT PRIMARY KEY,
    UserID INT,
    EventName VARCHAR(255) NOT NULL,
    EventDate DATE NOT NULL,
    EventVenue INT,  -- Assuming this references VenueID
    MaxAttendees INT DEFAULT 0,
    Budget DECIMAL(10,2) DEFAULT 0.00,
    FOREIGN KEY (UserID) REFERENCES User(UserID),
    FOREIGN KEY (EventVenue) REFERENCES Venue(VenueID)
);

CREATE TABLE Attendee (
    AttendeeID INT AUTO_INCREMENT PRIMARY KEY,
    EventID INT,
    FirstName VARCHAR(100) NOT NULL,
    LastName VARCHAR(100) NOT NULL,
    Email VARCHAR(255) NOT NULL,
    RegistrationDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (EventID) REFERENCES Event(EventID)
);

CREATE TABLE Schedule (
    ScheduleID INT AUTO_INCREMENT PRIMARY KEY,
    EventID INT,
    SessionName VARCHAR(255) NOT NULL,
    StartTime DATETIME NOT NULL,
    EndTime DATETIME NOT NULL,
    SpeakerName VARCHAR(255),
    Room VARCHAR(100),
    FOREIGN KEY (EventID) REFERENCES Event(EventID)
);

CREATE TABLE Vendor (
    VendorID INT AUTO_INCREMENT PRIMARY KEY,
    VendorName VARCHAR(255) NOT NULL,
    ServiceType VARCHAR(100) NOT NULL,
    ContractDetails TEXT DEFAULT NULL,
    PaymentStatus ENUM('paid', 'unpaid', 'partial') DEFAULT 'unpaid'
);

CREATE TABLE Transaction (
    TransactionID INT AUTO_INCREMENT PRIMARY KEY,
    EventID INT,
    VendorID INT,
    Amount DECIMAL(10,2) NOT NULL,
    TransactionDate DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    Status ENUM('completed', 'pending', 'failed') DEFAULT 'pending',
    FOREIGN KEY (EventID) REFERENCES Event(EventID),
    FOREIGN KEY (VendorID) REFERENCES Vendor(VendorID)
);

CREATE TABLE Feedback (
    FeedbackID INT AUTO_INCREMENT PRIMARY KEY,
    EventID INT,
    AttendeeID INT,
    Rating INT NOT NULL CHECK (Rating BETWEEN 1 AND 5),
    Comments TEXT DEFAULT NULL,
    FOREIGN KEY (EventID) REFERENCES Event(EventID),
    FOREIGN KEY (AttendeeID) REFERENCES Attendee(AttendeeID)
);
```

After this, initialize the tables:

1. Venue
2. Vendor

In a real world environment, this part of the setup process would be assisted and would allow the business that purchased the software to enter the various venues and vendors they have already worked with or intend to work with.

After this is done, ensure that you make a note of the database server’s (MySQL) connection port number, the name of your database, and the username and password used to connect to the database server.

That concludes the setup process for the database. It is now ready to be used by the user-facing application.

### 2. Application Installation

This process is also relatively simple, just clone the project from the GitHub repository, unzip the file, and then locate the `run.py` file. This is the main file that handles running all aspects of the system. Do not run this file yet, as it will return a large number of errors.

Instead, under the `app` directory, locate the folder titled `environment_variables`, if it doesn’t exist, create a folder with that exact name. Within it, create a new file with the name `.env`. There should not be anything before the `.` .

Once that has been created, copy the code below and paste it within, and then edit the values to reflect the details you collected from the database server in the previous step:

```xml
host="127.0.0.1" ## Localhost
port="3306" ## Default MySQL port
user="root" ## All Access
password="Your Password Here"
database="Your Database Name Here"
```

This will allow the application to connect to the database we set up in the previous step. Keep a copy of this file on hand so that it can be used when a new machine needs to be set up to use the event management system.

This concludes the setup of the application on a new machine. It is now ready to be used by end users.

## Functionality

When the application is first launched, the system provides a starting page that provides all user-accessible options, and allows the selection of any item:

```xml
Main Menu:
1. User Management
2. Event Management
3. Attendee Management
4. Schedule Management
5. Venue Management
6. Vendor Management
7. Transactions
8. Feedback Management
9. Exit
Enter your choice: 
```

Each section is largely self explanatory, with guidance provided at steps that have the potential for causing confusion.

### User Management

User management allows system users to be added, removed, viewed and authenticated:

```xml
User Management:
1. Register User
2. Authenticate User
3. View All Users
Enter your choice: 
```

Sample registration:

```xml
Enter your choice: 1
First Name: Samarth
Last Name: Kulkarni
Email: ssk5542@psu.edu
Password: Password123
Role (admin/organizer): organizer
Success: User Registered Successfully.
```

### Event Management

Event Management allows new events to be created, updated, deleted and viewed:

```xml
Event Management:
1. Create Event
2. Update Event
3. Delete Event
4. View All Events
Enter your choice: 
```

Sample creation:

```xml
Enter your choice: 1
Organizer User ID: 2
Event Name: Christmas Party
Event Date (YYYY-MM-DD): 2024-12-15
Venue ID: 2
Max Attendees: 350
Budget: 103000
Event created successfully.
```

### Attendee Management

Attendee management allows new attendees to be registered or unregistered for/from events, and allows attendees to be viewed by event:

```xml
Attendee Management:
1. Register Attendee
2. Cancel Registration
3. View Attendees for an Event
Enter your choice: 
```

Sample Creation:

```xml
Enter your choice: 1
Event ID: 5
First Name: Sam
Last Name: Kulkarni
Email: qasdlkj@aslkne.sja
Registration successful.
```

### Schedule Management

Schedule management allows for the schedule of a particular event to be set and modified. There are checks in place to ensure that rooms are not double booked, and each item in the schedule is linked to a particular (Already created) event:

```xml
Schedule Management:
1. Add Session
2. Update Session
3. Delete Session
4. View Schedule for an Event
Enter your choice: 
```

Sample Creation:

```xml
Enter your choice: 1
Event ID: 5
Session Name: Speaking about the year
Start Time (YYYY-MM-DD HH:MM:SS): 2024-12-15 15:00:00
End Time (YYYY-MM-DD HH:MM:SS): 2024-12-15 17:00:00
Speaker Name (optional): Multiple Speakers
Room (optional): Main Hall
Session added to Schedule.
```

### Venue Management

Venue management allows venues to be added, removed and viewed by availability status.

```xml
Venue Management:
1. Add Venue
2. View Available Venues
3. Assign Venue to Event
4. Release Venue
Enter your choice: 
```

Sample Creation:

```xml
Enter your choice: 1
Venue Name: Venue 3
Location: Location 3
Capacity: 2500
Cost Per Day: 275000
Venue added successfully.
```

### Vendor Management

Vendor management allows vendors to be added, assigned to events, paid and viewed by event.

```xml
Vendor Management:
1. Add Vendor
2. Assign Vendor to Event
3. Update Vendor Payment Status
4. View Vendors for an Event
Enter your choice: 
```

Sample Creation:

```xml
Enter your choice: 1
Vendor Name: Vendor 4
Service Type (e.g., Catering, AV Equipment): Media Equipment
Contract Details (optional): Contract Details
Vendor added successfully.
```

### Transactions

The Transactions section allows the organizers to keep track of any and all transactions made during the event, as a digital log. This log can then be viewed and a financial report can be generated.

```xml
Transactions:
1. Record Transaction
2. Update Transaction Status
3. View Transactions for an Event
4. Generate Financial Report
Enter your choice: 
```

Sample Creation:

```xml
Enter your choice: 1
Event ID: 5
Vendor ID (leave blank if not applicable): 
Transaction Amount: 1200
Transaction Status ('pending', 'completed', 'failed'): completed
Transaction recorded successfully.
```

### Feedback Management

Feedback management allows feedback for a particular event to be recorded and viewed:

```xml
Feedback Management:
1. Submit Feedback
2. View Feedback for an Event
Enter your choice: 
```

Sample Creation:

```xml
Enter your choice: 1
Event ID: 5
Attendee ID: 3
Rating (1-5): 5
Comments (optional): Comments Comments Comments
Feedback submitted successfully.
```
