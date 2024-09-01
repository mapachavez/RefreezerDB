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

INSERT INTO PROYECTO VALUES
(1, 'Instalación de Cámara Frigorífica', '2023-01-10', '2023-02-10'),
(2, 'Mantenimiento de Sistemas de Refrigeración', '2023-03-15', '2023-04-15'),
(3, 'Instalación de Aire Acondicionado', '2023-05-20', '2023-06-20'),
(4, 'Reparación de Unidad de Aire', '2023-07-25', '2023-08-25'),
(5, 'Revisión de Sistemas de Enfriamiento', '2023-09-30', '2023-10-30'),
(6, 'Instalación de Enfriadores Industriales', '2023-11-05', '2023-12-05'),
(7, 'Mantenimiento de Aires Acondicionados', '2024-01-10', '2024-02-10'),
(8, 'Instalación de Unidad de Refrigeración', '2024-03-15', '2024-04-15'),
(9, 'Optimización de Sistemas de Enfriamiento', '2024-05-20', '2024-06-20'),
(10, 'Revisión de Equipos de Refrigeración', '2024-07-25', '2024-08-25');

INSERT INTO PROFORMA VALUES
(1, '2023-01-01', 500.00, 1500.00, 'Aprobado', 'Calle 1', 'Mz5', 'Guayaquil', '2023-01-10', '10:00:00', 'Ninguna', 1, 1),
(2, '2023-02-01', 300.00, 1200.00, 'No Aprobado', 'Av. Central', 'Mz2', 'Quito', '2023-03-15', '11:00:00', 'Ninguna', 2, 2),
(3, '2023-03-01', 400.00, 1300.00, 'Aprobado', 'Calle 5', 'Mz18', 'Cuenca', '2023-05-20', '12:00:00', 'Ninguna', 3, 3),
(4, '2023-04-01', 350.00, 1400.00, 'No Aprobado', 'Av. Principal', 'Mz6', 'Loja', '2023-07-25', '13:00:00', 'Ninguna', 4, 4),
(5, '2023-05-01', 450.00, 1600.00, 'Aprobado', 'Calle 8', 'Mz1', 'Manta', '2023-09-30', '14:00:00', 'Ninguna', 5, 5),
(6, '2023-06-01', 500.00, 1700.00, 'No Aprobado', 'Zona Comercial', 'Mz10', 'Portoviejo', '2023-11-05', '15:00:00', 'Ninguna', 6, 6),
(7, '2023-07-01', 600.00, 1800.00, 'Aprobado', 'Av. Secundaria', 'Mz6', 'Esmeraldas', '2024-01-10', '16:00:00', 'Ninguna', 7, 7),
(8, '2023-08-01', 550.00, 1900.00, 'No Aprobado', 'Calle 2', 'Mz2', 'Ambato', '2024-03-15', '17:00:00', 'Ninguna', 8, 8),
(9, '2023-09-01', 650.00, 2000.00, 'Aprobado', 'Parque Industrial', 'Mz4', 'Machala', '2024-05-20', '18:00:00', 'Ninguna', 9, 9),
(10, '2023-10-01', 700.00, 2100.00, 'No Aprobado', 'Calle 3', 'Mz3', 'Latacunga', '2024-07-25', '19:00:00', 'Ninguna', 10, 10);

INSERT INTO SERVICIO VALUES
(1, 'Instalación de Cámara Frigorífica', 2000.00, 'Terminado', 12, '2023-01-10', '2023-02-10', 1),
(2, 'Mantenimiento de Sistemas de Refrigeración', 1500.00, 'En Progreso', 6, '2023-03-15', '2023-04-15', 2),
(3, 'Instalación de Aire Acondicionado', 1800.00, 'Terminado', 12, '2023-05-20', '2023-06-20', 3),
(4, 'Reparación de Unidad de Aire', 1600.00, 'En Progreso', 6, '2023-07-25', '2023-08-25', 4),
(5, 'Revisión de Sistemas de Enfriamiento', 1700.00, 'Terminado', 12, '2023-09-30', '2023-10-30', 5),
(6, 'Instalación de Enfriadores Industriales', 2200.00, 'En Progreso', 6, '2023-11-05', '2023-12-05', 6),
(7, 'Mantenimiento de Aires Acondicionados', 1900.00, 'Terminado', 12, '2024-01-10', '2024-02-10', 7),
(8, 'Instalación de Unidad de Refrigeración', 2100.00, 'En Progreso', 6, '2024-03-15', '2024-04-15', 8),
(9, 'Optimización de Sistemas de Enfriamiento', 2300.00, 'Terminado', 12, '2024-05-20', '2024-06-20', 9),
(10, 'Revisión de Equipos de Refrigeración', 2400.00, 'En Progreso', 6, '2024-07-25', '2024-08-25', 10);

