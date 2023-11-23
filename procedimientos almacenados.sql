DELIMITER //

CREATE PROCEDURE obtener_cliente_cedula(IN in_cedula VARCHAR(15))
BEGIN
    SELECT *
    FROM Cliente
    WHERE cedula = in_cedula;
END //
DELIMITER ;

CALL obtener_cliente_cedula('1103426258');

DROP PROCEDURE IF EXISTS actualizar_cliente_cedula;
DELIMITER //
CREATE PROCEDURE actualizar_cliente_cedula(
    IN cedula_cliente VARCHAR(15),
    IN nombre_cliente VARCHAR(50),
    IN apellido_cliente VARCHAR(50),
    IN correo_cliente VARCHAR(100),
    IN telefono_cliente VARCHAR(15),
    IN foto_cliente VARCHAR(255),
    IN tipo_membresia_nuevo VARCHAR(50),
    IN fecha_inicio_membresia_nueva DATE
)
BEGIN
    DECLARE id_cliente_existente INT;
    DECLARE fecha_fin_membresia_nueva DATE;

    -- Obtener el ID del cliente existente
    SELECT idCliente INTO id_cliente_existente FROM Cliente WHERE cedula = cedula_cliente;

    -- Verificar si se encontró el cliente
    IF id_cliente_existente IS NOT NULL THEN

        -- Calcular la nueva fecha de fin de membresía según el nuevo tipo de membresía
        CASE tipo_membresia_nuevo
            WHEN 'mensual' THEN SET fecha_fin_membresia_nueva = fecha_inicio_membresia_nueva + INTERVAL 30 DAY;
            WHEN 'trimestral' THEN SET fecha_fin_membresia_nueva = fecha_inicio_membresia_nueva + INTERVAL 90 DAY;
            WHEN 'semestral' THEN SET fecha_fin_membresia_nueva = fecha_inicio_membresia_nueva + INTERVAL 180 DAY;
            WHEN 'anual' THEN SET fecha_fin_membresia_nueva = fecha_inicio_membresia_nueva + INTERVAL 360 DAY;
            ELSE SET fecha_fin_membresia_nueva = fecha_inicio_membresia_nueva;
        END CASE;

        -- Imprimir valores antes de la actualización
        SELECT 'Antes de la actualización' AS Etiqueta,
               nombre, apellido, correo, telefono, fotoCliente,
               (SELECT tipoMembresia FROM Membresias WHERE idCliente = id_cliente_existente) AS tipo_membresia_actual,
               (SELECT fechaInicioMembresia FROM Membresias WHERE idCliente = id_cliente_existente) AS fecha_inicio_actual,
               (SELECT fechaFinMembresia FROM Membresias WHERE idCliente = id_cliente_existente) AS fecha_fin_actual;

        -- Actualizar los datos del cliente
        UPDATE Cliente
        SET
            nombre = nombre_cliente,
            apellido = apellido_cliente,
            correo = correo_cliente,
            telefono = telefono_cliente,
            fotoCliente = foto_cliente
        WHERE cedula = cedula_cliente;

        -- Actualizar el tipo de membresía en la tabla Membresias si se proporciona
        IF tipo_membresia_nuevo IS NOT NULL THEN
            UPDATE Membresias
            SET tipoMembresia = tipo_membresia_nuevo
            WHERE idCliente = id_cliente_existente;
        END IF;

        -- Actualizar la fecha de inicio y fin de membresía en la tabla Membresias si se proporciona la fecha de inicio
        IF fecha_inicio_membresia_nueva IS NOT NULL THEN
            UPDATE Membresias
            SET
                fechaInicioMembresia = fecha_inicio_membresia_nueva,
                fechaFinMembresia = fecha_fin_membresia_nueva
            WHERE idCliente = id_cliente_existente;
        END IF;

        -- Imprimir valores después de la actualización
        SELECT 'Después de la actualización' AS Etiqueta,
               nombre, apellido, correo, telefono, fotoCliente,
               (SELECT tipoMembresia FROM Membresias WHERE idCliente = id_cliente_existente) AS tipo_membresia_actual,
               (SELECT fechaInicioMembresia FROM Membresias WHERE idCliente = id_cliente_existente) AS fecha_inicio_actual,
               (SELECT fechaFinMembresia FROM Membresias WHERE idCliente = id_cliente_existente) AS fecha_fin_actual;

    END IF;

END //
DELIMITER ;

CALL actualizar_cliente_cedula(
    '1103426258',
    'Pepe Sano',
    'Losano Quexada',
    'email4@mail.com',
    '1235555890',
    NULL,  -- Puedes pasar NULL si no deseas actualizar la foto
    'semestral',  -- Puedes pasar NULL si no deseas actualizar el tipo de membresía
    '2023-11-05'  -- Puedes pasar NULL si no deseas actualizar la fecha de inicio de membresía
);

