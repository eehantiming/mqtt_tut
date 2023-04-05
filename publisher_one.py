""" mqtt Publisher that connects to a broker and publishes to a topic."""

import time
import sys
import paho.mqtt.client as mqtt


def main():
    """Main function thats runs when called as a script."""
    mqtt_broker_hostname = "mqtt.eclipseprojects.io"
    client = mqtt.Client("publisher_one")
    # Start processing message buffers in another thread
    client.loop_start()
    connect_client(client, mqtt_broker_hostname)
    publish_topic(client, "MY/TOPIC")


def connect_client(client, broker_name):
    """Connects the client to the broker. Exits the program if connection fails."""

    def callback_connect(client, userdata, flags, return_code):
        if return_code == 0:
            print("Connected!")
            client.connected_flag = True
        else:
            client.fail_connection_flag = True
            print(f"Connection failed, error code {return_code}")

    client.fail_connection_flag = False
    client.connected_flag = False
    client.on_connect = callback_connect
    try:
        print(f"Connecting to: {broker_name}")
        client.connect(broker_name, keepalive=20)
    except Exception as err:
        print(f"Bad Connection: '{err}'. Check your hostname/ port")
        client.fail_connection_flag = True

    # Block main thread until connected. Exits if connection fails.
    while not client.connected_flag:
        print("waiting for connection")
        time.sleep(1)

    if client.fail_connection_flag:
        client.loop_stop()
        sys.exit(1)


def publish_topic(client, topic_name):
    """Blocking function that publishes periodically to the topic."""
    while True:
        result, message_id = client.publish(topic=topic_name, payload=5)
        if result == mqtt.MQTT_ERR_SUCCESS:
            print(f"Sent message to topic {topic_name}!")
        time.sleep(1)


if __name__ == "__main__":
    main()