INSERT INTO EMPLEADO VALUES
(1, 'Pedro Jiménez', 'Técnico', 'pedro.j@refreezrec.com'),
(2, 'Lucía Morales', 'Ingeniera', 'lucia.m@refreezrec.com'),
(3, 'Miguel Ángel', 'Supervisor', 'miguel.a@refreezrec.com'),
(4, 'Claudia Ruiz', 'Administradora', 'claudia.r@refreezrec.com'),
(5, 'Ricardo Díaz', 'Técnico', 'ricardo.d@refreezrec.com'),
(6, 'Elena Torres', 'Ventas', 'elena.t@refreezrec.com'),
(7, 'Fernando Gómez', 'Mantenimiento', 'fernando.g@refreezrec.com'),
(8, 'Sofía Herrera', 'Ingeniera', 'sofia.h@refreezrec.com'),
(9, 'David Vargas', 'Técnico', 'david.v@refreezrec.com'),
(10, 'Laura Mendoza', 'Recepcionista', 'laura.m@refreezrec.com');

INSERT INTO EMPLEADO_SERVICIO VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO CERTIFICADO VALUES
(1, 'Certificado de Refrigeración', '2025-12-31', 'Pedro Jiménez',1),
(2, 'Certificado de Instalación de Aires Acondicionados', '2024-11-30', 'Lucía Morales',2),
(3, 'Certificado de Mantenimiento Industrial', '2026-10-29', 'Miguel Ángel',3),
(4, 'Certificado de Gestión Administrativa', '2025-09-28', 'Claudia Ruiz',4),
(5, 'Certificado de Seguridad en el Trabajo', '2024-08-27', 'Ricardo Díaz',5),
(6, 'Certificado de Ventas y Atención al Cliente', '2024-09-26', 'Elena Torres',6),
(7, 'Certificado de Mantenimiento Preventivo', '2026-06-25', 'Fernando Gómez',7),
(8, 'Certificado de Ingeniería en Refrigeración', '2025-05-24', 'Sofía Herrera',8),
(9, 'Certificado de Técnico en Aires Acondicionados', '2025-04-23', 'David Vargas',9),
(10, 'Certificado de Atención al Cliente', '2025-03-22', 'Laura Mendoza',10);

INSERT INTO EMPLEADO_CERTIFICADO VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);

INSERT INTO SERVICIO_TECNICO VALUES
(1, 'Instalación'),
(2, 'Mantenimiento'),
(3, 'Instalación'),
(4, 'Reparación'),
(5, 'Revisión'),
(6, 'Instalación'),
(7, 'Mantenimiento'),
(8, 'Instalación'),
(9, 'Optimización'),
(10, 'Revisión');

INSERT INTO DISEÑO_Y_FABRICACION VALUES
(1, 'Diseño de Cámara Frigorífica', 'Industrial'),
(2, 'Mantenimiento de Sistemas', 'Industrial'),
(3, 'Diseño de Aire Acondicionado', 'Residencial'),
(4, 'Reparación de Unidad', 'Residencial'),
(5, 'Revisión de Sistemas', 'Industrial'),
(6, 'Diseño de Enfriadores', 'Industrial'),
(7, 'Mantenimiento de Aires', 'Residencial'),
(8, 'Diseño de Unidad de Refrigeración', 'Industrial'),
(9, 'Optimización de Sistemas', 'Industrial'),
(10, 'Revisión de Equipos', 'Industrial');

INSERT INTO MANTENIMIENTO VALUES
(1, 'Preventivo', 'Cámara Frigorífica'),
(2, 'Correctivo', 'Sistema de Refrigeración'),
(3, 'Preventivo', 'Aire Acondicionado'),
(4, 'Correctivo', 'Unidad de Aire'),
(5, 'Preventivo', 'Sistema de Enfriamiento'),
(6, 'Correctivo', 'Enfriadores Industriales'),
(7, 'Preventivo', 'Aires Acondicionados'),
(8, 'Correctivo', 'Unidad de Refrigeración'),
(9, 'Preventivo', 'Sistema de Enfriamiento'),
(10, 'Correctivo', 'Equipos de Refrigeración');

