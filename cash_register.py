import serial

class CashRegister:
    def __init__(self):
        self.connection = None

    def connect(self, port, baudrate):
        try:
            self.connection = serial.Serial(port, baudrate=baudrate, timeout=1)
            return True
        except serial.SerialException as e:
            print(f"Грешка при свързване: {e}")
            return False

    def print_receipt(self, receipt_data):
        if self.connection:
            try:
                self.connection.write(receipt_data.encode())
                return True
            except Exception as e:
                print(f"Грешка при отпечатване: {e}")
                return False
        return False

# ser=serial.Serial(port="COM14", baudrate="115200", timeout=1)
# data = bytes([0x2B])
# ser.write(data)
# while True:
#     bs = ser.read().decode()
#     print(bs)