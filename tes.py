import serial
import time


class FiscalPrinter:
    def __init__(self, port='COM14', baudrate=115200, timeout=1):
        """
        Инициализиране на връзката със серийния порт.
        :param port: COM порт (пример: 'COM3' за Windows, '/dev/ttyUSB0' за Linux)
        :param baudrate: Скорост на комуникация
        :param timeout: Време за изчакване на отговор (в секунди)
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial = None

    def open(self):
        """Отваря сериен порт"""
        try:
            self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
            print(f"Свързан с {self.port} на {self.baudrate} baud")
        except serial.SerialException as e:
            print(f"Грешка при свързване: {e}")

    def close(self):
        """Затваря серийния порт"""
        if self.serial and self.serial.is_open:
            self.serial.close()
            print("Сериен порт затворен")

    def send_command(self, command_hex, data=b''):
        """
        Изпраща команда към касовия апарат.
        :param command_hex: Код на командата в hex (напр. 0x2B за подаване на хартия)
        :param data: Допълнителни данни (ако има)
        """
        if not self.serial or not self.serial.is_open:
            print("Грешка: Серийният порт не е отворен!")
            return None

        command = bytes([command_hex]) + data
        self.serial.write(command)
        time.sleep(0.1)  # Кратка пауза за обработка

        response = self.serial.read(10)  # Четем до 10 байта отговора
        print(f"Изпратена команда: {command.hex().upper()}")
        print(f"Отговор: {response.hex().upper()}")
        return response

    def feed_paper(self):
        """Команда за подаване на хартия (2Bh)"""
        return self.send_command(0x2B)

    def open_cash_drawer(self):
        """Команда за отваряне на чекмеджето (2Ah)"""
        return self.send_command(0x2A)

    def read_status(self):
        """Команда за четене на статус (20h)"""
        return self.send_command(0x20)


if __name__ == "__main__":
    fp = FiscalPrinter(port='COM14')  # Промени порта според твоята система
    fp.open()

    # Тестови команди
    fp.read_status()
    fp.feed_paper()
    fp.open_cash_drawer()

    fp.close()
