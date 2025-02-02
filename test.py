import serial

ser = serial.Serial(port='COM14', baudrate=115200, timeout=1)

command = bytes([0x2B])  # 2Bh = Подаване на хартия
ser.write(command)  # Изпращане на командата
response = ser.read(10)  # Четене на отговор (ако има)
print(response)

ser.close()