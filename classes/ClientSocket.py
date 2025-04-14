import socket
from SerialClass import Serial
from log import LogManager

class ClienteSocket(Serial):
    def __init__(self, serial_port='COM3', baud_rate=9600, tcp_ip='127.0.0.1', tcp_port=5978):
        super().__init__(serial_port, baud_rate)
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.sock = None
        self.running = False
        self.log = LogManager()

    def Connect(self):
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.connect((self.tcp_ip, self.tcp_port))
            self.log.write(f"[TCP] Conectado a {self.tcp_ip}:{self.tcp_port}")
        except Exception as e:
            self.log.write(f"[TCP ERRO] {e}")

    def Start(self):
        self.SerialStart()
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
            self.log.write(f"[ERROR] {e}")
        finally:
            self.encerrar()

    def Close(self):
        self.running = False
        if self.sock:
            self.sock.close()
            self.log.write("[TCP] Conexão encerrada.")
        self.SerialClose()
        self.log.write("[STATUS] Programa Fechado")
