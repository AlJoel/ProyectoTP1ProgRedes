import socket
import sqlite3
from datetime import datetime

# Configuración del servidor
HOST = "localhost"
PORT = 5000
DB_NAME = "mensajes.db"

def inicializar_base_datos():
    # inicializa la conexion con la base de datos y crea la tabla en caso de que no exista
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()

        cursor.execute("""CREATE TABLE IF NOT EXISTS mensajes (id INTEGER PRIMARY KEY AUTOINCREMENT,
                                                               contenido TEXT NOT NULL,
                                                               fecha_envio TEXT NOT NULL,
                                                               ip_cliente TEXT NOT NULL)""")

        conexion.commit()
        conexion.close()
        print("Base de datos inicializada correctamente.")
    except sqlite3.Error as e:
        print(f"Error al inicializar la base de datos: {e}")


def guardar_mensaje(contenido, fecha_envio, ip_cliente):
    # Guarda los mensajes recibidos
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()

        cursor.execute("INSERT INTO mensajes (contenido, fecha_envio, ip_cliente) VALUES (?, ?, ?)",
                       (contenido, fecha_envio, ip_cliente))

        conexion.commit()
        conexion.close()
        print("Mensaje guardado correctamente.")
    except sqlite3.Error as e:
        print(f"Error al guardar el mensaje: {e}")


def iniciar_servidor():
    # Inicializa el servidor y lo deja escuchando en el puerto elegido
    inicializar_base_datos()

    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
            servidor.bind((HOST,PORT))
            servidor.listen(1)

            print(f"Servidor escuchando en: {HOST}:{PORT}...")

            while True:
                conn, addr = servidor.accept()
                with conn:
                    print(f"Conexión establecida desde:{addr}")

                    while True:
                        datos = conn.recv(1024)
                        if not datos:
                            break
                        mensaje = datos.decode("utf-8")
                        ip_cliente = addr[0]
                        fecha_envio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                        print(f"Mensaje Recibido:{mensaje}")
                        guardar_mensaje(mensaje, fecha_envio, ip_cliente)

                        respuesta = f"Mensaje Recibido: {fecha_envio}"
                        conn.sendall(respuesta.encode("utf-8"))

                    print("Cliente desconectado.")

    except OSError as e:
        print(f"Error con el socket:{e}")


if __name__ == "__main__":
    iniciar_servidor()