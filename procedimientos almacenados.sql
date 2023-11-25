
DROP PROCEDURE IF EXISTS obtener_cliente_cedula;
DELIMITER //
CREATE PROCEDURE obtener_cliente_cedula(IN in_cedula VARCHAR(15))
BEGIN
    SELECT *
    FROM Cliente
    WHERE cedula = in_cedula;
END //
DELIMITER ;


-- PRODEDIMIENTO obtener_cliente_cedula variante
DROP PROCEDURE IF EXISTS obtener_cliente_cedula;
DELIMITER //
CREATE PROCEDURE obtener_cliente_cedula (IN in_cedula VARCHAR(15))
BEGIN
    SELECT c.*, m.tipoMembresia
    FROM Cliente c
    LEFT JOIN membresias m ON c.idCliente = m.idCliente
    WHERE c.cedula = in_cedula;
END //
DELIMITER ;

CALL obtener_cliente_cedula('1104286859');



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

        -- Imprimir valores antes de la actualización en la tabla Cliente
        SELECT 'Antes de la actualización en Cliente' AS Etiqueta,
               fechaInicioMembresia, fechaFinMembresia
        FROM Cliente
        WHERE idCliente = id_cliente_existente;

        -- Actualizar los datos del cliente
        UPDATE Cliente
        SET
            nombre = nombre_cliente,
            apellido = apellido_cliente,
            correo = correo_cliente,
            telefono = telefono_cliente,
            fotoCliente = foto_cliente,
            fechaInicioMembresia = fecha_inicio_membresia_nueva,
            fechaFinMembresia = fecha_fin_membresia_nueva
        WHERE cedula = cedula_cliente;

        -- Imprimir valores después de la actualización en la tabla Cliente
        SELECT 'Después de la actualización en Cliente' AS Etiqueta,
               fechaInicioMembresia, fechaFinMembresia
        FROM Cliente
        WHERE idCliente = id_cliente_existente;

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

    END IF;

END //

DELIMITER ;

DROP PROCEDURE IF EXISTS obtener_historial_asistencias_cliente;
delimiter //
CREATE PROCEDURE obtener_historial_asistencias_cliente(IN id_cliente INT)
BEGIN
    SELECT idRegistro, fechaAsistencia FROM registroasistencia
    WHERE idCliente = id_cliente
    AND fechaAsistencia BETWEEN CURDATE() - INTERVAL 30 DAY AND CURDATE();
END //
DELIMITER ;

call obtener_historial_asistencias_cliente (8);






CALL actualizar_cliente_cedula(
    '1103426258',
    'Pepe Enfermo',
    'Losano Macas',
    'email222@mail.com',
    '1235555890',
    NULL,  -- Puedes pasar NULL si no deseas actualizar la foto
    'semestral',  -- Puedes pasar NULL si no deseas actualizar el tipo de membresía
    '2023-11-08'  -- Puedes pasar NULL si no deseas actualizar la fecha de inicio de membresía
);


