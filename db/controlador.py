import pymysql
from db.database import obtener_conexion

def obtenerClientes():
    try:
        conexion = obtener_conexion()
        if conexion is not None:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT cedula, nombre, apellido, correo, telefono, fechaInicioMembresia, fechaFinMembresia FROM Cliente")
                clientes = cursor.fetchall()
                conexion.close()
                return clientes
    except pymysql.Error as error:
        print(f"Error al ejecutar la consulta: {error}")

    return []



# Función para obtener un cliente por cédula
def obtener_cliente_por_cedula(cedula):
    try:
        conexion = obtener_conexion()
        if conexion is not None:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT idCliente, cedula, nombre, apellido, correo, telefono, fechaInicioMembresia, fechaFinMembresia FROM Cliente WHERE cedula = %s", (cedula,))
                cliente = cursor.fetchone()
                conexion.close()
                return cliente
    except pymysql.Error as error:
        print(f"Error al ejecutar la consulta: {error}")

    return None

# Función para obtener un cliente por id

def obtener_cliente_por_id(id_cliente):
    try:
        conexion = obtener_conexion()
        if conexion is not None:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT idCliente, cedula, nombre, apellido, correo, telefono, fechaInicioMembresia, fechaFinMembresia FROM Cliente WHERE idCliente = %s", (id_cliente,))
                cliente = cursor.fetchone()
                conexion.close()
                return cliente
    except pymysql.Error as error:
        print(f"Error al ejecutar la consulta: {error}")

    return None




# Función para registrar la asistencia de un cliente por su ID
def registrar_asistencia_cliente(id_cliente):
    try:
        conexion = obtener_conexion()
        if conexion:
            with conexion.cursor() as cursor:
                cursor.execute("INSERT INTO registroasistencia (idCliente, fechaAsistencia) VALUES (%s, CURDATE())", (id_cliente,))
            conexion.commit()
            conexion.close()
            return True
    except pymysql.Error as error:
        print(f"Error al ejecutar la consulta: {error}")
        return False
    



def obtener_asistencias_diarias():
    try:
        conexion = obtener_conexion()
        if conexion is not None:
            with conexion.cursor() as cursor:
                #cursor.execute("SELECT c.nombre AS nombre_cliente, c.apellido AS apellido_cliente, ra.fechaAsistencia FROM registroasistencia ra JOIN Cliente c ON ra.idCliente = c.idCliente ORDER BY ra.fechaAsistencia DESC;")
                cursor.execute("SELECT c.idCliente, c.nombre AS nombre_cliente, c.apellido AS apellido_cliente, ra.fechaAsistencia FROM registroasistencia ra JOIN Cliente c ON ra.idCliente = c.idCliente ORDER BY ra.fechaAsistencia DESC;")
                asistencias_diarias = cursor.fetchall()

                # Imprime los resultados para verificar
                #print(asistencias_diarias)

                conexion.close()
                return asistencias_diarias
    except Exception as error:
        print(f"Error al obtener asistencias diarias: {error}")

    return []




def obtener_asistencias_diarias_cliente(id_cliente):
    
    try:
        conexion = obtener_conexion()
        if conexion is not None:
            with conexion.cursor() as cursor:
                cursor.execute("SELECT fechaAsistencia FROM registroasistencia WHERE idCliente = %s AND fechaAsistencia = CURDATE()", (id_cliente,))
                asistencias_diarias_cliente = cursor.fetchall()
                conexion.close()
                return asistencias_diarias_cliente
    except pymysql.Error as error:
        print(f"Error al ejecutar la consulta: {error}")

    return []




def insertarCliente(cedula, nombre, apellido, correo, telefono, foto, tipo_membresia, fecha_inicio_membresia):
    try:
        conexion = obtener_conexion()
        if conexion:
            cursor = conexion.cursor()

            # Parámetros del procedimiento almacenado
            argumentos = [
                cedula,
                nombre,
                apellido,
                correo,
                telefono,
                foto.read(),
                tipo_membresia,
                fecha_inicio_membresia
            ]

            # Llama al procedimiento almacenado
            cursor.callproc("anadir_cliente", argumentos)

            # Obtiene el resultado (número de filas afectadas)
            resultado = cursor.rowcount

            # Realiza la confirmación y cierra la conexión
            conexion.commit()
            conexion.close()

            # Devuelve el resultado
            return resultado
    except pymysql.Error as error:
        print(f"Error al ejecutar la consulta: {error}")
        return None
