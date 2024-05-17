# 三角定位算法

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
    
    # 将数据写入文件
    with open("AOA_pos11.txt", "w") as file:
        print("数据已保存")
        for i in range(len(intersections)):
            # 四舍五入保留两位小数
            x_rounded = round(intersections[i][0], 2)
            y_rounded = round(intersections[i][1], 2)
            file.write(f"Angle1: {angles[i][0]}, Angle2: {angles[i][1]}, x: {x_rounded}, y: {y_rounded}\n")
