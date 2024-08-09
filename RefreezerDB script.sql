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
    ID_Proyecto INT,
    ID_Cliente INT NOT NULL,
    FOREIGN KEY (ID_Proyecto) REFERENCES PROYECTO(ID_Proyecto),
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID_Cliente)
);
CREATE TABLE SERVICIO (
    ID_Servicio INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    costo_servicio DECIMAL(10, 2) NOT NULL,
    estado VARCHAR(50) CHECK(estado like "En progreso" OR estado like "Terminado") NOT NULL DEFAULT "En progreso",
    garantia INT,
    Fecha_inicio DATE NOT NULL,
    Fecha_fin DATE,
    ID_Cliente int NOT NULL,
    FOREIGN KEY (ID_Cliente) REFERENCES CLIENTE(ID_Cliente)
);

CREATE TABLE EMPLEADO (
    ID_Empleado INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    correo VARCHAR(100) NOT NULL
);

CREATE TABLE EMPLEADO_SERVICIO (
    ID_Empleado INT,
    ID_Servicio INT,
    PRIMARY KEY (ID_Empleado, ID_Servicio),
    FOREIGN KEY (ID_Empleado) REFERENCES EMPLEADO(ID_Empleado),
    FOREIGN KEY (ID_Servicio) REFERENCES SERVICIO(ID_Servicio)
);

CREATE TABLE CERTIFICADO (
    ID_Certificado INT AUTO_INCREMENT PRIMARY KEY,
    descripcion TEXT NOT NULL,
    fecha_vigencia DATE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    ID_Empleado INT NOT NULL,
    FOREIGN KEY (ID_Empleado) REFERENCES EMPLEADO(ID_Empleado)
);

CREATE TABLE EMPLEADO_CERTIFICADO (
    ID_Certificado INT,
    ID_Empleado INT,
    PRIMARY KEY (ID_Certificado, ID_Empleado),
    FOREIGN KEY (ID_Certificado) REFERENCES CERTIFICADO(ID_Certificado),
    FOREIGN KEY (ID_Empleado) REFERENCES EMPLEADO(ID_Empleado)
);

CREATE TABLE SERVICIO_TECNICO (
    ID_Servicio INT,
    tipo_servicio TEXT NOT NULL,
    PRIMARY KEY (ID_Servicio),
    FOREIGN KEY (ID_Servicio) REFERENCES SERVICIO(ID_Servicio)
);

CREATE TABLE DISEÑO_Y_FABRICACION (
    ID_Servicio INT,
    diseño TEXT NOT NULL,
    tipo_diseño TEXT NOT NULL,
    PRIMARY KEY (ID_Servicio),
    FOREIGN KEY (ID_Servicio) REFERENCES SERVICIO(ID_Servicio)
);

CREATE TABLE MANTENIMIENTO (
    ID_Servicio INT,
    Tipo_Mantenimiento TEXT NOT NULL,
    Name_Unidad_Maquinaria TEXT NOT NULL,
    PRIMARY KEY (ID_Servicio),
    FOREIGN KEY (ID_Servicio) REFERENCES SERVICIO(ID_Servicio)
);

CREATE TABLE INSTALACION_Y_MONTAJE (
    ID_Servicio INT,
    tipo_instalacion TEXT NOT NULL,
    PRIMARY KEY (ID_Servicio),
    FOREIGN KEY (ID_Servicio) REFERENCES SERVICIO(ID_Servicio)
);

CREATE TABLE INVENTARIO (
    ID_Inventario INT AUTO_INCREMENT PRIMARY KEY,
    Stock INT CHECK(Stock >= 0) NOT NULL ,
    nombre VARCHAR(100) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    precio_unidad DECIMAL(10, 2) CHECK(precio_unidad >= 0) NOT NULL
);

CREATE TABLE MATERIAL (
    ID_Material INT AUTO_INCREMENT PRIMARY KEY,
    descripcion VARCHAR(100) NOT NULL,
    marca VARCHAR(50) NOT NULL,
    precio_unidad DECIMAL(10, 2) CHECK(precio_unidad >= 0) NOT NULL,
     ID_Inventario INT NOT NULL,
    FOREIGN KEY (ID_Inventario) REFERENCES INVENTARIO(ID_Inventario)
);
