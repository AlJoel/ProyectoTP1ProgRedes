import sqlite3

DB_NAME = "mensajes.db"

def ver_mensajes():
    # Obtener todos los mensajes almacenados
    try:
        conexion = sqlite3.connect(DB_NAME)
        cursor = conexion.cursor()

        cursor.execute("SELECT * FROM mensajes")
        filas = cursor.fetchall()

        print("Mensajes guardados:\n")

        for fila in filas:
            print(f"ID: {fila[0]}")
            print(f"Contenido: {fila[1]}")
            print(f"Fecha: {fila[2]}")
            print(f"IP: {fila[3]}")
            print("-" *git  30)

        conexion.close()

    except sqlite3.Error as e:
        print(f"Error al leer la base de datos:{e}")


if __name__ == "__main__":
    ver_mensajes()