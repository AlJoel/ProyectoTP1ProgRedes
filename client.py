import socket

# Configuración del cliente
HOST = "localhost"
PORT = 5000

def iniciar_cliente():
    # Inicializa el programa cliente y la conexión con el servidor
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
            cliente.connect((HOST, PORT))
            print(f"Conectado al servidor {HOST}:{PORT}")

            while True:
                mensaje = input("Escribí un mensaje (o 'éxito' para salir): ")

                if mensaje == "éxito":
                    print("Cerrando cliente...")
                    break

                cliente.sendall(mensaje.encode("utf-8"))

                respuesta = cliente.recv(1024).decode("utf-8")
                print(f"Respuesta del servidor: {respuesta}")

    except ConnectionRefusedError:
        print("No se pudo conectar al servidor.")
    except OSError as e:
        print(f"Error en el cliente: {e}")

if __name__ == "__main__":
    iniciar_cliente()