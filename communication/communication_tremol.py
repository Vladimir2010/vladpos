import serial
import socket
import re  # За почистване на излишни кодове
import time



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
        final_command = b'\x02' + command + self.calculate_crc(command) + b'\x03'

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
# if __name__ == "__main__":
#     printer = FiscalPrinter(connection_type="serial", port="COM4")  # Или "/dev/ttyUSB0" за Linux
#     # printer = FiscalPrinter(connection_type="tcp", host="192.168.1.100", tcp_port=5555)
#
#     printer.connect()
#
#     # Командите, които трябва да бъдат изпратени - X
#     commands_x = [
#         b'\x09',
#         b'\x09',
#         b'\x02\x23\x26\x61\x36\x34\x0a',
#         b'\x09',
#         b'\x02\x23\x27\x21\x32\x35\x0a',
#         b'\x09',
#         b'\x02\x23\x28\x60\x36\x3b\x0a',
#         b'\x09',
#         b'\x02\x24\x29\x7c\x58\x32\x39\x0a'
#     ]
#     # Z otchet
#     commands_z = [
#         b'\x09',
#         b'\x09',
#         b'\x02\x23\x2a\x60\x36\x39\x0a',
#         b'\x09',
#         b'\x02\x23\x2b\x61\x36\x39\x0a',
#         b'\x09',
#         b'\x02\x23\x2c\x21\x32\x3e\x0a',
#         b'\x09',
#         b'\x02\x23\x2d\x60\x36\x3e\x0a',
#         b'\x09',
#         b'\x02\x24\x2e\x7c\x5a\x32\x3c\x0a'
#         b'\x09',
#     ]
#
#     # commands = [
#     #     b'\x09',
#     #     # b'\x02\x23\x89\x20\x38\x3a\x0a',
#     #     # b'\x09',
#     #     # b'\x02\x23\x8a\x68\x3c\x31\x0a',
#     #     # b'\x09',
#     #     b'\x02\x31\x8b\x30\x31\x3b\x30\x20\x20\x20\x20\x20\x3b\x30\x3b\x30\x3b\x30\x39\x3b\x0a',
#     #     # b'\x02\x2b\x8c\x32\x2b\x30\x30\x30\x30\x31\x2a\x31\x39\x34\x0a',#markira
#     #     # b'\x02\x2b\x8c\x32\x2b\x30\x30\x30\x30\x32\x2a\x37\x39\x34\x0a' #- resto
#     #     b'\x02\x2b\x2e\x32\x2b\x30\x30\x30\x30\x32\x2a\x31\x33\x35\x0a' #- #art 2
#     #     # b'\x02\x26\x8d\x33\x30\x3b\x31\x3a\x32\x0a', #ST
#     #     b'\x02\x2b\x8e\x35\x30\x3b\x30\x3b\x32\x30\x3b\x30\x39\x39\x0a',
#     #     # b'\x09',
#     #     # b'\x02\x26\x8f\x33\x30\x3b\x31\x3a\x20\x0a',
#     #     # b'\x09',
#     #     b'\x02\x23\x90\x38\x38\x3b\x0a'
#     #
#     # ]
#
#     # commands = [
#     #     b'\x09',
#     #     b'\x02 \x23 \x2a \x60 \x36 \x39 \x0a',
#     #     b'\x09',
#     #     b'\x02 \x23 \x2b \x61 \x36 \x39 \x0a',
#     #     b'\x09',
#     #     b'\x02 \x23 \x2c \x21 \x32 \x3e \x0a',
#     #     b'\x09',
#     #     b'\x02 \x23 \x2d \x60 \x36 \x3e \x0a',
#     #     b'\x09',
#     #     b'\x02 \x24 \x2e \x7c \x5a \x32 \x3c \x0a',
#     # ]
#
#
#     # Изпращане на командите една по една
#     for cmd in commands:
#         time.sleep(0)
#         printer.send_command(cmd)
#
#     printer.disconnect()
