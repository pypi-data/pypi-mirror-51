# päckel

Network protocol library. Handles packet serialization/deserialization in a Pythonic way.

### Usage

* Define a basic protocol :

```python
import packel

class Ping(packel.Packet):
    text = packel.String()

class Pong(packel.Packet):
    is_hello = packel.Boolean()

protocol = packel.Protocol([Ping, Pong])
```

* Use it to serialize and deserialize data :

```python
request = Ping(text='hello')
serialized_bytes = protocol.serialize(request)

# ...

packet = protocol.deserialize(serialized_bytes)
if isinstance(packet, Ping):
    is_hello = packet.text == 'hello'
    response = Pong(is_hello=is_hello)
    # ...
```