INSERT INTO INSTALACION_Y_MONTAJE VALUES
(1, 'Instalación de Cámara Frigorífica'),
(2, 'Instalación de Sistemas de Refrigeración'),
(3, 'Instalación de Aire Acondicionado'),
(4, 'Reparación de Unidad de Aire'),
(5, 'Instalación de Sistemas de Enfriamiento'),
(6, 'Instalación de Enfriadores Industriales'),
(7, 'Instalación de Aires Acondicionados'),
(8, 'Instalación de Unidad de Refrigeración'),
(9, 'Optimización de Sistemas de Enfriamiento'),
(10, 'Revisión de Equipos de Refrigeración');

INSERT INTO INVENTARIO VALUES
(1, 100, 'Refrigerante R-410A', 'DuPont', 100.00),
(2, 50, 'Compresor', 'LG', 300.00),
(3, 30, 'Evaporador', 'Samsung', 200.00),
(4, 20, 'Condensador', 'Panasonic', 250.00),
(5, 200, 'Termostato', 'Honeywell', 50.00),
(6, 40, 'Válvula de Expansión', 'Danfoss', 150.00),
(7, 60, 'Filtro Deshidratador', 'Parker', 80.00),
(8, 10, 'Unidad de Control', 'Johnson Controls', 500.00),
(9, 25, 'Motor Ventilador', 'GE', 120.00),
(10, 150, 'Sensor de Temperatura', 'Siemens', 70.00);

INSERT INTO MATERIAL VALUES
(1, 'Refrigerante R-410A', 'DuPont', 100.00,1),
(2, 'Compresor', 'LG', 300.00,2),
(3, 'Evaporador', 'Samsung', 200.00,3),
(4, 'Condensador', 'Panasonic', 250.00,4),
(5, 'Termostato', 'Honeywell', 50.00,5),
(6, 'Válvula de Expansión', 'Danfoss', 150.00,6),
(7, 'Filtro Deshidratador', 'Parker', 80.00,7),
(8, 'Unidad de Control', 'Johnson Controls', 500.00,8),
(9, 'Motor Ventilador', 'GE', 120.00,9),
(10, 'Sensor de Temperatura', 'Siemens', 70.00,10);

INSERT INTO SERVICIO_MATERIAL VALUES
(1, 1, 10, 100.00),
(2, 2, 5, 80.00),
(3, 3, 2, 50.00),
(4, 4, 3, 60.00),
(5, 5, 4, 70.00),
(6, 6, 8, 200.00),
(7, 7, 6, 90.00),
(8, 8, 7, 150.00),
(9, 9, 5, 120.00),
(10, 10, 9, 110.00);

INSERT INTO PROVEEDOR VALUES
(1, 'Carrier', 'carrier@mail.com', '1112223334', 'Disponible'),
(2, 'YORK', 'york@mail.com', '2223334445', 'Disponible'),
(3, 'PARKER', 'parker@mail.com', '3334445556', 'No Disponible'),
(4, 'Bitzer', 'blitzer@mail.com', '4445556667', 'Disponible'),
(5, 'MYCOM', 'mycom@mail.com', '5556667778', 'Disponible'),
(6, 'Vilter', 'Vilter@mail.com', '6667778889', 'No Disponible'),
(7, 'HANSES-TECNOLOGIES', 'hansen_tech@mail.com', '7778889990', 'Disponible'),
(8, 'COPELAND', 'copeland@mail.com', '8889990001', 'Disponible'),
(9, 'North Star', 'north_star@mail.com', '9990001112', 'No Disponible'),
(10, 'Cool Tech', 'cool_tech@mail.com', '0001112223', 'Disponible');

INSERT INTO INVENTARIO_PROVEEDOR VALUES
(1, 1),
(2, 2),
(3, 3),
(4, 4),
(5, 5),
(6, 6),
(7, 7),
(8, 8),
(9, 9),
(10, 10);


