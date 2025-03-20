import serial
import time

# Настройки за серийна връзка
ser = serial.Serial(
    port="COM4",  # Промени порта според твоето устройство (на Windows: COM3, на Linux: /dev/ttyUSB0)
    baudrate=115200,  # Скоростта може да бъде 9600, 19200, 115200 (провери в документацията на касовия апарат)
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

def send_command(command):
    """Изпраща команда към касовия апарат"""
    command_bytes = command.encode("ascii") + b"\r\n"
    ser.write(command_bytes)
    time.sleep(0.1)  # Малка пауза за обработка
    response = ser.read(ser.in_waiting)  # Чете отговора
    return response.decode("ascii")

# Тестова команда за проверка на статус
response = send_command("20h")  # '20h' е команда за статус според протокола
print("Отговор от касовия апарат:", response)

ser.close()

send_command("30h")  # Команда за отваряне на фискален бон
send_command('31h "Кафе" 2.50')
send_command("35h 0")  # Плащане в брой
send_command("38h")  # Команда за затваряне на бона
