from flask import Flask, render_template, request, redirect, url_for, request, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_wtf import FlaskForm
#from db.usuario import Usuario
from db.controlador import obtener_usuario_por_username, obtenerClientes, insertarCliente, obtener_cliente_por_cedula, registrar_asistencia_cliente, obtener_asistencias_diarias_cliente, obtener_asistencias_diarias, obtener_cliente_por_id, eliminar_cliente_cedula, obtener_cliente
from db import controlador
from flask_wtf.csrf import CSRFProtect
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
from db.forms import RegistroSuperusuarioForm, LoginForm
from db.usuario import Usuario
from werkzeug.security import check_password_hash


app = Flask(__name__)


app.config['SECRET_KEY'] = '8b31879689e5392cb4744f2fd09e67aa5515118b8c8629c4'
login_manager = LoginManager(app)
login_manager.login_view = 'login'

csrf = CSRFProtect(app)


@login_manager.user_loader
def load_user(username):
    return obtener_usuario_por_username(username)



@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = obtener_usuario_por_username(username)

        if user and check_password_hash(user.password, password):
            login_user(user)

            if user.role == 'admin':
                return redirect(url_for('mostrar_clientes'))
            elif user.role == 'cliente':
                return redirect(url_for('mostrar_datos_cliente'))

    return render_template('login.html', form=form)


#REGISTRO DEL SUPERUSUARIO
@app.route('/registrar_superusuario', methods=['GET', 'POST'])
def registrar_superusuario():
    form = RegistroSuperusuarioForm()

    if form.validate_on_submit():
        
        if Usuario.crear_superusuario(form.username.data, form.password.data):
            flash('Superusuario registrado exitosamente', 'success')
            return redirect(url_for('login'))
    print(form.errors)
    return render_template('registrar_superusuario.html', form=form)





@app.route('/dashboard')
@login_required
def dashboard():
    # Ejemplo de cómo acceder al usuario actual
    user_info = f"Usuario actual: {current_user}"
    return f"¡Dashboard! {user_info}"

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



app.config['CARPETA_FOTOS'] = 'static/fotos'

@app.route('/')
def mostrar_clientes():
    # Obtener la lista de clientes desde la base de datos
    clientes = obtenerClientes()

    # Renderizar la plantilla con la lista de clientes
    return render_template('lista_clientes.html', clientes=clientes)

@app.route('/agregar_cliente', methods=['GET', 'POST'])
def agregar_cliente():
    resultado = None
    if request.method == 'POST':
        # Obtener datos del formulario
        cedula = request.form.get('cedula')
        nombre = request.form.get('nombre')
        apellido = request.form.get('apellido')
        correo = request.form.get('correo')
        telefono = request.form.get('telefono')
        # Obtener el archivo de la solicitud
        foto = request.files['foto']
        tipo_membresia = request.form.get('tipo_membresia')
        fecha_inicio_membresia = request.form.get('fecha_inicio_membresia')
        
        resultado = insertarCliente(cedula, nombre, apellido, correo, telefono, foto, tipo_membresia, fecha_inicio_membresia)
        return redirect(url_for('mostrar_clientes'))
    return render_template('agregar.html')


# Nueva ruta para la página de registro de asistencia
@app.route('/registrar_asistencia', methods=['GET'])
def mostrar_formulario_asistencia():
    return render_template('registrar_asistencia.html')

# Ruta para manejar el registro de asistencia
@app.route('/registrar_asistencia', methods=['POST'])
def registrar_asistencia():
    if request.method == 'POST':
        # Obtener el valor de cedula desde el formulario
        cedula = request.form.get('cedula')

        # Lógica para buscar el cliente en la base de datos con la cédula
        cliente = obtener_cliente_por_cedula(cedula)

        if cliente:
            # Registra la asistencia en la tabla 'registroasistencia'
            # (Aquí debes agregar la lógica para insertar en la tabla 'registroasistencia')
            resultado_asistencia = registrar_asistencia_cliente(cliente[0])  # Utiliza el idCliente

            # Verificar si la asistencia se registró correctamente
            if resultado_asistencia:
                # Redireccionar a 'datos_cliente.html' después de registrar la asistencia
                return render_template('datos_cliente.html', cliente=cliente, mensaje="Asistencia registrada exitosamente")
            else:
                # Manejar el caso en que la asistencia no se registre correctamente
                return render_template('registrar_asistencia.html', mensaje_error="Error al registrar asistencia")
        else:
            # Cliente no encontrado, puedes manejar esto como desees
            return render_template('registrar_asistencia.html', mensaje_error="Cliente no encontrado")


# Nueva ruta para mostrar los datos del cliente
@app.route('/datos_cliente', methods=['GET'])
def mostrar_datos_cliente():
    return render_template('datos_cliente.html')


#@app.route('/mostrar_datos_cliente/<int:idCliente>')
@app.route('/mostrar_datos_cliente/<int:idCliente>', methods=['GET'])
def mostrar_datos_cliente_id(idCliente):
    
    cliente = obtener_cliente_por_id(idCliente)

    if cliente:
        return render_template('datos_cliente.html', cliente=cliente)
    else:
        return render_template('error.html', mensaje="Cliente no encontrado")


