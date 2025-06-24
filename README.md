DB-B8: IoT Health & Wellness Data Platform
1. Project Overview

This project implements a robust, real-time data engineering pipeline designed to handle data from IoT wearable devices. It successfully demonstrates the collection, processing, and strategic storage of simulated health data (heart rate, physical activity) into three distinct types of databases, showcasing a polyglot persistence approach suitable for modern Big Data applications.

The entire system is containerized using Docker and Docker Compose, ensuring easy deployment and scalability.
2. Key Features

    Real-time Data Ingestion: Uses the lightweight MQTT protocol to handle high-volume data streams from multiple IoT devices.
    Polyglot Persistence: Strategically stores different data types in the most suitable database.
    Topic-Based Routing: A Python subscriber intelligently routes incoming data to the correct database based on the MQTT topic.
    Scalable Architecture: Fully containerized with Docker, allowing for easy scaling of services.
    Live Data Dashboard: A simple web-based frontend built with PHP to visualize the stored data in real-time.
    Graph-Based Data Modeling: Uses Neo4j to model and visualize the relationships between devices and the data they produce.

3. System Architecture

The project follows a classic publisher-subscriber pattern. The architecture is designed to be decoupled and resilient.
Data Flow

    The Publisher (publisher.py) script simulates IoT devices and sends data to the MQTT Broker.
    The MQTT Broker (Mosquitto) receives the data and delivers it to the subscribed Python Subscriber.
    The Subscriber (subscriber.py) processes the message and, based on the topic, routes the data to the correct database.
    The PHP Frontend reads data from the databases (SQLite and MongoDB) to display the live dashboard to the user.

Component Breakdown

    publisher.py: A Python script that simulates multiple wearable devices, generating random but realistic health data and publishing it to the MQTT broker.
    subscriber.py: The core processing engine. This Python script subscribes to all sensor topics, receives the data, and executes the logic to store it in the appropriate database.
    Eclipse Mosquitto: A lightweight MQTT broker running in a Docker container that handles message queuing and delivery.
    Databases: All databases run in their own Docker containers:
        MongoDB: Stores complex, JSON-like documents for physical activity.
        Neo4j: Stores a graph of devices and their produced readings.
        SQLite: A file-based SQL database for structured heart rate data.
    PHP Frontend: An Apache server with PHP that queries the databases and presents a simple, real-time dashboard.

4. Database Schema and Rationale

A key objective of this project was to use the best database for the job.

    SQL (SQLite)
        Data Stored: Heart Rate Readings (timestamp, device_id, heart_rate).
        Rationale: Heart rate data is highly structured and uniform. A relational SQL database is perfect for querying and aggregating this kind of time-series data efficiently.
    NoSQL Document (MongoDB)
        Data Stored: Physical Activity Logs (JSON documents including timestamp, device_id, activity_type, and nested metrics like steps and calories).
        Rationale: Activity data can be more complex and may evolve over time (e.g., adding new metrics). MongoDB's flexible, document-based schema is ideal for storing this semi-structured data without requiring schema migrations.
    NoSQL Graph (Neo4j)
        Data Stored: A graph of (:Device) nodes connected to (:Reading) nodes via [:PRODUCED] relationships.
        Rationale: A graph database excels at managing and querying relationships. This effectively demonstrates how one could model a large network of devices and their interactions for more complex analysis.

5. Technology Stack

    Backend: Python 3
    Libraries: Paho MQTT, PyMongo, Neo4j Driver, python-dotenv
    Databases: SQLite 3, MongoDB 5.0, Neo4j 4.4
    Frontend: PHP 8, Apache Server
    Messaging: Eclipse Mosquitto
    Containerization: Docker & Docker Compose

6. Getting Started

Follow these instructions to set up and run the project locally.
Prerequisites

    Docker Desktop installed and running.
    Python 3 installed.

Installation & Setup

    Clone the Repository:
    Bash

git clone <your-repo-url>
cd <repository-name>

Install Python Dependencies:
Bash

pip install paho-mqtt pymongo neo4j python-dotenv

Create Environment File:
For better security, create a new file named .env in the project's root directory. Add the following line to it, choosing a secure password:

NEO4J_PASS=my-secret-password

Start the System with Docker Compose:
This command will build the custom PHP image and start all services in the background.
Bash

    docker-compose up --build -d

Running the Application

    Start the Subscriber:
    Open a new terminal in the project directory and run:
    Bash

python subscriber.py

Start the Publisher:
Open a second terminal and run:
Bash

    python publisher.py

    View the Live Dashboard:
    Open your web browser and navigate to: http://localhost:8080

7. Future Work

    Real-time Alerts: Implement a component that analyzes data as it arrives and sends an alert if an abnormal reading is detected.
    Advanced Analytics: Use the graph database to perform more complex queries, such as identifying devices that frequently lose connection or correlating activity levels.
    Data Visualization: Enhance the frontend with JavaScript libraries like Chart.js to create dynamic charts and graphs of the incoming data.
