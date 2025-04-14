import socket
from SerialClass import Serial
from log import LogManager

class SocketHost(Serial):
    def __init__(self, serial_port='COM3', baud_rate=9600, tcp_ip='0.0.0.0', tcp_port=5978):
        super().__init__(serial_port, baud_rate)
        self.tcp_ip = tcp_ip
        self.tcp_port = tcp_port
        self.server_socket = None
        self.client_socket = None
        self.client_address = None
        self.running = False
        self.log = LogManager()

    def StartServer(self):
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.bind((self.tcp_ip, self.tcp_port))
            self.server_socket.listen(1) 
            self.log.write(f"[TCP] Servidor iniciado em {self.tcp_ip}:{self.tcp_port}")
        except Exception as e:
            self.log.write(f"[TCP ERRO] Falha ao iniciar servidor: {e}")

    def AcceptConnection(self):
        try:
            self.log.write("[TCP] Aguardando conexão do cliente...")
            self.client_socket, self.client_address = self.server_socket.accept()
            self.log.write(f"[TCP] Cliente conectado: {self.client_address}")
        except Exception as e:
            self.log.write(f"[TCP ERRO] Falha ao aceitar conexão: {e}")

    def start(self):
        self.SerialStart()
        self.StartServer()
        self.AcceptConnection()

        self.running = True
        self.log.write("[INICIADO] Enviando dados da serial para o cliente TCP")

        try:
            while self.running:
                if self.ser.in_waiting:
                    data = self.ser.readline().decode('utf-8').strip()
                    if data:
                        self.client_socket.sendall((data + "\n").encode('utf-8'))
        except Exception as e:
            self.log.write(f"[ERROR] {e}")
        finally:
            self.close()

    def close(self):
        self.running = False
        if self.client_socket:
            self.client_socket.close()
            self.log.write("[TCP] Conexão com cliente encerrada.")
        if self.server_socket:
            self.server_socket.close()
            self.log.write("[TCP] Servidor encerrado.")
        self.SerialClose()
        self.log.write("[STATUS] Programa Fechado")
