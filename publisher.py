import paho.mqtt.client as mqtt
import time
import json
import random

# --- Configuration ---
MQTT_BROKER_HOST = "localhost"
MQTT_BROKER_PORT = 1883
# Define a list of devices to simulate
DEVICE_IDS = ["wearable1", "wearable2", "wearable3"]

# --- Main Publishing Logic ---
def on_connect(client, userdata, flags, reason_code, properties):
    """Callback function for when the client connects to the broker."""
    if reason_code.is_failure:
        print(f"Failed to connect, return code {reason_code}")
    else:
        print("Connected successfully to MQTT Broker!")

def connect_mqtt():
    """Connects to the MQTT broker."""
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2, client_id="multi_device_publisher")
    client.on_connect = on_connect
    client.connect(MQTT_BROKER_HOST, MQTT_BROKER_PORT)
    return client

def publish_data(client):
    """Generates and publishes simulated health data for multiple devices."""
    while True:
        try:
            # Loop through each device ID
            for device_id in DEVICE_IDS:
                # Define topics dynamically for the current device
                topic_heart_rate = f"sensors/{device_id}/heartrate"
                topic_activity = f"sensors/{device_id}/activity"

                # 1. Simulate Heart Rate Data
                heart_rate = random.randint(55, 125) # Give each device slightly different ranges
                heart_rate_payload = json.dumps({
                    "timestamp": time.time(),
                    "device_id": device_id,
                    "heart_rate": heart_rate
                })
                result = client.publish(topic_heart_rate, heart_rate_payload)
                if result.rc == 0:
                    print(f"Sent to topic `{topic_heart_rate}`: {heart_rate_payload}")

                # 2. Simulate Physical Activity Data
                steps = random.randint(0, 100)
                calories = steps * 0.04
                activity_payload = json.dumps({
                    "timestamp": time.time(),
                    "device_id": device_id,
                    "activity_type": "walking",
                    "metrics": {
                        "steps_taken": steps,
                        "calories_burned": round(calories, 2)
                    }
                })
                result = client.publish(topic_activity, activity_payload)
                if result.rc == 0:
                    print(f"Sent to topic `{topic_activity}`: {activity_payload}")

            # Wait for 5 seconds before the next burst of data from all devices
            print("--- All devices published. Waiting 5 seconds. ---")
            time.sleep(5)

        except KeyboardInterrupt:
            print("\nPublisher stopped.")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            break

if __name__ == '__main__':
    mqtt_client = connect_mqtt()
    mqtt_client.loop_start()
    publish_data(mqtt_client)
    mqtt_client.loop_stop()