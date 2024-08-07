CREATE DATABASE RefreezerDB;
USE RefreezerDB;

CREATE TABLE CLIENTE (
    ID_Cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL
);

CREATE TABLE CLIENTE_NATURAL (
    ID_Cliente INT NOT NULL,
    Cedula VARCHAR(10) NOT NULL,
    PRIMARY KEY (ID_Cliente),
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID_Cliente)
);

CREATE TABLE CLIENTE_EMPRESA (
    ID_Cliente INT NOT NULL,
    RUC VARCHAR(13) NOT NULL,
    PRIMARY KEY (ID_Cliente),
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID_Cliente)
);

CREATE TABLE PROYECTO (
    ID_Proyecto INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    fecha_inicio DATE NOT NULL,
    fecha_fin DATE
);
CREATE TABLE PROFORMA (
    ID_Proforma INT auto_increment PRIMARY KEY,
    fecha_emision DATE NOT NULL,
    costo_mano_obra DECIMAL(10, 2) NOT NULL,
    subtotal DECIMAL(10, 2) NOT NULL,
    estado_aprobacion VARCHAR(50) CHECK(estado_aprobacion like "Aprobado" OR estado_aprobacion like "No Aprobado") NOT NULL DEFAULT "No Aprobado",
    calle VARCHAR(100) NOT NULL,
    manzana VARCHAR(50) NOT NULL,
    ciudad VARCHAR(100) NOT NULL,
    visita_fecha DATE NOT NULL,
    visita_hora TIME NOT NULL,
    visita_observacion TEXT,
    ID_Proyecto INT NOT NULL,
    ID_Cliente INT NOT NULL,
    FOREIGN KEY (ID_Proyecto) REFERENCES PROYECTO(ID_Proyecto),
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID_Cliente)
);
