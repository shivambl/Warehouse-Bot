import paho.mqtt.publish as publish
import paho.mqtt.client as mqtt
import config
import uuid

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe(config.MQTT_CHANNEL_PUT + uid)
    return

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    return

client = mqtt.Client()
uid = uuid.uuid1().hex
print("Our UID is: ", uid)

def start_server():
    client.on_connect = on_connect
    client.on_message = on_message
    client.connect(config.MQTT_SERVER, 1883, 60)

    client.loop_start()
    return

def stop_server():
    client.loop_stop()
    return

def send_message(msg, uid):
    channel = config.MQTT_CHANNEL_GET + uid
    print("Sending message: {} to channel {}".format(msg, channel))
    publish.single(channel, msg, hostname=config.MQTT_SERVER)
    return

def menu():
    main_menu = ['q to quit',
                'p to publish']

    start_server()
    while True:
        print("\tMQTT RPI TEST MENU")
        for option in main_menu:
            print(option)

        choice = input()
        if choice is 'q':
            print("Stopping the listener...")
            stop_server()
            return
        elif choice is 'p':
            msg = input("Enter message:\n")
            send_message(msg, uid)
    return

if __name__ == "__main__":
    menu()