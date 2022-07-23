# ESPTOOL-GUI
快捷将MicroPython固件烧录到esp32，esp8266等单片机


![image](https://user-images.githubusercontent.com/58870893/180613201-436a6cf0-6a6d-4349-9132-56fa20d0b4d8.png)
# 特性
1. 使用官方esptool工具封装，使用稳定
2. 打包好的exe程序内置esptool，无须任何配置即可烧录固件
3. 记住上次下载的固件，连接的端口号及芯片型号，使用方便
# 使用方法
在图形界面中直接选择固件，选择使用的端口及芯片型号进行烧录即可
# 常见问题
1. 卡在connecting
    - 芯片需要手动进入下载模式(按住boot，按下rst一次)
2. 芯片烧录后无限重启
    - 选择正确的固件及芯片型号
3. 在哪里下载micropython固件
    - 在[这里](https://micropython.org/download/?port=esp32)
4. 可以用来下载自制的其它.bin固件吗
    - 可以
