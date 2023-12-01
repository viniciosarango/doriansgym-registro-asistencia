from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import pymysql
from db.database import obtener_conexion

class Usuario(UserMixin):
    def __init__(self, username, password, role, cliente_id=None):
        self.username = username
        self.password = password
        self.role = role
        self.cliente_id = cliente_id

    def get_id(self):
        return self.username
    
    def is_active(self):
        
        return True

    @staticmethod
    def crear_superusuario(username, password):
        try:
            conexion = obtener_conexion()
            if conexion:
                with conexion.cursor() as cursor:
                    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
                    cursor.execute("INSERT INTO usuario (username, password, role) VALUES (%s, %s, %s)", (username, hashed_password, 'admin'))
                
                
                conexion.commit()
                conexion.close()

                print(f"Superusuario registrado con nombre de usuario: {username}")

                return True
        except pymysql.Error as error:
            print(f"Error al ejecutar la consulta: {error}")
            return False