-- triggers 
DELIMITER /
CREATE TRIGGER tr_actualizar_stock_inventario
AFTER INSERT ON SERVICIO_MATERIAL
FOR EACH ROW
BEGIN
    DECLARE nuevo_stock INT;
    
    -- Calcular el nuevo stock
    SELECT Stock INTO nuevo_stock 
    FROM INVENTARIO 
    WHERE ID_Inventario = (SELECT ID_Inventario FROM MATERIAL WHERE ID_Material = NEW.ID_Material);
    
    IF nuevo_stock < NEW.cantidad_usada THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'Stock insuficiente en el inventario';
    ELSE
        -- Actualizar el stock
        UPDATE INVENTARIO
        SET Stock = Stock - NEW.cantidad_usada
        WHERE ID_Inventario = (SELECT ID_Inventario FROM MATERIAL WHERE ID_Material = NEW.ID_Material);
    END IF;
END /
DELIMITER;

-- el siguiente es para validar fechas en la tabla de proformas
DELIMITER /
CREATE TRIGGER tg_valida_fechas_proforma
BEFORE INSERT ON PROFORMA
FOR EACH ROW
BEGIN
    IF NEW.fecha_emision > NEW.visita_fecha THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'La fecha de emisión no puede ser posterior a la fecha de visita';
    END IF;
END /
DELIMITER ;

-- reportes 

-- reporte de proyectos por cliente_empresa
create view clientes_empresa
AS SELECT 
    C.nombre AS "Nombre Cliente", 
    P.nombre AS "Nombre Proyecto", 
    P.fecha_inicio AS "Fecha Inicio", 
    P.fecha_fin AS "Fecha Fin"
	FROM PROYECTO P
    JOIN PROFORMA PF ON P.ID_proyecto = PF.ID_proyecto
    JOIN CLIENTE C ON PF.ID_cliente = C.ID_cliente
    JOIN CLIENTE_EMPRESA CE ON C.ID_cliente = CE.ID_cliente;

-- reporte de servicios por empleado
create view servicios_por_empleado
AS SELECT 
    E.nombre AS "Nombre Empleado",
    S.descripcion AS "Descripción Servicio",
    S.estado AS "Estado",
    S.Fecha_inicio AS "Fecha Inicio",
    S.Fecha_fin AS "Fecha Fin"
	FROM SERVICIO S
    JOIN EMPLEADO_SERVICIO ES ON S.ID_Servicio = ES.ID_Servicio
    JOIN EMPLEADO E ON ES.ID_Empleado = E.ID_Empleado;

-- reporte de inventario con sus proveedores asosiados
create view inventario_y_proveedores
AS SELECT 
    I.nombre AS "Material",
    I.Stock AS "Stock Disponible",
    P.nombre AS "Proveedor",
    P.disponibilidad AS "Disponibilidad"
	FROM 
    INVENTARIO I
    JOIN INVENTARIO_PROVEEDOR IP ON I.ID_Inventario = IP.ID_Inventario
    JOIN PROVEEDOR P ON IP.ID_Proveedor = P.ID_Proveedor;

-- reporte de empleados y servicios asosiados donde tambien se mostrara el certificado del empleado 
create view empleados_y_servicios
AS SELECT 
    E.nombre AS "Nombre Empleado",
    C.descripcion AS "Descripción Certificado",
    C.fecha_vigencia AS "Fecha Vigencia",
    S.descripcion AS "Descripción Servicio",
    S.estado AS "Estado Servicio"
	FROM 
    EMPLEADO E
    JOIN CERTIFICADO C ON E.ID_Empleado = C.ID_Empleado
    JOIN EMPLEADO_SERVICIO ES ON E.ID_Empleado = ES.ID_Empleado
    JOIN SERVICIO S ON ES.ID_Servicio = S.ID_Servicio
	ORDER BY 
    E.nombre, C.fecha_vigencia;

-- tabla cliente
-- procedimiento para la insercion de clientes 
DELIMITER //
CREATE PROCEDURE sp_insert_cliente(
    IN p_nombre VARCHAR(50),
    IN p_direccion VARCHAR(255),
    IN p_correo VARCHAR(100),
    IN p_telefono VARCHAR(10),
    IN p_tipo_cliente CHAR(1), -- 'N' para Natural, 'E' para Empresa
    IN p_identificacion VARCHAR(13))
