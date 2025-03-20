import struct


class FiscalCommand:
    def __init__(self):
        self.nbl_counter = 0x70  # Стартова стойност за NBL (пример: 0x70)

    def calculate_len(self, cmd, data):
        """Изчислява LEN (дължина на съобщението)"""
        length = 1 + 1 + 1 + len(data)  # LEN + NBL + CMD + DATA
        return (length + 0x20) & 0xFF  # Добавяме 0x20

    def calculate_nbl(self):
        """Изчислява NBL (номер на съобщението)"""
        nbl_value = (self.nbl_counter + 0x20) & 0xFF  # Добавяме 0x20
        self.nbl_counter += 1  # Увеличаваме NBL за всяка нова команда
        return nbl_value

    def calculate_checksum(self, message):
        """Изчислява CS CS (контролна сума)"""
        crc = 0
        for byte in message:
            crc ^= byte  # XOR на всички байтове от LEN до DATA

        # Разбиване на резултата на два нибъла и добавяне на 0x30
        cs1 = ((crc >> 4) & 0x0F) + 0x30
        cs2 = (crc & 0x0F) + 0x30
        return bytes([cs1, cs2])

    def build_command(self, cmd, data):
        """Сглобява финалната команда"""
        stx = b'\x02'
        etx = b'\x0A'

        cmd_byte = bytes.fromhex(cmd)  # Преобразуваме CMD от HEX в байтове
        data_bytes = data.encode('cp1251')  # Преобразуваме DATA в байтове (Windows 1251)

        len_byte = self.calculate_len(cmd_byte, data_bytes)
        nbl_byte = self.calculate_nbl()

        message_body = bytes([len_byte, nbl_byte]) + cmd_byte + data_bytes
        checksum = self.calculate_checksum(message_body)

        final_message = stx + message_body + checksum + etx
        return final_message.hex().upper()



