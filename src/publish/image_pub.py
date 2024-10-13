import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2
import socket
import struct
import numpy as np

class ImageServer(Node):
    def __init__(self):
        super().__init__('image_server')
        self.br = CvBridge()

        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, 8192)
        self.server_socket.bind(('0.0.0.0', 8888)) 
        self.server_socket.listen(5)
        self.get_logger().info("等待客户端连接...")

        self.client_socket, self.addr = self.server_socket.accept()
        self.get_logger().info(f"连接来自: {self.addr}")

        self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            10)
        self.subscription  

        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 30] 

    def image_callback(self, msg):
        try:
            frame = self.br.imgmsg_to_cv2(msg, "bgr8")

            result, encoded_frame = cv2.imencode('.jpg', frame, self.encode_param)
            if not result:
                self.get_logger().warn("图像编码失败")
                return

            data = encoded_frame.tobytes()
            message_size = struct.pack("I", len(data))  

            self.client_socket.sendall(message_size + data)
            self.get_logger().debug(f"发送图像数据大小: {len(data)} bytes")

        except Exception as e:
            self.get_logger().error(f"发送图像数据时出错: {e}")
            self.client_socket.close()
            self.server_socket.close()
            rclpy.shutdown()

    def destroy_node(self):
        if self.client_socket:
            self.client_socket.close()
        if self.server_socket:
            self.server_socket.close()
        super().destroy_node()

def main(args=None):
    rclpy.init(args=args)
    image_server = ImageServer()
    try:
        rclpy.spin(image_server)
    except KeyboardInterrupt:
        image_server.get_logger().info("程序中断，关闭连接...")
    finally:
        image_server.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()
