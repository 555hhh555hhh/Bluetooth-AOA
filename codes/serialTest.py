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
        print(data1)
        
        # 解析并筛选数据
        if data1.startswith("+UUDF:"):
            parts1 = data1.split(',')
            if len(parts1) == 10:
                # 提取第三、第四数据段
                angle1 = [int(parts1[2]),int(parts1[3])]

                # 打印数据
                # print(angle1[0],angle1[1])

except serial.SerialException as e:
    print("打开串口失败：", e)

finally:
    # 关闭串口
    ser1.close()
    print("串口已关闭")
