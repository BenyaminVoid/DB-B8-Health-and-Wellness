import paho.mqtt.client as mqtt
import json
import sqlite3
from pymongo import MongoClient
from neo4j import GraphDatabase

# --- Configuration ---
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
# This topic uses a wildcard (+) to listen for ALL devices
MQTT_TOPIC = "sensors/+/+" 

# --- Database Connection Details ---
SQLITE_DB_FILE = "health_data.db"
MONGO_CLIENT_URL = "mongodb://localhost:27018/" # Using the specific Docker port
MONGO_DB_NAME = "health_wellness_db"
MONGO_COLLECTION_NAME = "activity_logs"
NEO4J_URI = "neo4j://localhost:7687"
NEO4J_USER = "neo4j"
NEO4J_PASSWORD = "my-secret-password" # The password you set in docker-compose

# --- Database Setup and Connection ---
def setup_sql_database():
    conn = sqlite3.connect(SQLITE_DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS heart_rate_readings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp REAL NOT NULL,
            device_id TEXT NOT NULL,
            heart_rate INTEGER NOT NULL
        );
    """)
    conn.commit()
    return conn

def connect_mongo():
    client = MongoClient(MONGO_CLIENT_URL)
    db = client[MONGO_DB_NAME]
    return db[MONGO_COLLECTION_NAME]

def connect_neo4j():
    driver = GraphDatabase.driver(NEO4J_URI, auth=(NEO4J_USER, NEO4J_PASSWORD))
    # Test connection on startup
    driver.verify_connectivity()
    return driver

# Initialize connections
sql_conn = setup_sql_database()
mongo_collection = connect_mongo()
neo4j_driver = connect_neo4j()

# --- MQTT Message Handling ---
def on_connect(client, userdata, flags, reason_code, properties):
    """Callback for when the client connects."""
    if reason_code.is_failure:
        print(f"Failed to connect: {reason_code}. loop_forever() will retry connection")
    else:
        print("Connected successfully to MQTT Broker!")
        client.subscribe(MQTT_TOPIC)
        print(f"Subscribed to topic: {MQTT_TOPIC}")

def on_message(client, userdata, msg):
    """The core callback function that processes incoming MQTT messages."""
    topic = msg.topic
    payload = msg.payload.decode()
    print(f"Received message on topic `{topic}`: {payload}")
    try:
        data = json.loads(payload)
        # Routing logic based on topic content
        if "heartrate" in topic:
            store_in_sql(data)
            store_in_neo4j(data) # Store relationship in Neo4j
        elif "activity" in topic:
            store_in_mongodb(data)
    except Exception as e:
        print(f"An error occurred while processing message: {e}")

# --- Data Storage Functions ---
def store_in_sql(data):
    try:
        cursor = sql_conn.cursor()
        cursor.execute( "INSERT INTO heart_rate_readings (timestamp, device_id, heart_rate) VALUES (?, ?, ?)", (data['timestamp'], data['device_id'], data['heart_rate']))
        sql_conn.commit()
        print(f"  -> Stored in SQL: {data['heart_rate']} bpm")
    except sqlite3.Error as e:
        print(f"SQL Error: {e}")

def store_in_mongodb(data):
    try:
        result = mongo_collection.insert_one(data)
        print(f"  -> Stored in MongoDB with ID: {result.inserted_id}")
    except Exception as e:
        print(f"MongoDB Error: {e}")

def store_in_neo4j(data):
    """Creates a Device node, a Reading node, and links them."""
    try:
        with neo4j_driver.session(database="neo4j") as session:
            # Using MERGE ensures we don't create duplicate device nodes
            session.run("""
                MERGE (d:Device {deviceId: $device_id})
                CREATE (r:Reading {
                    heart_rate: $heart_rate,
                    timestamp: $timestamp
                })
                CREATE (d)-[:PRODUCED]->(r)
                """,
                device_id=data['device_id'],
                heart_rate=data['heart_rate'],
                timestamp=data['timestamp']
            )
            print(f"  -> Created Neo4j relationship for heart rate: {data['heart_rate']}")
    except Exception as e:
        print(f"Neo4j Error: {e}")

# --- Main Subscriber Logic ---
if __name__ == '__main__':
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="db_subscriber")
    client.on_connect = on_connect
    client.on_message = on_message
    try:
        print("Attempting to connect to MQTT broker...")
        client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT, 60)
        client.loop_forever()
    except KeyboardInterrupt:
        print("\nSubscriber stopped.")
    except Exception as e:
        print(f"Could not connect to MQTT Broker at {MQTT_BROKER_HOST}:{MQTT_BROKER_PORT}. Please ensure it is running. Error: {e}")
    finally:
        sql_conn.close()
        neo4j_driver.close()