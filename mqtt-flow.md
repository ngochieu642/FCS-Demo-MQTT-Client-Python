# Javascript mqtt client

## 1. Tạo mqtt client

- Kết nối vào địa chỉ: ws://192.168.1.127

```typescript
mqtt.connect(`ws://${process.env.SERVER_URL}`, {
	port: 1889,
	clientId: socket_client_id,
});
```

- Trong đó: 
	- socket_client_id: uuidv4()
- connect(): - `mqtt.connect([url], options)` - Connects to the broker specified by the given url and options and returns a Client.

- The URL can be on the following protocols: 'mqtt', 'mqtts', 'tcp', 'tls', 'ws', 'wss'. The URL can also be an object as returned by URL.parse(), in that case the two objects are merged, i.e. you can pass a single object with both the URL and the connect options.

- You can also specify a servers options with content: [{ host: 'localhost', port: 1883 }, ... ], in that case that array is iterated at every connect.

- For all MQTT-related options, see the Client constructor.

- options is the client connection options (see: the connect packet). Defaults:
	- `wsOptions`: is the WebSocket connection options. Default is {}. It's specific for WebSockets. For possible options have a look at: https://github.com/websockets/ws/blob/master/doc/ws.md.
	- `keepalive`: 60 seconds, set to 0 to disable
	- `reschedulePings`: reschedule ping messages after sending packets (default true)
	- `clientId`: 'mqttjs_' + Math.random().toString(16).substr(2, 8)
	- `protocolId`: 'MQTT'
	- `protocolVersion`: 4
	- `clean`: true, set to false to receive QoS 1 and 2 messages while offline
	- `reconnectPeriod`: 1000 milliseconds, interval between two reconnections. Disable auto reconnect by setting to 0.
	- `connectTimeout`: 30 * 1000 milliseconds, time to wait before a CONNACK is received
	- `username`: the username required by your broker, if any
	- `password`: the password required by your broker, if any
	- `incomingStore`: a Store for the incoming packets
	- `outgoingStore`: a Store for the outgoing packets
	- `queueQoSZero`: if connection is broken, queue outgoing QoS zero messages (default true)
	- `customHandleAcks`: MQTT 5 feature of custom handling puback and pubrec packets. Its callback:

## 2. On 'connect'

- tạo msg_id = uuidv4()
- tạo hello_msg

```javascript
let hello_msg = new fcsHelloMessageModel(
	msg_id,
	socket_topic_id,
	socket_client_id
);
```

- `hello_msg` sẽ có dạng như sau

```json
{
	"message_id": msg_id,
	"topic": socket_topic_id,
	"client_id": socket_client_id
}
```

- Trong đó 
	- `socket_topic_id` = `socket_client_id` = uuidv4() 
	- `msg_id` = uuidv4()

- Tạo `msg_builder`, dùng để build ra `transfer_msg` và dùng mqtt publish `transfer_msg`

```typescript
let msg_builder = new fcsMessageBuilder(socket_topic_id, false, 0, msg_id);
let transfer_msg = msg_builder.createPackage(
	fcsMessageTypes.Hello,
	fcsMessageTypes[fcsMessageTypes.Hello],
	hello_msg
);
mqttClient.publish(socket_topic_id, transfer_msg).then(() => {
	console.log("We async now");
	return mqttClient.end();
});
```

- Ta xem xét hàm `createPackage`:

```typescript
public createPackage(messageType: number, messageName: string, messageContent: any){}

```

- `fcsMessageTypes.Hello`: 1001
- `fcsMessageTypes[fcsMessageTypes.Hello]`
- `transfer_msg` có dạng như sau:

- Từ đó suy ra hàm được gọi là

```typescript
createPackage(1001, "Hello", hello_msg);
```

dẫn tới hàm sau được gọi

```typescript
fcsTransferableMessageModel(1001, "Hello", hello_msg);
```

- `transfer_msg` sẽ có dạng như sau:

```json
{
	"message_type": 1001,
	"message_name": "Hello",
	"message_content": stringify(hello_msg),
	"STX": 9001,
	"ETX": 9002
}
```

Tuy nhiên ta chú ý `transfer_msg` sẽ là buffer của object được để cập phía trên

```typescript
const safeBuffer = require("safe-buffer");
safeBuffer.Buffer.from(messageReply);
```

## 3. Tổng hợp flow `on 'connect'`

- Tin nhắn gửi đi là buffer của object như sau tới `socket_topic_id`
  ```json
  {
    "message_type": 1001,
    "message_name": "Hello",
    "message_content": stringify(hello_msg),
    "STX": 9001,
    "ETX": 9002
  }
  ```
- `hello_msg` có dạng như sau:

  ```json
  {
    "message_id": msg_id,
    "topic": socket_topic_id,
    "client_id": socket_client_id
  }
  ```

- Trong đó các string quy định như sau:
	- `socket_topic_id` = `socket_client_id` = uuidv4() 
	- `msg_id` = uuidv4()

- Vậy tin nhắn thực sự cần gửi sẽ trông như thế này

```json
{
    "message_type": 1001,
    "message_name": "Hello",
    "message_content": 
		"{
			"message_id": uuidv4_2(),
			"topic": uuidv4_1(),
			"client_id": uuidv4_1()
		}",
    "STX": 9001,
    "ETX": 9002
  }
```

- Buffer về cơ bản sẽ đổi dữ liệu từ kiểu string sang tương ứng trong ASCII. 
- Tham khảo link sau : https://ascii.cl/
- Vd: 

		'{"one":1,"two":2}' -> Buffer.from() 
		-> <Buffer 7b 22 6f 6e 65 22 3a 31 2c 22 74 77 6f 22 3a 32 7d>
		
		7b = {
		22 = "
		6f = o
		6e = n	




