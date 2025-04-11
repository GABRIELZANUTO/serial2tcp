# servidor_socket.py
import socket

HOST = '0.0.0.0'
PORT = 5978

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)

print(f"Servidor escutando em {HOST}:{PORT}...")

try:
    while True:
        conn, addr = server_socket.accept()
        print(f"Conexão estabelecida com {addr}")


        try:
            while True:
                data = conn.recv(1024)
                if not data:
                    print(f"Conexão encerrada por {addr}")
                    break
                print(f"Recebido de {addr}: {data.decode('utf-8').strip()}")
        except ConnectionResetError:
            print(f"Conexão perdida com {addr}")
        finally:
            conn.close()

except KeyboardInterrupt:
    print("\nServidor encerrado pelo usuário.")
finally:
    server_socket.close()
