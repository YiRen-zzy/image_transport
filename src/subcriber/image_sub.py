import cv2
import socket
import struct
import numpy as np

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
client_socket.connect(('192.168.1.3', 8888))

data = b""
payload_size = struct.calcsize("I")  

while True:
    while len(data) < payload_size:
        data += client_socket.recv(8192)

    packed_msg_size = data[:payload_size]
    data = data[payload_size:]
    msg_size = struct.unpack("I", packed_msg_size)[0]  

    while len(data) < msg_size:
        data += client_socket.recv(8192)

    frame_data = data[:msg_size]
    data = data[msg_size:]

    frame = np.frombuffer(frame_data, dtype=np.uint8)  
    frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

    cv2.imshow("Video Stream", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

client_socket.close()
cv2.destroyAllWindows()
