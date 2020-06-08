import os
import paho.mqtt.client as mqtt

SERVER_HOST = os.environ.get('SERVER_HOST')
SERVER_PORT = os.environ.get('SERVER_PORT')

print(f'SERVER HOST: {SERVER_HOST}')


def on_connect(client, userdata, flags, rc):
    print('Connected with result code: ' + str(rc))

    client.subscribe('update.info.gateway.123')
    print('Subscribed')


def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))


def on_disconnect(client, userdata, msg):
    print(client, userdata, msg)


client = mqtt.Client(transport="websockets")
client.ws_set_options(path="/mqtt", headers=None)

client.on_connect = on_connect
client.on_message = on_message

try:
    client.connect(host=SERVER_HOST, port=int(SERVER_PORT), keepalive=60)

except Exception as e:
    print(e)


client.loop_forever()