@app.route('/mostrar_datos_cliente_cedula/<string:cedula>', methods=['GET'])
def mostrar_datos_cliente_cedula(cedula):
    cliente = obtener_cliente(cedula)

    if cliente:
        #print(f"Cliente encontrado: {cliente}")
        return render_template('datos_cliente.html', cliente=cliente)
    else:
        print("Cliente no encontrado")
        return render_template('error.html', mensaje="Cliente no encontrado")



@app.route('/registro_asistencias_diarias')
def registro_asistencias_diarias():
    # Lógica para obtener el registro de asistencias diarias desde la base de datos
    asistencias_diarias = obtener_asistencias_diarias()

    # Renderizar la plantilla con el registro de asistencias diarias
    return render_template('registro_asistencias_diarias.html', asistencias_diarias=asistencias_diarias)


@app.route('/registro_asistencias_diarias_cliente/<id_cliente>')
def registro_asistencias_diarias_cliente(id_cliente):
    # Lógica para obtener las asistencias diarias de un cliente específico
    historial_asistencias_cliente = obtener_asistencias_diarias_cliente(id_cliente)

    # Obtener información del cliente
    cliente = obtener_cliente_por_id(id_cliente)

    # Renderizar la plantilla con las asistencias diarias del cliente
    return render_template('registro_asistencias_diarias_cliente.html', historial_asistencias_cliente=historial_asistencias_cliente, cliente=cliente)



@app.route('/editar_cliente/<string:cedula>', methods=['GET', 'POST'])
def editar_cliente(cedula):
    # Lógica para obtener los detalles del cliente por su cédula
    cliente = obtener_cliente(cedula)

    if request.method == 'POST':
        # Obtener los datos del formulario de edición
        nuevo_nombre = request.form['nombre']
        nuevo_apellido = request.form['apellido']
        nuevo_correo = request.form['correo']
        nuevo_telefono = request.form['telefono']
        nueva_foto = request.form['foto']
        nuevo_tipo_membresia = request.form['tipo_membresia']
        nuevo_fecha_inicio = request.form['fecha_inicio']

        print(f'Datos antes de la actualización para cédula {cedula}:')
        print(f'Cliente: {cliente}')

        controlador.actualizar_cliente_cedula(cedula, nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono, nueva_foto, nuevo_tipo_membresia, nuevo_fecha_inicio)

        print(f'Datos después de la actualización para cédula {cedula}:')
        #cliente_actualizado = obtener_cliente_por_cedula(cedula)
        #print(f'Nombre: {cliente_actualizado[2]}, Apellido: {cliente_actualizado[3]}, Correo: {cliente_actualizado[4]}, Teléfono: {cliente_actualizado[5]}, Foto: {cliente_actualizado[6]}, Tipo membresía: {cliente_actualizado[7]}, Fecha Inicio: {cliente_actualizado[8]}, Fecha Fin: {cliente_actualizado[9]}')

        # Redireccionar a la página de lista de clientes después de la edición
        return redirect(url_for('mostrar_clientes'))

    # Renderizar la plantilla de edición de cliente
    return render_template('editar_cliente.html', cliente=cliente)



@app.route('/actualizar_cliente', methods=['POST'])
def actualizar_cliente():
    if request.method == 'POST':
        # Obtener los datos del formulario de edición
        cedula = request.form['cedula']
        nuevo_nombre = request.form['nombre']
        nuevo_apellido = request.form['apellido']
        nuevo_correo = request.form['correo']
        nuevo_telefono = request.form['telefono']
        nueva_foto = request.form['foto']
        nuevo_tipo_membresia = request.form['tipo_membresia']
        nueva_fecha_inicio = request.form['fecha_inicio']


        # Lógica para actualizar los datos del cliente
        # (Llama al procedimiento almacenado actualizar_cliente_cedula)
        controlador.actualizar_cliente_cedula(cedula, nuevo_nombre, nuevo_apellido, nuevo_correo, nuevo_telefono, nueva_foto, nuevo_tipo_membresia, nueva_fecha_inicio)

        # Redireccionar a la página de lista de clientes después de la edición
        return redirect(url_for('mostrar_clientes'))


@app.route("/delete", methods=["POST"])
def eliminar_cliente_cedula():
    controlador.eliminar_cliente_cedula(request.form["cedula"])
    return redirect(url_for('mostrar_clientes'))



#RUTA PARA HACER PRUEBAS

@app.route('/probar_obtener_cliente_por_id/<int:idCliente>')
def probar_obtener_cliente_por_id(idCliente):
    # Llama a la función obtener_cliente_por_id con el idCliente proporcionado
    cliente = obtener_cliente_por_id(idCliente)

    # Verifica si se encontró el cliente
    if cliente:
        return render_template('datos_cliente.html', cliente=cliente)
    else:
        return render_template('error.html', mensaje="Cliente no encontrado para el ID proporcionado")






if __name__ == '__main__':
    app.run(debug=True)