BEGIN
    START TRANSACTION;

    INSERT INTO CLIENTE
    VALUES (0,p_nombre, p_direccion, p_correo, p_telefono);

    -- Inserta en la tabla correspondiente al tipo de cliente usando LAST_INSERT_ID() para obtener el ID del cliente recién insertado
    IF p_tipo_cliente = 'N' THEN
        INSERT INTO CLIENTE_NATURAL (ID_cliente, Cedula)
        VALUES (LAST_INSERT_ID(), p_identificacion);
    ELSEIF p_tipo_cliente = 'E' THEN
        INSERT INTO CLIENTE_EMPRESA (ID_cliente, RUC)
        VALUES (LAST_INSERT_ID(), p_identificacion);
    END IF;

    COMMIT;

    SELECT 'Cliente insertado correctamente';
END //
DELIMITER ;

-- procedimiento para actualizacion de clientes
DELIMITER //
CREATE PROCEDURE sp_update_cliente(
    IN p_id_cliente INT,
    IN p_nombre VARCHAR(50),
    IN p_direccion VARCHAR(255),
    IN p_correo VARCHAR(100),
    IN p_telefono VARCHAR(10),
    IN p_cedula VARCHAR(13),
    IN p_ruc VARCHAR(13)       
)
BEGIN
    START TRANSACTION;
    UPDATE CLIENTE 
    SET nombre = p_nombre, direccion = p_direccion, correo = p_correo, telefono = p_telefono
    WHERE ID_cliente = p_id_cliente;

    IF EXISTS (SELECT * FROM CLIENTE_NATURAL WHERE ID_cliente = p_id_cliente) THEN
        UPDATE CLIENTE_NATURAL 
        SET Cedula = p_cedula
        WHERE ID_cliente = p_id_cliente;
    END IF;

    IF EXISTS (SELECT * FROM CLIENTE_EMPRESA WHERE ID_cliente = p_id_cliente) THEN
        UPDATE CLIENTE_EMPRESA 
        SET RUC = p_ruc
        WHERE ID_cliente = p_id_cliente;
    END IF;
    COMMIT;
    SELECT 'Cliente actualizado correctamente';
END //
DELIMITER ;

-- procedimiento para eliminacion de cliente
DELIMITER //
CREATE PROCEDURE sp_delete_cliente(IN p_id_cliente INT)
BEGIN
    START TRANSACTION;

    DELETE FROM CLIENTE_NATURAL WHERE ID_cliente = p_id_cliente;
    DELETE FROM CLIENTE_EMPRESA WHERE ID_cliente = p_id_cliente;
    DELETE FROM CLIENTE WHERE ID_cliente = p_id_cliente;

    COMMIT;

    SELECT 'Cliente eliminado correctamente';
END //
DELIMITER ;

-- procedimientos para la tabla de servicios
-- insertar servicio
DELIMITER // 
CREATE PROCEDURE sp_insert_servicio(
    IN p_descripcion TEXT,
    IN p_costo_servicio DECIMAL(10,2),
    IN p_estado VARCHAR(50),
    IN p_garantia INT,
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE,
    IN p_id_cliente INT,
    IN p_id_proforma INT
)
BEGIN
    START TRANSACTION;

    INSERT INTO SERVICIO     
    VALUES (0,p_descripcion, p_costo_servicio, p_estado, p_garantia, p_fecha_inicio, p_fecha_fin, p_id_cliente, p_id_proforma);
    COMMIT;
    SELECT 'Servicio insertado correctamente';
END //
DELIMITER ;

-- sp para insertar diseño y fabricacion
DELIMITER //
CREATE PROCEDURE sp_insert_diseno_y_fabricacion(
    IN p_diseno TEXT,
    IN p_tipo_diseno TEXT
)
BEGIN
    DECLARE v_id_servicio INT;

    SET v_id_servicio = LAST_INSERT_ID();
    START TRANSACTION;
    INSERT INTO DISEÑO_Y_FABRICACIÓN (
        ID_Servicio, diseño, tipo_diseño
    )
    VALUES (
        v_id_servicio, p_diseno, p_tipo_diseno
    );
    COMMIT;
    SELECT 'Registro insertado en la tabla Diseño y Fabricación correctamente';
END //
DELIMITER ;

