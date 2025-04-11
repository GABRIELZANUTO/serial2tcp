import serial
import socket
import threading
from log import LogManager

class SerialBridge:
    def __init__(self, serial_port='COM3', baud_rate=9600, tcp_ip='127.0.0.1', tcp_port=5978):
        self.serial_port = serial_port
        self.baud_rate = baud_rate
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port

        self.ser = None
        self.sock = None
        self.running = False
        self.log = LogManager()

    def serialConnect(self):
        self.ser = serial.Serial(self.serial_port, self.baud_rate, timeout=1)
        self.log.write("[SERIAL] Conectado à porta {self.serial_port} em {self.baud_rate} bps.")

    def tcpConnect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.tcp_ip, self.tcp_port))
        self.log.write(f"[TCP] Conectado a {self.tcp_ip}:{self.tcp_port}")

    def iniciar(self):
        self.conectar_serial()
        self.conectar_tcp()
        self.running = True
        self.log.write("[INICIADO] Enviando dados da serial para o servidor TCP")
        try:
            while self.running:
                if self.ser.in_waiting:
                    data = self.ser.readline().decode('utf-8').strip()
                    if data:
                        self.sock.sendall((data + "\n").encode('utf-8'))
        except Exception as e:
            self.log.write(f"\n[ERROR] {e}")
        finally:
            self.encerrar()

    def encerrar(self):
        self.running = False
        if self.sock:
            self.sock.close()
            self.log.write("[TCP] Conexão encerrada.")
        if self.ser:
            self.ser.close()
            self.log.write("[SERIAL] Porta serial fechada.")
            self.log.write('[STATUS] Programa Fechado')
