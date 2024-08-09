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
CREATE TABLE SERVICIO_MATERIAL (
    ID_Servicio INT,
    ID_Material INT,
    cantidad_usada INT NOT NULL,
    precio_unidad DECIMAL(10, 2) CHECK(precio_unidad >= 0) NOT NULL,
    PRIMARY KEY (ID_Servicio, ID_Material),
    FOREIGN KEY (ID_Servicio) REFERENCES SERVICIO(ID_Servicio),
    FOREIGN KEY (ID_Material) REFERENCES MATERIAL(ID_Material)
);

CREATE TABLE PROVEEDOR (
    ID_Proveedor INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    disponibilidad VARCHAR(50) NOT NULL
);

CREATE TABLE INVENTARIO_PROVEEDOR (
    ID_Inventario INT,
    ID_Proveedor INT,
    PRIMARY KEY (ID_Inventario, ID_Proveedor),
    FOREIGN KEY (ID_Inventario) REFERENCES INVENTARIO(ID_Inventario),
    FOREIGN KEY (ID_Proveedor) REFERENCES PROVEEDOR(ID_Proveedor)
);
INSERT INTO CLIENTE VALUES
(1, 'Coca Cola', 'Calle 1, Zona Industrial', 'contacto@abc.com', '1234567890'),
(2, 'Fiber Home', 'Av. Central, Edificio XYZ', 'info@xyz.com', '0987654321'),
(3, 'Carlos Pérez', 'Calle 5, Edificio 3', 'c.perez@mail.com', '0922334455'),
(4, 'María García', 'Av. Principal, Casa 10', 'm.garcia@mail.com', '0933445566'),
(5, 'Juan Rodríguez', 'Calle 8, Casa 14', 'juan.r@mail.com', '0944556677'),
(6, 'Comercial Juanita', 'Zona Comercial, Local 5', 'ventas@lmn.com', '4455667788'),
(7, 'José Fernández', 'Av. Secundaria, Edificio 2', 'jose.fernandez@mail.com', '0966778899'),
(8, 'Ana López', 'Calle 2, Casa 6', 'ana.lopez@mail.com', '0977889900'),
(9, 'Telconet', 'Parque Industrial, N° 7', 'servicios@pqr.com', '7788990011'),
(10, 'Luisa Ramírez', 'Calle 3, Edificio 8', 'l.ramirez@mail.com', '0999001122');

INSERT INTO CLIENTE_NATURAL VALUES
(3, '0934567890'),
(4, '0945678901'),
(5, '0256789012'),
(7, '1167890123'),
(8, '2478901234'),
(10,'0989012345');

INSERT INTO CLIENTE_EMPRESA VALUES
(1, '0912345678001'),
(2, '0923456789001'),
(6, '0967890123001'),
(9, '0990123456001');
