import serial
from log import LogManager

class Serial:
    def __init__(self, serial_port='COM3', baud_rate=9600):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.ser = None
        self.log = LogManager()

    def SerialStart(self):
        try:
            self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
            self.log.write(f"[SERIAL] Conectado à porta {self.serial_port} em {self.baud_rate} bps.")
        except Exception as e:
            self.log.write(f"[SERIAL ERRO] {e}")

    def SerialClose(self):
        if self.ser:
            self.ser.close()
            self.log.write("[SERIAL] Porta serial fechada.")