-- sp para insertar un servicio tecnico
DELIMITER //
CREATE PROCEDURE sp_insert_servicio_tecnico(
    IN p_tipo_servicio TEXT
)
BEGIN
    DECLARE v_id_servicio INT;

    SET v_id_servicio = LAST_INSERT_ID();
    START TRANSACTION;
    INSERT INTO SERVICIO_TECNICO (
        ID_Servicio, tipo_servicio
    )
    VALUES (
        v_id_servicio, p_tipo_servicio
    );
    COMMIT;
    SELECT 'Registro insertado en la tabla Servicio Técnico correctamente';
END //
DELIMITER ;

-- sp para insertar una instalacion y montaje
DELIMITER // 
CREATE PROCEDURE sp_insert_instalacion_y_montaje(
    IN p_tipo_instalacion TEXT
)
BEGIN
    DECLARE v_id_servicio INT;

    SET v_id_servicio = LAST_INSERT_ID();
    START TRANSACTION;
    INSERT INTO INSTALACION_Y_MONTAJE (
        ID_Servicio, tipo_instalacion
    )
    VALUES (
        v_id_servicio, p_tipo_instalacion
    );
    COMMIT;
    SELECT 'Registro insertado en la tabla Instalación y Montaje correctamente';
END //
DELIMITER ;

-- sp para insertar un mantenimiento
DELIMITER //
CREATE PROCEDURE sp_insert_mantenimiento(
    IN p_tipo_mantenimiento TEXT,
    IN p_name_unidad_maquinaria TEXT
)
BEGIN
    DECLARE v_id_servicio INT;

    SET v_id_servicio = LAST_INSERT_ID();
    START TRANSACTION;
    INSERT INTO MANTENIMIENTO (
        ID_Servicio, Tipo_Mantenimiento, Name_Unidad_Maquinaria
    )
    VALUES (
        v_id_servicio, p_tipo_mantenimiento, p_name_unidad_maquinaria
    );
    COMMIT;
    SELECT 'Registro insertado en la tabla Mantenimiento correctamente';
END //
DELIMITER ;


-- actualizacion de servicio
DELIMITER //
CREATE PROCEDURE sp_update_servicio(
    IN p_id_servicio INT,
    IN p_descripcion TEXT,
    IN p_costo_servicio DECIMAL(10,2),
    IN p_estado VARCHAR(50),
    IN p_garantia INT,
    IN p_fecha_inicio DATE,
    IN p_fecha_fin DATE
)
BEGIN
    START TRANSACTION;

    -- Actualiza los datos del servicio en la tabla SERVICIO
    UPDATE SERVICIO 
    SET descripcion = p_descripcion, costo_servicio = p_costo_servicio, estado = p_estado, 
        garantia = p_garantia, Fecha_inicio = p_fecha_inicio, Fecha_fin = p_fecha_fin
    WHERE ID_Servicio = p_id_servicio;

    COMMIT;

    SELECT 'Servicio actualizado correctamente';
END //
DELIMITER ;


-- eliminar servicio
DELIMITER //
CREATE PROCEDURE sp_delete_servicio(
    IN p_id_servicio INT
)
BEGIN
    DECLARE id_diseño INT DEFAULT 0;
    DECLARE id_tecnico INT DEFAULT 0;
    DECLARE id_montaje INT DEFAULT 0;
    DECLARE id_mantenimiento INT DEFAULT 0;

    START TRANSACTION;

    -- Verifica si el servicio existe en la tabla DISEÑO_Y_FABRICACIÓN
    SELECT COUNT(*) INTO id_diseño
    FROM DISEÑO_Y_FABRICACION
    WHERE ID_Servicio = p_id_servicio;

    IF id_diseño > 0 THEN
        DELETE FROM DISEÑO_Y_FABRICACION WHERE ID_Servicio = p_id_servicio;
    END IF;

    -- Verifica si el servicio existe en la tabla SERVICIO_TECNICO
    SELECT COUNT(*) INTO id_tecnico
    FROM SERVICIO_TECNICO
    WHERE ID_Servicio = p_id_servicio;

    IF id_tecnico > 0 THEN
        DELETE FROM SERVICIO_TECNICO WHERE ID_Servicio = p_id_servicio;
    END IF;

    -- Verifica si el servicio existe en la tabla INSTALACION_Y_MONTAJE
    SELECT COUNT(*) INTO id_montaje
    FROM INSTALACION_Y_MONTAJE
    WHERE ID_Servicio = p_id_servicio;

    IF id_montaje > 0 THEN
        DELETE FROM INSTALACION_Y_MONTAJE WHERE ID_Servicio = p_id_servicio;
    END IF;

    -- Verifica si el servicio existe en la tabla MANTENIMIENTO
    SELECT COUNT(*) INTO id_mantenimiento
    FROM MANTENIMIENTO
    WHERE ID_Servicio = p_id_servicio;

    IF id_mantenimiento > 0 THEN
        DELETE FROM MANTENIMIENTO WHERE ID_Servicio = p_id_servicio;
    END IF;

    -- Finalmente, borra el servicio de la tabla SERVICIO
    DELETE FROM SERVICIO WHERE ID_Servicio = p_id_servicio;
    COMMIT;

    SELECT 'Servicio eliminado correctamente de todas las tablas relacionadas';
