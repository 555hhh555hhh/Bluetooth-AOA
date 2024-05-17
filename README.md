# ublox XPLR-AOA-2 explorer kits定位套件使用指南

作者：汤竑敬

联系方式：12011827@mail.sustech.edu.cn / 微信:13769875999

资料附件：https://github.com/555hhh555hhh/Bluetooth-AOA

产品官网：https://www.u-blox.com/en/product/xplr-aoa-2-kit

## 设备配置

> [!NOTE]
>
> 在开始使用之前，建议在[官网](https://www.u-blox.com/en/product/xplr-aoa-2-kit?legacy=Current#Product-description)下载最新的用户手册和DataSheet阅读，本文仅供参考

### C211 anchor 天线接收板固件刷新

1. 下载并安装ublox官方[上位机程序](https://www.u-blox.com/en/product/s-center)

2. 打开上位机s-center，选择串口号连接，检查波特率、奇偶校验、数据位、停止位等参数

   <img src="Image\image-20240517223735546.png" alt="image-20240517223735546" style="zoom:80%;" />

   <img src="Image\image-20240517223213278.png" alt="image-20240517223213278" style="zoom:75%;" />

   上电之后POWER指示灯常亮，上位机连接成功连接后CTS指示灯常亮

3. 切换天线板进入到程序下载模式

   > [!IMPORTANT]
   >
   > Hold down SW2 during board reset to enter the download mode. 

​	按住SW2，插拔数据线来使电路板重新上电，这时候就能进入下载模式，可以观察到电路板上DSR和CTS高速闪烁（一段时间后会熄灭，但出现闪烁已经标志进入了下载模式）。

4. 烧录程序

   点击Software Update按钮，选择合适的文件进行烧录，格式例如NINA-B4-nRFC-DF-SW-2.1.0-005.bin，还要注意调整波特率。

   可能会等待一段时间才出现如下所示黑框，或者出现黑框后要等待一段时间才开始有进度条变动

<img src="Image\image-20240517224331320.png" alt="image-20240517224331320" style="zoom:50%;" />

5. 烧录完成

<img src="Image\image-20240517231107248.png" alt="image-20240517231107248" style="zoom:80%;" />

​	这时电路板DS1常亮绿灯，CTS和RTS指示灯常亮，代表工作正常。上位机也从串口读到数据，代表工作正常。

> [!NOTE]
>
> 使用AT命令交互框可以和更改电路板设置，具体查看AT命令手册，输入内容后按键盘回车ENTER键发送

### C209 Tag 蓝牙标签固件刷新

我阅读用户手册的理解是c209不可以使用s-center来刷固件，但是手册里仍然给了实例，但是我没有测试成功，所以还是使用比较原始的方案来进行烧录，同4.4.2.1和4.4.2.3节的内容。

1. 下载烧录软件nrfutil

   从原作者[github链接](https://github.com/NordicSemiconductor/pc-nrfutil/releases)处下载或者从[便捷仓库](https://github.com/555hhh555hhh/Bluetooth-AOA/tree/main/nrfutil)下载

2. 下载固件包

   从原作者[github链接](https://github.com/u-blox/c209-aoa-tag/releases)处下载或者从[便捷仓库](https://github.com/555hhh555hhh/Bluetooth-AOA/tree/main/C209%E5%9B%BA%E4%BB%B6)下载

3. 让C209进入下载模式

   > [!IMPORTANT]
   >
   >  press and hold the SW2 button on the C209 tag while resetting the board (either by inserting the USB cable or pressing the RESET button) to set the bootloader in “download” mode. 

   按住SW2按键（靠近LED那个）插拔数据线重新上电来进入下载模式，是否成功进入下载模式似乎没有明显提示

4. 进行烧录

   之前下载了nrfutil软件，双击运行应该什么也不会发生，这个软件类似于安装python，需要在控制命令行cmd来使用它。

<img src="Image\image-20240517235223443.png" alt="image-20240517235223443" style="zoom:80%;" />

​	但现在还不能直接运行，因为我们只是把这个软件下载下来，系统还不知道我们下载了这个软件，所以要把它添加到系统路径

在Windows搜索框搜索“高级系统设置”并打开

<img src="Image\image-20240517235715384.png" alt="image-20240517235715384" style="zoom:50%;" />

点击环境变量->系统变量->Path->编辑

<img src="Image\image-20240518000103118.png" alt="image-20240518000103118" style="zoom:67%;" />

新建->浏览->选择包含nrfutil程序的文件夹点确定

<img src="Image\image-20240518000522961.png" alt="image-20240518000522961" style="zoom:67%;" />

现在能使用nrfutil了，但是为了输入命令简单，我们可以在包含烧录文件的文件夹里打开控制命令行，就不用输入文件位置了。

首先找到适合烧录的文件

<img src="Image\image-20240518001338051.png" alt="image-20240518001338051" style="zoom:80%;" />

<img src="Image\image-20240518001545271.png" alt="image-20240518001545271" style="zoom:80%;" />

这时候控制命令行就能够直接使用了，输入命令并运行，**注意修改串口号**

`nrfutil dfu serial -pkg NINA-B4-DF-TAG-SW-2.0.1-001.zip -p COM17 -b 115200 -fc 1`

如下图所示，第一次运行命令是正常烧录，第二次运行时没有进入下载模式导致的错误

> [!IMPORTANT]
>
> 运行命令后请耐心等待至少1分钟，反正报错会自己停止，不要手动去终止。一般来说要等待一段时间后进度条才会开始变化。

<img src="Image\image-20240518001715027.png" alt="image-20240518001715027" style="zoom:80%;" />

5. 检查是否烧录成功

   可以有多种方式检查是否烧录成功

   指示灯法：指示灯周期性闪烁

   按键法：按SW2按键，观察是否有灯闪烁

   串口通信法：打开s-center，流控制选择nano，选择串口进行连接。

   ​	可以进行简单的通信测试，请注意，C209的串口只在开机后10s内可用，如无应答可以按RESET按钮再尝试。

   ​	<img src="Image\image-20240518003102466.png" alt="image-20240518003102466" style="zoom:67%;" />

## 数据读取

固件刷新后就可以开始进行定位实验，可以使用上位机进行数据读取或者使用Python或者其他编程语言读取串口数据，进行帧解码解析数据。

### 上位机定位

将C211天线板连接到电脑，打开s-center

<img src="Image\image-20240518003852404.png" alt="image-20240518003852404" style="zoom:67%;" />

报文个字段含义如下：

|               数据报文字段含义               |      值      |
| :------------------------------------------: | :----------: |
|            Eddystone instance ID             | CCF9578E0D8A |
|           RSSI of 1st polarization           |     -42      |
|                   Angle 1                    |     -10      |
|                   Angle 2                    |      2       |
|                   Reserved                   |     -43      |
|               Detected channel               |      39      |
|      Anchor ID as set by AT+UDFCFG tag       | CCF9578E0D89 |
| User defined strings as set by AT+UDFCFG tag |      -       |
|                  Timestamp                   |    15921     |
|     Periodic advertising sequence number     |      25      |

即第三字段代表水平角度，第四字段代表垂直角度

### [Python](https://github.com/555hhh555hhh/Bluetooth-AOA/blob/main/codes/serialTest.py)数据读取

使用Python进行数据读取，在设置串口时需要增加一些设置，特别是开启RTSCTS

<img src="Image\image-20240518005605295.png" alt="image-20240518005605295" style="zoom:80%;" />

在死循环中读取串口数据

<img src="Image\image-20240518005655206.png" alt="image-20240518005655206" style="zoom:80%;" />

![image-20240518005740131](Image\image-20240518005740131.png)

进行数据筛选，只保留两个角度的信息

<img src="Image\image-20240518005831578.png" alt="image-20240518005831578" style="zoom:80%;" />

![image-20240518005857061](Image\image-20240518005857061.png)

```python
import serial

# 配置串口参数
ser1 = serial.Serial(
    port='COM13',
    baudrate=115200,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    rtscts=True
)

try:
    while True:
        # 读取串口数据
        data1 = ser1.readline().decode('utf-8').strip()
        # print(data1)
        
        # 解析并筛选数据
        if data1.startswith("+UUDF:"):
            parts1 = data1.split(',')
            if len(parts1) == 10:
                # 提取第三、第四数据段
                angle1 = [int(parts1[2]),int(parts1[3])]

                # 打印数据
                print(angle1[0],angle1[1])

except serial.SerialException as e:
    print("打开串口失败：", e)

finally:
    # 关闭串口
    ser1.close()
    print("串口已关闭")
```



## 三角定位算法

### 理论计算



<img src="Image\image-20240518010741124.png" alt="image-20240518010741124" style="zoom:50%;" />

假设在二维空间中，有两个基站分别位于A\(x1, y1\)、B\(x2, y2\)，而待定位的移动基站N(x, y)。如果基站A和B测量到的信号到达角度分别为θ1、θ2

由直线斜率关系可得如下方程：![image-20240518011150793](Image\image-20240518011150793.png)

将上式变形，构造线性方程组得：![image-20240518011205581](Image\image-20240518011205581.png)

求解方程组，即可得出移动基站𝑁的位置坐标：![image-20240518011226178](Image\image-20240518011226178.png)

### [Python](https://github.com/555hhh555hhh/Bluetooth-AOA/blob/main/codes/Triangulation.py)实现

注意首先要初始化基站位置，且要注意创建的两个串口ser1、ser2和station1、station2的对应关系

```python
import math
import serial
import matplotlib.pyplot as plt

# 创建串口对象
ser1 = serial.Serial(
    port='COM7',
    baudrate=115200,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    rtscts=True
)

ser2 = serial.Serial(
    port='COM4',
    baudrate=115200,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    parity=serial.PARITY_NONE,
    rtscts=True
)

# 基站位置
station1 = (100, 0)
station2 = (300, 0)

# 初始化图形
plt.figure()
plt.axis([0, 400, 0, 400])  # 调整横纵坐标范围
plt.plot(station1[0], station1[1], 'ro', label='Station 1')
plt.plot(station2[0], station2[1], 'bo', label='Station 2')
plt.legend()

# 存储交点的坐标
intersections = []
angles = []

def update_position(angle1, angle2):
    global intersections  # 使用全局变量
    # 计算目标点位置
    # 根据角度和基站位置计算目标点坐标
    theta1 = (90 - angle1) * math.pi / 180
    theta2 = (90 - angle2) * math.pi / 180

    # 计算交点坐标
    x1, y1 = station1
    x2, y2 = station2
    
    # 计算三角函数
    tan_theta1 = math.tan(theta1)
    tan_theta2 = math.tan(theta2)
    cot_theta1 = 1 / math.tan(theta1)
    cot_theta2 = 1 / math.tan(theta2)
    
    # 计算交点的坐标
    x = ((y2 - x2 * tan_theta2) - (y1 - x1 * tan_theta1)) / (tan_theta1 - tan_theta2)
    y = ((x2 - y2 * cot_theta2) - (x1 - y1 * cot_theta1)) / (cot_theta1 - cot_theta2)
    
    # 将交点添加到列表中
    intersections.append((x, y))

    # 更新标签
    print(f"目标点坐标：({x:.2f}, {y:.2f})")
    
    return x, y

try:
    while True:
        # 读取串口数据
        data1 = ser1.readline().decode('utf-8').strip()
        data2 = ser2.readline().decode('utf-8').strip()

        # 解析并筛选数据
        if data1.startswith("+UUDF:") and data2.startswith("+UUDF:"):
            parts1 = data1.split(',')
            parts2 = data2.split(',')
            if len(parts1) == 10 and len(parts2) == 10:
                # 提取第三、第四数据段
                angle1 = int(parts1[2])
                angle2 = int(parts2[2])
                # 打印数据
                print("Ser1:", angle1)
                print("Ser2:", angle2)
                angles.append((angle1, angle2))

                # 可视化
                plt.clf()  # 清除之前的绘图
                plt.axis([0, 400, 0, 400])  # 调整横纵坐标范围
                plt.plot(station1[0], station1[1], 'ro', label='Station 1')
                plt.plot(station2[0], station2[1], 'bo', label='Station 2')
                x, y = update_position(angle1, angle2)
                
                # 绘制所有交点
                for point in intersections[-80:]: #绘制近80个点
                    plt.plot(point[0], point[1], 'go')
                    
                # 只绘制当前位置
                # plt.plot(x, y, 'go')
                    
                plt.pause(0.001)  # 延迟一段时间，以允许图形更新

except serial.SerialException as e:
    print("打开串口失败：", e)

finally:
    # 关闭串口
    ser1.close()
    ser2.close()
    print("串口已关闭")
```

