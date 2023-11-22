CREATE DATABASE dorians_gym;

USE dorians_gym;

drop table cliente;


CREATE TABLE Cliente (
    idCliente INT PRIMARY KEY AUTO_INCREMENT,
    cedula VARCHAR(15) UNIQUE,
    nombre VARCHAR(50),
    apellido VARCHAR(50),
    correo VARCHAR(100),
    telefono VARCHAR(15),
    fotoCliente BLOB, -- Puedes almacenar la foto del cliente como un BLOB (Binary Large Object)
    fechaInicioMembresia DATE,
    fechaFinMembresia DATE
);

CREATE TABLE Membresias (
    idMembresia INT PRIMARY KEY AUTO_INCREMENT,
    idCliente INT,
    tipoMembresia VARCHAR(50),
    fechaInicio DATE,
    fechaFin DATE,
    FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente)
);


CREATE TABLE RegistroEntrada (
    idRegistroEntrada INT PRIMARY KEY AUTO_INCREMENT,
    idCliente INT,
    fecha DATE,
    horaEntrada TIME,
    FOREIGN KEY (idCliente) REFERENCES Cliente(idCliente)
);

RENAME TABLE registroentrada TO registro_entrada;



