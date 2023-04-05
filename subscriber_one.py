""" mqtt Subscriber that connects to a broker, subscribes to a topic and prints out the message."""

import time
import paho.mqtt.client as mqtt
from publisher_one import connect_client


def main():
    """Main function thats runs when called as a script."""
    mqtt_broker_hostname = "mqtt.eclipseprojects.io"
    client = mqtt.Client("subscriber_one")
    # Start processing message buffers in another thread
    client.loop_start()
    connect_client(client, mqtt_broker_hostname)
    subscribe_topic(client, "MY/TOPIC")

    # While loop to block the main thread. Put the rest of your code here.
    while True:
        # print("blocking.")
        time.sleep(1)


def subscribe_topic(client, topic_name):
    """Subscribes the client to the topic. Prints out the message received and its type."""

    def callback_topic(client, userdata, message):
        message = message.payload.decode("utf-8")
        print(f"Received {message} of type {type(message)}")

    client.on_message = callback_topic
    client.subscribe(topic_name)


if __name__ == "__main__":
    main()
