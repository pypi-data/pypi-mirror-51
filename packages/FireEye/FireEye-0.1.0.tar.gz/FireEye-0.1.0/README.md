# FireEye

## Installation

Node.js installation:
```
npm install fireeye
```

Python installation:
```
pip install FireEye
```

These libraries are developed in parallel, and designed to be used together.

## Features

FireEye enables real-time bidirectional communication between a Node.js server, and a Python process. It is specifically designed to stream video between these two processes when running on separate devices. 

Its main features are:

### Speed

Connections are made using TCP sockets and can pass information from processes extremely quickly and reliably.

### Easy to use

This library was designed to lower the barrier to entry as much as possible. As such, it has a built in wrapper to send images from process to process.

## How to use — Node.js

The following example imports and creates the data socket in Node.js, and then sets up a listener event.
```javascript
const FireEye = require('fireeye');

var socket = new FireEye();

socket.on('image', (data) => {
	/* your code here */
})

```

## How to use — Python

The following is a simple example of how to use NodeSocket in Python:
```python
from FireEye import FireEye
import cv2
import base64

socket = FireEye()

cap = cv2.VideoCapture(0) #Camera Number Here

cap.set(3, 640)
cap.set(4, 480)

def encode_img(img):
	success, encoded_img = cv2.imencode('.jpg', img)
	return base64.b64encode(encoded_img)

ret, frame = cap.read()

socket.writeImg(encode_img(frame))
```