END //
DELIMITER ;

-- sp para insertar proformas
DELIMITER //
CREATE PROCEDURE sp_insert_proforma(
    IN p_fecha_emision DATE,
    IN p_costo_mano_obra DECIMAL(10,2),
    IN p_subtotal DECIMAL(10,2),
    IN p_estado_aprobacion VARCHAR(50),
    IN p_calle VARCHAR(100),
    IN p_manzana VARCHAR(50),
    IN p_ciudad VARCHAR(100),
    IN p_visita_fecha DATE,
    IN p_visita_hora TIME,
    IN p_visita_observacion TEXT,
    IN p_id_proyecto INT,
    IN p_id_cliente INT
)
BEGIN
    START TRANSACTION;

    INSERT INTO PROFORMA
    VALUES (
        0,p_fecha_emision, p_costo_mano_obra, p_subtotal, p_estado_aprobacion, 
        p_calle, p_manzana, p_ciudad, p_visita_fecha, p_visita_hora, 
        p_visita_observacion, p_id_proyecto, p_id_cliente
    );
    COMMIT;
    SELECT 'Proforma insertada correctamente';
END //
DELIMITER ;

-- sp para actualizar la proforma
DELIMITER //
CREATE PROCEDURE sp_update_proforma(
    IN p_id_proforma INT,
    IN p_fecha_emision DATE,
    IN p_costo_mano_obra DECIMAL(10,2),
    IN p_subtotal DECIMAL(10,2),
    IN p_estado_aprobacion VARCHAR(50),
    IN p_calle VARCHAR(100),
    IN p_manzana VARCHAR(50),
    IN p_ciudad VARCHAR(100),
    IN p_visita_fecha DATE,
    IN p_visita_hora TIME,
    IN p_visita_observacion TEXT
)
BEGIN
    START TRANSACTION;

    UPDATE PROFORMA 
    SET 
        fecha_emision = p_fecha_emision,
        costo_mano_obra = p_costo_mano_obra,
        subtotal = p_subtotal,
        estado_aprobacion = p_estado_aprobacion,
        calle = p_calle,
        manzana = p_manzana,
        ciudad = p_ciudad,
        visita_fecha = p_visita_fecha,
        visita_hora = p_visita_hora,
        visita_observacion = p_visita_observacion
    WHERE ID_proforma = p_id_proforma;
    COMMIT;
    SELECT 'Proforma actualizada correctamente';
END //
DELIMITER ;

-- sp para eliminar proformas 
DELIMITER //
CREATE PROCEDURE sp_delete_proforma(
    IN p_id_proforma INT
)
BEGIN
    START TRANSACTION;

    DELETE FROM PROFORMA WHERE ID_proforma = p_id_proforma;
    COMMIT;
    SELECT 'Proforma eliminada correctamente';
END //
DELIMITER ;

-- tabla Inventario
-- sp para insertar inventario
DELIMITER //
CREATE PROCEDURE sp_insert_inventario(
    IN p_nombre VARCHAR(100),
    IN p_marca VARCHAR(50),
    IN p_precio_unidad DECIMAL(10,2),
    IN p_stock INT
)
BEGIN
    START TRANSACTION;

    INSERT INTO INVENTARIO
    VALUES (0, p_stock, p_nombre, p_marca, p_precio_unidad);
    COMMIT;
    SELECT 'Inventario insertado correctamente';
END //
DELIMITER ;

