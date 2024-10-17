# image_transport
用于2024.10 Reborn 队内赛
## 功能包
**image_pub.py**用于发布图像信息
**image_sub.py**用于接收图像信息
## 使用指南
所需调用的包在**requirements.txt**列出
先在相应的工作区启动相机节点
```bash
# 编译节点包
colcon build
source install/setup.bash
ros2 launch mindvision_camera mv_launch.py 
#替换为实际存在的节点
```
在另一个终端启动发布端**image_pub.py** `python3 image_pub.py`

实际使用时，将 **/image_raw** 替换为相应的话题名称
```python
self.subscription = self.create_subscription(
            Image,
            '/image_raw',
            self.image_callback,
            5)  
```
打开新终端，启动订阅端**image_sub.py** `python3 image_sub.py`

实际使用时，将 **192.168.31.248** 替换为相应的IP地址
```python
client_socket.connect(('192.168.31.248', 8888))
```
## 电控端示例
在同一局域网中，先使用SSH连接远程电脑
`ssh reborn@192.168.31.248`
在远程终端中启动相机节点和发布节点
```bash
colcon build
source install/setup.bash
ros2 launch mindvision_camera mv_launch.py 
```
```bash
cd image_transport/src/publish
python3 image_pub.py
```
最后在本地终端启动接收节点
```bash
python3 image_sub.py
```
