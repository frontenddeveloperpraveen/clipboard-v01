import pyperclip
import paho.mqtt.client as mqtt
import time
import threading
import random
connection_id = str(random.randint(11111111,99999999))
print(connection_id)
variable_copy = ''
docket_id = connection_id + '1'
new_copy = False
def on_connect(client, userdata, flags, rc):
    print("Connected - rc:", rc)
def on_message(client, userdata, message):
    print(str(message.payload.decode('utf-8')))
def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed:", str(mid), str(granted_qos))
def on_unsubscribe(client, userdata, mid):
    print("Unsubscribed:", str(mid))
def on_disconnect(client, userdata, rc):
    if rc != 0:
        print("Unexpected Disconnection")
def send_message(client, topic):
    while True:
        if new_copy == True:
            client.publish(topic, variable_copy)
            print("Recent : ",variable_copy)
def receive_messages(client, topic):
    client.subscribe(topic)
    while True:
        client.loop()
        time.sleep(0.1)
def copy_paste():
    while True:
        global variable_copy, new_copy
        copy_item = pyperclip.paste()
        if copy_item == variable_copy:
            new_copy = False
            continue
        else:
            variable_copy = copy_item
            new_copy = True
broker_address = "broker.emqx.io"
port = 1883
client = mqtt.Client()
client.on_subscribe = on_subscribe
client.on_connect = on_connect
client.on_message = on_message
client.connect(broker_address, port)
send_topic = f"/praveen/r"
receive_topic = f"/praveen/k"
send_thread = threading.Thread(target=send_message, args=(client, send_topic))
receive_thread = threading.Thread(target=receive_messages, args=(client, receive_topic))
copy_thread = threading.Thread(target=copy_paste)
send_thread.start()
copy_thread.start()
receive_thread.start()
send_thread.join()
receive_thread.join()
copy_thread.join()
client.disconnect()
client.loop_stop()
