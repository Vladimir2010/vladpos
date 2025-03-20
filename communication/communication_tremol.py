import serial
import socket
import re  # За почистване на излишни кодове
import time
from commands_generator_tremol import FiscalCommand


class FiscalPrinter:
    def __init__(self, connection_type="serial", port="COM4", baudrate=115200, host="192.168.1.100", tcp_port=5555):
        """Инициализира принтера с избрания метод на комуникация."""
        self.connection_type = connection_type
        self.port = port
        self.baudrate = baudrate
        self.host = host
        self.tcp_port = tcp_port
        self.conn = None

    def connect(self):
        """Свързва се с касовия апарат."""
        if self.connection_type == "serial":
            try:
                self.conn = serial.Serial(self.port, self.baudrate, timeout=1)
                print(f"[+] Свързан към {self.port} на {self.baudrate} baud.")
            except Exception as e:
                print(f"[!] Грешка при свързване със сериен порт: {e}")
        elif self.connection_type == "tcp":
            try:
                self.conn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.conn.connect((self.host, self.tcp_port))
                print(f"[+] Свързан към {self.host}:{self.tcp_port} по TCP/IP.")
            except Exception as e:
                print(f"[!] Грешка при TCP свързване: {e}")
        else:
            print("[!] Невалиден метод на комуникация.")

    def disconnect(self):
        """Затваря връзката с принтера."""
        if self.conn:
            self.conn.close()
            print("[+] Връзката е затворена.")

    def calculate_crc(self, data):
        """Изчислява XOR базирана контролна сума (CRC) за командата."""
        crc = 0
        for byte in data:
            crc ^= byte
        return crc.to_bytes(1, 'big')

    def hex_to_readable(self, hex_string):
        """Конвертира HEX данни в четим ASCII текст."""
        try:
            decoded = bytes.fromhex(hex_string).decode("utf-8", errors="ignore")
            return decoded.strip()
        except Exception as e:
            return f"Грешка при декодиране: {e}"

    def clean_response(self, response_text):
        """
        Почиства отговора, като премахва ненужни кодове като "38h"
        и оставя само полезната информация (например дата и час).
        """
        # Премахваме "38h" или друг код от вида "XXh" в началото на отговора
        cleaned_text = re.sub(r'^\d{2,}h', 't', response_text).strip()

        # Ако има "=" в края (индикатор за край на отговора), махаме го
        cleaned_text = cleaned_text.rstrip('=')

        return cleaned_text

    def send_command(self, command):
        """Изпраща команда към касовия апарат и обработва отговора."""
        if not self.conn:
            print("[!] Връзката не е установена.")
            return None

        # Форматираме командата със StartByte (0x02) и EndByte (0x03)
        # final_command = b'\x02' + command + self.calculate_crc(command) + b'\x03'
        final_command = bytes.fromhex(command)

        try:
            self.conn.write(final_command) if self.connection_type == "serial" else self.conn.send(final_command)
            print(f"[>] Изпратена команда: {final_command.hex()}")

            # Четене на отговор
            response = self.conn.read(64) if self.connection_type == "serial" else self.conn.recv(1024)
            response_hex = response.hex()

            # Декодиране на отговора
            readable_response = self.hex_to_readable(response_hex)
            cleaned_response = self.clean_response(readable_response)  # Почистване на излишното

            print(f"[<] Получен отговор (HEX): {response_hex}")
            print(f"[<] Декодиран отговор: {cleaned_response}")

            return cleaned_response
        except Exception as e:
            print(f"[!] Грешка при изпращане: {e}")
            return None


# ==========================
# === Автоматично изпращане на зададените команди ===
# ==========================
if __name__ == "__main__":
    printer = FiscalPrinter(connection_type="serial", port="COM4")  # Или "/dev/ttyUSB0" за Linux
    # printer = FiscalPrinter(connection_type="tcp", host="192.168.1.100", tcp_port=5555)

    # Пример за използване
    fiscal = FiscalCommand()
    commands = []

    commands_for_sale = [

    ]

    # Вход от потребителя
    num_of_comands = int(input("Брой команди: "))
    for i in range(num_of_comands):
        cmd = input()
        data = input()
        command = fiscal.build_command(cmd, data)
        commands.append(command)
        print("Генерирана команда:", command)


    printer.connect()

    # Изпращане на командите една по една
    for cmd in commands:
        time.sleep(0)
        printer.send_command(cmd)

    printer.disconnect()



