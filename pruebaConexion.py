from db.database import obtener_conexion

# Intentar obtener una conexión
conexion = obtener_conexion()

# Verificar si la conexión fue exitosa
if conexion:
    print("Conexión exitosa a la base de datos.")
    # Puedes realizar más operaciones con la conexión aquí, si es necesario.
else:
    print("No se pudo conectar a la base de datos.")