-- sp para actualizar inventario
DELIMITER //
CREATE PROCEDURE sp_update_inventario(
    IN p_id_inventario INT,
    IN p_nombre VARCHAR(100),
    IN p_marca VARCHAR(50),
    IN p_precio_unidad DECIMAL(10,2),
    IN p_stock INT
)
BEGIN
    START TRANSACTION;

    UPDATE INVENTARIO 
    SET Stock = p_stock, nombre = p_nombre, marca = p_marca, precio_unidad = p_precio_unidad
    WHERE ID_Inventario = p_id_inventario;
    COMMIT;
    SELECT 'Inventario actualizado correctamente';
END //
DELIMITER ;

-- sp para eliminar inventario
DELIMITER //
CREATE PROCEDURE sp_delete_inventario(
    IN p_id_inventario INT
)
BEGIN
    START TRANSACTION;
    
    DELETE FROM INVENTARIO WHERE ID_Inventario = p_id_inventario;
    COMMIT;
    SELECT 'Inventario eliminado correctamente';
END //
DELIMITER ;

-- tabla material
DELIMITER //
CREATE PROCEDURE sp_insert_material(
    IN p_descripcion VARCHAR(100),
    IN p_marca VARCHAR(50),
    IN p_precio_unidad DECIMAL(10,2)
)
BEGIN
    DECLARE id_inventario INT;

    SELECT i.ID_Inventario INTO id_inventario
    FROM INVENTARIO i
    WHERE i.nombre = p_descripcion AND i.marca = p_marca;

    IF id_inventario IS NULL THEN
        SIGNAL SQLSTATE '45000'
        SET MESSAGE_TEXT = 'No se encontró el inventario especificado';
    ELSE
        START TRANSACTION;

        INSERT INTO MATERIAL
        VALUES (0, p_descripcion, p_marca, p_precio_unidad, id_inventario);
        COMMIT;
        SELECT 'Material insertado correctamente';
    END IF;
END //
DELIMITER ;

-- sp para actualizar material
DELIMITER //
CREATE PROCEDURE sp_update_material(
    IN p_id_material INT,
    IN p_descripcion VARCHAR(100),
    IN p_marca VARCHAR(50),
    IN p_precio_unidad DECIMAL(10,2)
)
BEGIN
    START TRANSACTION;

    UPDATE MATERIAL 
    SET descripcion = p_descripcion, marca = p_marca, precio_unidad = p_precio_unidad
    WHERE ID_Material = p_id_material;
    COMMIT;
    SELECT 'Material actualizado correctamente';
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE sp_delete_material(
    IN p_id_material INT
)
BEGIN
    START TRANSACTION;

    DELETE FROM MATERIAL WHERE ID_Material = p_id_material;
    COMMIT;
    SELECT 'Material eliminado correctamente';
END //
DELIMITER ;

-- Añadir por lo menos 5 usuarios y especificar por lo menos 2 permisos por usuario
CREATE USER 'usuario1'@'localhost' IDENTIFIED BY 'p@ssw0rd1';
CREATE USER 'usuario2'@'localhost' IDENTIFIED BY 'P@s$w0rd2';
CREATE USER 'usuario3'@'localhost' IDENTIFIED BY 'p@$sw0rD3';
CREATE USER 'usuario4'@'localhost' IDENTIFIED BY 'p@ssW0Rd4';
CREATE USER 'usuario5'@'localhost' IDENTIFIED BY 'pa$sw0rd5';

GRANT SELECT, INSERT ON refreezerdb.* TO 'usuario1'@'localhost';
GRANT SELECT, UPDATE ON refreezerdb.* TO 'usuario2'@'localhost';
GRANT SELECT, DELETE ON refreezerdb.* TO 'usuario3'@'localhost';
GRANT SELECT, INSERT ON refreezerdb.* TO 'usuario4'@'localhost';
GRANT SELECT, UPDATE ON refreezerdb.* TO 'usuario5'@'localhost';

-- Debe existir por lo menos 1 permiso 1 a un stored procedure
GRANT EXECUTE ON PROCEDURE refreezerdb.sp_insert_cliente TO 'usuario1'@'localhost';
-- Debe existir por lo menos 2 permisos a vistas
GRANT SELECT, UPDATE ON refreezerdb.clientes_empresa TO 'usuario2'@'localhost';
GRANT SELECT ON refreezerdb.clientes_empresa TO 'usuario5'@'localhost';
GRANT SELECT, UPDATE ON refreezerdb.servicios_por_empleado to 'usuario5'@'localhost';
GRANT SELECT ON refreezerdb.servicios_por_empleado to 'usuario2'@'localhost';
