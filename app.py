from flask import Flask, render_template, request, redirect, url_for
from db.controlador import obtenerClientes, insertarCliente, obtener_cliente_por_cedula, registrar_asistencia_cliente, obtener_asistencias_diarias_cliente, obtener_asistencias_diarias, obtener_cliente_por_id
from flask import request




app = Flask(__name__)
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


@app.route('/mostrar_datos_cliente/<int:idCliente>')
def mostrar_datos_cliente_id(idCliente):
    
    cliente = obtener_cliente_por_id(idCliente)

    if cliente:
        return render_template('datos_cliente.html', cliente=cliente)
    else:
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
    asistencias_diarias_cliente = obtener_asistencias_diarias_cliente(id_cliente)

    # Renderizar la plantilla con las asistencias diarias del cliente
    return render_template('registro_asistencias_diarias_cliente.html', asistencias_diarias_cliente=asistencias_diarias_cliente)


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
