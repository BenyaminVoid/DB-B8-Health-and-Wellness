# Project: Integration of MQTT and Python for Big Data Analysis and Storage (DB-B8 Health and Wellness)

## 1. Project Description

[cite_start]This project successfully implements a system to collect, process, and store large volumes of data from simulated IoT wearable devices. The system uses the MQTT protocol for real-time data ingestion and Python for processing. [cite_start]Based on the data topic, it is then stored in three different database platforms: SQLite (SQL), MongoDB (NoSQL), and Neo4j (Graph).

## 2. System Architecture

The system follows a publisher-subscriber architecture, orchestrated with Docker to ensure modularity and ease of deployment.

**Data Flow:**
1.  **Publisher (`publisher.py`):** A Python script simulates one or more wearable devices, generating health data (heart rate, activity) and publishing it to specific topics on an MQTT broker.
2.  **MQTT Broker (Eclipse Mosquitto):** A Docker container running Mosquitto receives the data from the publisher and forwards it to any subscribed clients.
3.  **Subscriber (`subscriber.py`):** A second Python script subscribes to the MQTT topics. It receives the data, processes it, and routes it to the appropriate database based on the topic.
4.  **Databases (Dockerized):**
    * Heart rate data is stored in **SQLite** for structured, time-series analysis.
    * Complex activity data (steps, calories) is stored in **MongoDB** as JSON-like documents.
    * Relationships between devices and the data they produce are stored in **Neo4j**, our graph database.
5.  **Web Frontend (PHP/Apache):** A Dockerized web server reads data from SQLite and MongoDB to display a live dashboard.

## 3. Technologies Used

* **Backend:** Python 3
* **Messaging:** Paho MQTT, Eclipse Mosquitto
* **Databases:** SQLite, MongoDB 5.0, Neo4j 4.4
* **Frontend:** PHP, HTML/CSS
* **Containerization:** Docker & Docker Compose

## 4. Installation and Use

[cite_start]Instructions for setting up and running the project.

**Prerequisites:**
* Docker
* Docker Compose
* Python 3

**Running the Project:**

1.  **Clone the Repository:**
    ```bash
    git clone <your-repo-url>
    cd <repository-name>
    ```
2.  **Configure Passwords:** In the `docker-compose.yml` file, set a password for Neo4j in the `NEO4J_AUTH` environment variable. Ensure the same password is set for `NEO4J_PASSWORD` in the `subscriber.py` file.

3.  **Start all services:**
    ```bash
    docker-compose up --build -d
    ```
4.  **Run the Python Scripts:** Open two separate terminals from the project's root directory.
    * In terminal 1, start the subscriber:
        ```bash
        python subscriber.py
        ```
    * In terminal 2, start the publisher:
        ```bash
        python publisher.py
        ```
5.  **View the Dashboard:** Open your web browser and navigate to:
    `http://localhost:8080`

## 5. Project Structure