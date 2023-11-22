DELIMITER //

CREATE PROCEDURE anadir_cliente(
    IN cedula_cliente VARCHAR(15),
    IN nombre_cliente VARCHAR(50),
    IN apellido_cliente VARCHAR(50),
    IN correo_cliente VARCHAR(100),
    IN telefono_cliente VARCHAR(15),
    IN foto_cliente VARCHAR(255),
    IN fecha_inicio_membresia DATE
)
BEGIN
    DECLARE tipo_membresia_cliente VARCHAR(50);
    DECLARE fecha_fin_membresia DATE;

    -- Obtiene el tipo de membresía del cliente
    SELECT tipoMembresia INTO tipo_membresia_cliente
    FROM membresias
    WHERE idCliente = cedula_cliente
    ORDER BY fechaFin DESC
    LIMIT 1;

    -- Calcula la fecha de fin de membresía según el tipo de membresía
    CASE tipo_membresia_cliente
        WHEN 'mensual' THEN SET fecha_fin_membresia = fecha_inicio_membresia + INTERVAL 30 DAY;
        -- Añade más casos según otros tipos de membresía (trimestral, semestral, etc.)
        WHEN 'trimestral' THEN SET fecha_fin_membresia = fecha_inicio_membresia + INTERVAL 90 DAY;
        WHEN 'semestrar' THEN SET fecha_fin_membresia = fecha_inicio_membresia + INTERVAL 180 DAY;
        WHEN 'anual' THEN SET fecha_fin_membresia = fecha_inicio_membresia + INTERVAL 360 DAY;
        -- ...
        ELSE SET fecha_fin_membresia = fecha_inicio_membresia; -- Manejo de casos no contemplados
    END CASE;

    -- Inserta el nuevo cliente en la tabla Cliente
    INSERT INTO Cliente (
        cedula,
        nombre,
        apellido,
        correo,
        telefono,
        fotoCliente,
        fechaInicioMembresia,
        fechaFinMembresia
    ) VALUES (
        cedula_cliente,
        nombre_cliente,
        apellido_cliente,
        correo_cliente,
        telefono_cliente,
        foto_cliente,
        fecha_inicio_membresia,
        fecha_fin_membresia
    );
END //

DELIMITER ;

CALL anadir_cliente(
     '1233436789',          -- Cédula del cliente
     'Juan',               -- Nombre del cliente
     'Perez',              -- Apellido del cliente
     'correo@ejemplo.com', -- Correo del cliente
     '1234567890',         -- Teléfono del cliente
     'static/fotos/membresia-caducada-2.png', -- Ruta de la foto del cliente
     CURDATE()              -- Fecha de inicio de membresía (usa la fecha actual)
);





