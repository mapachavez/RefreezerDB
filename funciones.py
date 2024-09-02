from datetime import datetime


def gestionClientes(conexion):
    opc = ""
    while (opc != "5"):
        cursor = conexion.cursor()
        print("\n1. Insertar datos")
        print("2. Consultar datos")
        print("3. Modificar datos")
        print("4. Eliminar datos")
        print("5. Regresar")
        
        opc = input("\nIntroduce el número de opción: ")
        
        if opc == "1":
            print("\n------\t Insertar nuevos clientes \t------")
            try:
                nombre = input("\nIntroduzca el nombre: ")
                direccion = input("Introduzca la direccion: ")
                mail = input("Introduzca el correo: ")
                telf = input("Introduzca el telefono: ")

                tipo = ""
                while tipo == "":
                    tipo = input("""\n\t\tTipo de cliente:
                            1. Cliente natural
                            2. Cliente empresa
                            Inserte tipo de cliente: """)

                if tipo == "1":
                    cedula = input("Ingrese el numero de cedula: ")
                    cursor.callproc('sp_insert_cliente', (nombre, direccion, mail, telf, 'N', cedula))
                elif tipo == "2":
                    ruc = input("Ingrese el ruc de la empresa: ")
                    cursor.callproc('sp_insert_cliente', (nombre, direccion, mail, telf, 'E', ruc))
                else:
                    input("Opcion no válida. Intente nuevamente...")

                conexion.commit()
                input("\nINFO: Cliente insertado correctamente...\n")

            except mysql.connector.Error as err: # type: ignore
                print(f"Error: {err} \n")
                conexion.rollback()

            finally:
                cursor.close()

        elif opc == "2":
            ocon = ""
            while ocon != "3":
                print("\n------\t Consulta de clientes \t------")
                print("1. Clientes naturales")
                print("2. Clientes empresa")
                print("3. Regresar")
                ocon = input("\nIngrese una opcion: ")
                
                if ocon == "1":
                    print("\n---------- \t\t Consulta de clientes naturales \t\t----------\n")
                    query_ccn = "SELECT * FROM CLIENTE c JOIN CLIENTE_NATURAL USING(ID_cliente)"
                    
                    try:
                        cursor.execute(query_ccn)
                        rescn = cursor.fetchall()

                        for fila in rescn:
                            print(f"ID: {fila[0]}| Nombre: {fila[1]}| Direccion: {fila[2]}| Correo: {fila[3]}| Teléfono: {fila[4]}| Cédula: {fila[5]}\n")
                        
                        input("\nConsulta exitosa! \nPresione enter para continuar...")

                    except mysql.connector.Error as err: # type: ignore
                        print(f"Error: {err}")
                elif ocon == "2":
                    print("\n---------- \t\t Consulta de clientes empresa \t\t----------\n")
                    query_cce = "SELECT * FROM CLIENTE c JOIN CLIENTE_EMPRESA USING(ID_cliente)"
                    
                    try:
                        cursor.execute(query_cce)
                        resce = cursor.fetchall()

                        for fila in resce:
                            print(f"ID: {fila[0]}| Nombre: {fila[1]}| Direccion: {fila[2]}| Correo: {fila[3]}| Teléfono: {fila[4]}| RUC: {fila[5]}\n")

                        input("\nConsulta exitosa! \nPresione enter para continuar...")
                        
                    except mysql.connector.Error as err: # type: ignore
                        print(f"Error: {err}")
                elif ocon =="3":
                    input("Regresando al menú anterior...\n")
                else:
                    input("Opcion no válida. Intente nuevamente...")
                    ocon = ""
                    
            cursor.close()

        elif opc == "3":
            print("\n------\t Modificar datos de clientes \t------")

            # Selección del tipo de cliente
            while True:
                print("\nSeleccione el tipo de cliente:")
                print("1. Cliente Natural")
                print("2. Cliente Empresa")
                tipo_cliente = input("\nIngrese el número correspondiente al tipo de cliente: ")
                if tipo_cliente in ['1', '2']:
                    break
                else:
                    print("Selección inválida. Por favor, intente de nuevo.")

            id_cliente = input("Ingrese el ID del cliente: ")

            # Recuperar los valores actuales del cliente
            if tipo_cliente == '1':
                cursor.execute(
                    "SELECT c.nombre, c.direccion, c.correo, c.telefono, cn.Cedula "
                    "FROM CLIENTE c JOIN CLIENTE_NATURAL cn ON c.ID_cliente = cn.ID_cliente "
                    "WHERE c.ID_cliente = %s", (id_cliente,))
            else:
                cursor.execute(
                    "SELECT c.nombre, c.direccion, c.correo, c.telefono, ce.RUC "
                    "FROM CLIENTE c JOIN CLIENTE_EMPRESA ce ON c.ID_cliente = ce.ID_cliente "
                    "WHERE c.ID_cliente = %s", (id_cliente,))

            cliente = cursor.fetchone()

            if cliente is None:
                print("Cliente no encontrado.")
                continue

            (nombre, direccion, correo, telefono, identificacion) = cliente

            print("Valores actuales:")
            print(f"Nombre: {nombre}")
            print(f"Dirección: {direccion}")
            print(f"Correo: {correo}")
            print(f"Teléfono: {telefono}")
            if tipo_cliente == '1':
                print(f"Cédula: {identificacion}")
            else:
                print(f"RUC: {identificacion}")

            print("Seleccione el campo que desea editar:")
            print("1. Nombre")
            print("2. Dirección")
            print("3. Correo")
            print("4. Teléfono")
            if tipo_cliente == '1':
                print("5. Cédula")
            else:
                print("5. RUC")
            
            campo = input("Opción: ")

            nuevo_nombre = nombre
            nuevo_direccion = direccion
            nuevo_correo = correo
            nuevo_telefono = telefono
            nuevo_identificacion = identificacion

            if campo == '1':
                nuevo_nombre = input("Ingrese el nuevo nombre: ")
            elif campo == '2':
                nuevo_direccion = input("Ingrese la nueva dirección: ")
            elif campo == '3':
                nuevo_correo = input("Ingrese el nuevo correo: ")
            elif campo == '4':
                nuevo_telefono = input("Ingrese el nuevo teléfono: ")
            elif campo == '5':
                nuevo_identificacion = input("Ingrese el nuevo valor (Cédula/RUC): ")
            else:
                print("Opción no válida.")
                continue

            # Llamar al procedimiento almacenado para actualizar
            if tipo_cliente == '1':
                cursor.callproc('sp_update_cliente', (id_cliente, nuevo_nombre, nuevo_direccion, nuevo_correo, nuevo_telefono, nuevo_identificacion, None))
            else:
                cursor.callproc('sp_update_cliente', (id_cliente, nuevo_nombre, nuevo_direccion, nuevo_correo, nuevo_telefono, None, nuevo_identificacion))

            conexion.commit()
            input("Cliente actualizado exitosamente...")
            cursor.close()
            input("Aplicando cambios... \nPulse enter para continuar...")

        elif opc == "4":
            print("\n------\t Eliminar datos de clientes \t------")
            id_cliente = input("Ingrese el ID del cliente: ")

            try:
                cursor.callproc('sp_delete_cliente', (id_cliente,))
                conexion.commit()
                input(f"Cliente con ID {id_cliente} eliminado correctamente.")
            except mysql.connector.Error as err: # type: ignore
                print(f"Error: {err}")
                conexion.rollback()

            cursor.close()
            input("Aplicando cambios... \nPulse enter para continuar...")

        elif opc == "5":
            cursor.close()
            input("\nRegresando al menú principal... \nPresione enter para continuar...")
        else:
            input("\nOpcion no válida. Intente nuevamente...")
            opc = ""
            cursor.close()

def gestionProformas(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Proformas ---")
        print("1. Añadir nueva proforma")
        print("2. Consultar proformas")
        print("3. Editar proforma")
        print("4. Eliminar proforma")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir nueva proforma
            fecha_emision = input("Ingrese la fecha de emisión (YYYY-MM-DD): ")
            costo_mano_obra = input("Ingrese el costo de mano de obra: ")
            subtotal = input("Ingrese el subtotal: ")

            while True:
                estado_aprobacion = input(
                    "Ingrese el estado de aprobación (Aprobado/No Aprobado) [Enter para 'No Aprobado']: ")
                if estado_aprobacion == "":
                    estado_aprobacion = "No Aprobado"
                if estado_aprobacion in ["Aprobado", "No Aprobado"]:
                    break
                print("Entrada no válida. Intente nuevamente.")

            calle = input("Ingrese la calle: ")
            manzana = input("Ingrese la manzana: ")
            ciudad = input("Ingrese la ciudad: ")
            visita_fecha = input("Ingrese la fecha de visita (YYYY-MM-DD): ")
            visita_hora = input("Ingrese la hora de visita (HH:MM:SS): ")
            visita_observacion = input("Ingrese observaciones de la visita (puede dejarlo vacío): ")
            id_cliente = input("Ingrese el ID del cliente: ")
            id_proyecto = input("Ingrese el ID del proyecto (opcional): ")

            cursor.callproc('sp_insert_proforma', (fecha_emision, costo_mano_obra, subtotal, estado_aprobacion,
                                                   calle, manzana, ciudad, visita_fecha, visita_hora,
                                                   visita_observacion, id_proyecto or None, id_cliente))

            for result in cursor.stored_results():
                print(result.fetchone()[0])

            conexion.commit()

        elif opcion == '2':
            # Consultar proformas (mostrar todas)
            query = "SELECT * FROM PROFORMA"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Proformas Creadas ---")
                for row in resultados:
                    id_proforma = row[0]
                    fecha_emision = row[1].strftime("%Y-%m-%d")
                    costo_mano_obra = row[2]
                    subtotal = row[3]
                    estado_aprobacion = row[4]
                    calle = row[5]
                    manzana = row[6]
                    ciudad = row[7]
                    visita_fecha = row[8].strftime("%Y-%m-%d")
                    visita_hora = str(row[9])  # Convertir TIME a string
                    visita_observacion = row[10] if row[10] else 'N/A'
                    id_proyecto = row[11] if row[11] else 'N/A'
                    id_cliente = row[12]

                    print(f"ID: {id_proforma} | Fecha Emisión: {fecha_emision} | Costo Mano de Obra: {costo_mano_obra} | Subtotal: {subtotal} | "
                          f"Estado Aprobación: {estado_aprobacion} | Dirección: {calle}, {manzana}, {ciudad} | "
                          f"Fecha Visita: {visita_fecha} | Hora Visita: {visita_hora} | Observaciones: {visita_observacion} | "
                          f"ID Proyecto: {id_proyecto} | ID Cliente: {id_cliente}\n")
                input("Consulta realizada correctamente...")
            else:
                print("No se encontraron proformas.")

        elif opcion == '3':
            id_proforma = input("Ingrese el ID de la proforma que desea editar: ")

            cursor.execute(
                "SELECT fecha_emision, costo_mano_obra, subtotal, estado_aprobacion, calle, manzana, ciudad, visita_fecha, visita_hora, visita_observacion FROM PROFORMA WHERE ID_Proforma = %s",
                (id_proforma,))
            proforma = cursor.fetchone()

            if proforma is None:
                print("Proforma no encontrada.")
                continue

            (fecha_emision, costo_mano_obra, subtotal, estado_aprobacion, calle, manzana, ciudad, visita_fecha,
             visita_hora, visita_observacion) = proforma

            print("Valores actuales:")
            print(f"Fecha de Emisión: {fecha_emision}")
            print(f"Costo Mano de Obra: {costo_mano_obra}")
            print(f"Subtotal: {subtotal}")
            print(f"Estado de Aprobación: {estado_aprobacion}")
            print(f"Calle: {calle}")
            print(f"Manzana: {manzana}")
            print(f"Ciudad: {ciudad}")
            print(f"Fecha de Visita: {visita_fecha}")
            print(f"Hora de Visita: {visita_hora}")
            print(f"Observaciones de la Visita: {visita_observacion}")

            print("Seleccione el campo que desea editar:")
            print("1. Fecha de Emisión")
            print("2. Costo Mano de Obra")
            print("3. Subtotal")
            print("4. Estado de Aprobación")
            print("5. Calle")
            print("6. Manzana")
            print("7. Ciudad")
            print("8. Fecha de Visita")
            print("9. Hora de Visita")
            print("10. Observaciones de la Visita")
            campo = input("Opción: ")

            nuevo_fecha_emision = fecha_emision
            nuevo_costo_mano_obra = costo_mano_obra
            nuevo_subtotal = subtotal
            nuevo_estado_aprobacion = estado_aprobacion
            nuevo_calle = calle
            nuevo_manzana = manzana
            nuevo_ciudad = ciudad
            nuevo_visita_fecha = visita_fecha
            nuevo_visita_hora = visita_hora
            nuevo_visita_observacion = visita_observacion

            if campo == '1':
                nuevo_valor = input("Ingrese la nueva fecha de emisión (YYYY-MM-DD): ")
                nuevo_fecha_emision = datetime.strptime(nuevo_valor, '%Y-%m-%d').date()
            elif campo == '2':
                nuevo_valor = input("Ingrese el nuevo costo de mano de obra: ")
                nuevo_costo_mano_obra = float(nuevo_valor)
            elif campo == '3':
                nuevo_valor = input("Ingrese el nuevo subtotal: ")
                nuevo_subtotal = float(nuevo_valor)
            elif campo == '4':
                while True:
                    nuevo_valor = input(
                        "Ingrese el nuevo estado de aprobación (Aprobado/No Aprobado) [Enter para 'No Aprobado']: ")
                    if nuevo_valor == "":
                        nuevo_estado_aprobacion = "No Aprobado"
                    if nuevo_valor in ["Aprobado", "No Aprobado"]:
                        nuevo_estado_aprobacion = nuevo_valor
                        break
                    print("Entrada no válida. Intente nuevamente.")
            elif campo == '5':
                nuevo_valor = input("Ingrese la nueva calle: ")
                nuevo_calle = nuevo_valor
            elif campo == '6':
                nuevo_valor = input("Ingrese la nueva manzana: ")
                nuevo_manzana = nuevo_valor
            elif campo == '7':
                nuevo_valor = input("Ingrese la nueva ciudad: ")
                nuevo_ciudad = nuevo_valor
            elif campo == '8':
                nuevo_valor = input("Ingrese la nueva fecha de visita (YYYY-MM-DD): ")
                nuevo_visita_fecha = datetime.strptime(nuevo_valor, '%Y-%m-%d').date()
            elif campo == '9':
                nuevo_valor = input("Ingrese la nueva hora de visita (HH:MM:SS): ")
                nuevo_visita_hora = datetime.strptime(nuevo_valor, '%H:%M:%S').time()
            elif campo == '10':
                nuevo_valor = input("Ingrese las nuevas observaciones de la visita: ")
                nuevo_visita_observacion = nuevo_valor
            else:
                print("Opción no válida.")
                continue

            cursor.callproc('sp_update_proforma', [
                id_proforma,
                nuevo_fecha_emision,
                nuevo_costo_mano_obra,
                nuevo_subtotal,
                nuevo_estado_aprobacion,
                nuevo_calle,
                nuevo_manzana,
                nuevo_ciudad,
                nuevo_visita_fecha,
                nuevo_visita_hora,
                nuevo_visita_observacion
            ])
            conexion.commit()
            input("Proforma actualizada exitosamente...")
        elif opcion == '4':

            id_proforma = input("Ingrese el ID de la proforma que desea eliminar: ")
            cursor.callproc('sp_delete_proforma', (id_proforma,))

            for result in cursor.stored_results():
                print(result.fetchone()[0])

            conexion.commit()
            input("Proforma eliminada exitosamente.")

        elif opcion == '5':
            # Salir
            input("Saliendo del sistema de gestión de proformas...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

    cursor.close()

def gestionCertificado(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Certificados ---")
        print("1. Añadir nuevo Certificado")
        print("2. Consultar Certificados")
        print("3. Editar Certificado")
        print("4. Eliminar Certificado")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir nuevo certificado
            descripcion = input("Ingrese la descripción del certificado: ")
            fecha_vigencia = input("Ingrese la fecha de vigencia (YYYY-MM-DD): ")
            nombre = input("Ingrese el nombre del certificado: ")
            id_empleado = input("Ingrese el ID del empleado: ")

            query = """
            INSERT INTO CERTIFICADO (descripcion, fecha_vigencia, nombre, ID_Empleado)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (descripcion, fecha_vigencia, nombre, id_empleado))
            conexion.commit()
            print("Certificado añadido exitosamente.")

        elif opcion == '2':
            # Consultar certificados
            query = "SELECT * FROM CERTIFICADO"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Certificados ---")
                for fila in resultados:
                    id_certificado = fila[0]
                    descripcion = fila[1]
                    fecha_vigencia = fila[2]
                    nombre = fila[3]
                    id_empleado = fila[4]
                    print(f"ID: {id_certificado} | Descripción: {descripcion} | Fecha de Vigencia: {fecha_vigencia} | Nombre: {nombre} | ID Empleado: {id_empleado}")
            else:
                print("No se encontraron certificados.")

        elif opcion == '3':
            # Editar certificado
            id_certificado = input("Ingrese el ID del certificado que desea editar: ")
            nueva_descripcion = input("Ingrese la nueva descripción: ")
            query = "UPDATE CERTIFICADO SET descripcion = %s WHERE ID_Certificado = %s"
            cursor.execute(query, (nueva_descripcion, id_certificado))
            conexion.commit()
            print("Certificado actualizado exitosamente.")

        elif opcion == '4':
            # Eliminar certificado
            id_certificado = input("Ingrese el ID del certificado que desea eliminar: ")
            query = "DELETE FROM CERTIFICADO WHERE ID_Certificado = %s"
            cursor.execute(query, (id_certificado,))
            conexion.commit()
            print("Certificado eliminado exitosamente.")

        elif opcion == '5':
            # Salir
            print("Saliendo del sistema de gestión de certificados...")
            break
        else:
            print("Opción inválida...")

    cursor.close()

def gestionproyecto(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Proyectos ---")
        print("1. Añadir nuevo Proyecto")
        print("2. Consultar proyectos")
        print("3. Editar proyecto")
        print("4. Eliminar proyecto")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir un nuevo proyecto
            id_cliente = input("Ingrese el ID del cliente: ")
            # Verificar si el ID_cliente corresponde a un cliente empresa
            query_check_cliente_empresa = """
            SELECT ID_Cliente FROM CLIENTE_EMPRESA WHERE ID_Cliente = %s
            """
            cursor.execute(query_check_cliente_empresa, (id_cliente,))
            resultado = cursor.fetchone()

            if resultado and str(resultado[0]) == id_cliente:
                # Si el cliente es una empresa, se solicitan los datos del proyecto
                nombre = input("Ingrese el nombre del proyecto: ")
                fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
                fecha_fin = input("Ingrese la fecha de finalización (YYYY-MM-DD): ")

                query = """
                INSERT INTO PROYECTO (nombre, fecha_inicio, fecha_fin)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query, (nombre, fecha_inicio, fecha_fin))
                conexion.commit()
                input("Proyecto añadido exitosamente.")
            else:
                input("Error: El ID del cliente no corresponde a una empresa. No se puede crear el proyecto.")

        elif opcion == '2':
            # Mostrar los proyectos
            query = "SELECT * FROM PROYECTO"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Proyectos Creados ---")
                for fila in resultados:
                    id_proyecto = fila[0]
                    nombre = fila[1]
                    fecha_inicio = fila[2].strftime("%Y-%m-%d")
                    fecha_fin = fila[3].strftime("%Y-%m-%d")
                    
                    print(f"ID: {id_proyecto} | Nombre: {nombre} "
                          f"Fecha de Inicio: {fecha_inicio} | Fecha de Fin: {fecha_fin}\n")
                input("Consulta realizada correctamente...")
            else:
                print("No se encontraron proyectos.")
        
        elif opcion == '3':
            id_proyecto = input("Ingrese el ID del proyecto que desea editar: ")
            print("Seleccione el campo que desea editar:")
            print("1. Nombre del Proyecto")
            print("2. Fecha de Inicio")
            print("3. Fecha de Fin")
            campo = input("Opción: ")

            if campo == '1':
                nuevo_valor = input("Ingrese el nuevo nombre del proyecto: ")
                query = "UPDATE PROYECTO SET nombre = %s WHERE ID_Proyecto = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese la nueva fecha de inicio (YYYY-MM-DD): ")
                query = "UPDATE PROYECTO SET fecha_inicio = %s WHERE ID_Proyecto = %s"
            elif campo == '3':
                nuevo_valor = input("Ingrese la nueva fecha de fin (YYYY-MM-DD): ")
                query = "UPDATE PROYECTO SET fecha_fin = %s WHERE ID_Proyecto = %s"
            else:
                print("Opción incorrecta...")
                continue

            cursor.execute(query, (nuevo_valor, id_proyecto))
            conexion.commit()
            input("Proyecto actualizado exitosamente...")
        
        elif opcion == '4':
            # Eliminar el proyecto 
            id_proyecto = input("Ingrese el ID del proyecto que desea eliminar: ")
            query = "DELETE FROM PROYECTO WHERE ID_Proyecto = %s"
            cursor.execute(query, (id_proyecto,))
            conexion.commit()
            input("El proyecto se ha eliminado exitosamente...")
        
        elif opcion == '5':
            # Salir
            input("Saliendo del sistema de gestión de proyectos...")
            break
        else: 
            print("Opción inválida...")
    
    cursor.close()

#ponle 10 centavos de fe mijo
def gestionServicios(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Servicios ---")
        print("1. Añadir nuevo Servicio")
        print("2. Consultar Servicios")
        print("3. Editar Servicio")
        print("4. Eliminar Servicio")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir nuevo servicio
            descripcion = input("Ingrese la descripción del servicio: ")
            costo_servicio = float(input("Ingrese el costo del servicio: "))

            while True:
                estado = input("Ingrese el estado del servicio (En progreso/Terminado) [Enter para dejarlo 'En progreso']: ")
                if estado == "":
                    estado = "En progreso"
                if estado in ["En progreso", "Terminado"]:
                    break
                print("Entrada no válida. Intente nuevamente.")

            garantia = int(input("Ingrese la garantía (en meses): "))
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
            id_cliente = int(input("Ingrese el ID del cliente: "))
            id_proforma = int(input("Ingrese el ID de la proforma: "))  # Agregado para el procedimiento

            # Llamar al procedimiento almacenado para insertar servicio
            cursor.callproc('sp_insert_servicio', (descripcion, costo_servicio, estado, garantia, fecha_inicio, fecha_fin, id_cliente, id_proforma))

            cursor.execute("SELECT @id_servicio := LAST_INSERT_ID();")
            result = cursor.fetchone()  # fetchone() para obtener la primera fila

            cursor.execute("SELECT LAST_INSERT_ID();")
            result = cursor.fetchone()
            id_servicio = result[0] if result else None

            if id_servicio:
                print("Servicio insertado correctamente con ID:", id_servicio)
            else:
                print("Error al insertar el servicio o no se generó el ID.")
                continue

            print("\nSeleccione el tipo de servicio que desea añadir:")
            print("1. Diseño y Fabricación")
            print("2. Mantenimiento")
            print("3. Instalación y Montaje")
            print("4. Servicio Técnico")
            tipo_servicio = input("Opción: ")

            if tipo_servicio == '1':
                tipo_diseno = input("Ingrese el tipo de diseño: ")
                cursor.callproc('sp_insert_diseno_y_fabricacion', (id_servicio, tipo_diseno))
            elif tipo_servicio == '2':
                tipo_mantenimiento = input("Ingrese el tipo de mantenimiento: ")
                name_unidad_maquinaria = input("Ingrese el nombre de la unidad/maquinaria: ")
                cursor.callproc('sp_insert_mantenimiento', (id_servicio, tipo_mantenimiento, name_unidad_maquinaria))
            elif tipo_servicio == '3':
                tipo_instalacion = input("Ingrese el tipo de instalación: ")
                cursor.callproc('sp_insert_instalacion_y_montaje', (id_servicio, tipo_instalacion))
            elif tipo_servicio == '4':
                tipo_servicio_tecnico = input("Ingrese el tipo de servicio técnico: ")
                cursor.callproc('sp_insert_servicio_tecnico', (id_servicio, tipo_servicio_tecnico))
            else:
                print("Opción no válida. Servicio no registrado en una tabla específica.")
                continue

            conexion.commit()

        elif opcion == '2':
            # Consultar servicios en general de la tabla servicio
            query = "SELECT * FROM SERVICIO"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Servicios ---")
                for fila in resultados:
                    id_servicio = fila[0]
                    descripcion = fila[1]
                    costo_servicio = fila[2]
                    estado = fila[3]
                    garantia = fila[4]
                    fecha_inicio = fila[5].strftime("%Y-%m-%d")
                    fecha_fin = fila[6].strftime("%Y-%m-%d")
                    id_cliente = fila[7]

                    print(f"ID: {id_servicio} | Descripción: {descripcion} | Costo: {costo_servicio} | "
                          f"Estado: {estado} | Garantía: {garantia} meses | "
                          f"Fecha de Inicio: {fecha_inicio} | Fecha de Fin: {fecha_fin} | ID Cliente: {id_cliente}\n")
                input("Consulta realizada correctamente...")
            else:
                print("No se encontraron servicios.")

        elif opcion == '3':
            # modificar servicio
            id_servicio = input("Ingrese el ID del servicio que desea editar: ")

            # Obtener los valores actuales del servicio
            cursor.execute("SELECT descripcion, costo_servicio, estado, garantia, Fecha_inicio, Fecha_fin, ID_cliente FROM SERVICIO WHERE ID_Servicio = %s", (id_servicio,))
            servicio_actual = cursor.fetchone()

            if servicio_actual:
                descripcion_actual, costo_servicio_actual, estado_actual, garantia_actual, fecha_inicio_actual, fecha_fin_actual, id_cliente_actual = servicio_actual

                print("Valores actuales:")
                print(f"Descripción: {descripcion_actual}")
                print(f"Costo del Servicio: {costo_servicio_actual:.2f}")
                print(f"Estado: {estado_actual}")
                print(f"Garantía: {garantia_actual} meses")
                print(f"Fecha de Inicio: {fecha_inicio_actual}")
                print(f"Fecha de Fin: {fecha_fin_actual}")
                print(f"ID Cliente: {id_cliente_actual}")

                print("\nSeleccione el tipo de servicio que desea editar:")
                print("1. Diseño y Fabricación")
                print("2. Mantenimiento")
                print("3. Instalación y Montaje")
                print("4. Servicio Técnico")
                tipo_servicio = input("Ingrese el número de la opción: ")

                if tipo_servicio == '1':

                    cursor.execute("SELECT tipo_diseno FROM DISEÑO_Y_FABRICACION WHERE ID_Servicio = %s", (id_servicio,))
                    (tipo_diseno_actual,) = cursor.fetchone()
                    
                    print("Valores actuales:")
                    print(f"Tipo de diseño: {tipo_diseno_actual}")

                    nuevo_tipo_diseno = input(f"Ingrese el nuevo tipo de diseño [Enter para mantener '{tipo_diseno_actual}']: ")
                    if not nuevo_tipo_diseno:
                        nuevo_tipo_diseno = tipo_diseno_actual

                    cursor.callproc('sp_update_diseno_y_fabricacion', (id_servicio, nuevo_tipo_diseno))
                    conexion.commit()

                    for result in cursor.stored_results():
                        print(result.fetchone()[0])

                elif tipo_servicio == '2':

                    cursor.execute("SELECT tipo_mantenimiento, name_unidad_maquinaria FROM MANTENIMIENTO WHERE ID_Servicio = %s", (id_servicio,))
                    (tipo_mantenimiento_actual, name_unidad_maquinaria_actual) = cursor.fetchone()

                    print("Valores actuales:")
                    print(f"Tipo de mantenimiento: {tipo_mantenimiento_actual}")
                    print(f"Nombre de la unidad/maquinaria: {name_unidad_maquinaria_actual}")

                    nuevo_tipo_mantenimiento = input(f"Ingrese el nuevo tipo de mantenimiento [Enter para mantener '{tipo_mantenimiento_actual}']: ")
                    if not nuevo_tipo_mantenimiento:
                        nuevo_tipo_mantenimiento = tipo_mantenimiento_actual  

                    nuevo_name_unidad_maquinaria = input(f"Ingrese el nuevo nombre de la unidad/maquinaria [Enter para mantener '{name_unidad_maquinaria_actual}']: ")
                    if not nuevo_name_unidad_maquinaria:
                        nuevo_name_unidad_maquinaria = name_unidad_maquinaria_actual  

                    cursor.callproc('sp_update_mantenimiento', (id_servicio, nuevo_tipo_mantenimiento, nuevo_name_unidad_maquinaria))
                    conexion.commit()

                    for result in cursor.stored_results():
                        print(result.fetchone()[0])

                elif tipo_servicio == '3':
                    
                    cursor.execute("SELECT tipo_instalacion FROM INSTALACION_Y_MONTAJE WHERE ID_Servicio = %s", (id_servicio,))
                    (tipo_instalacion_actual,) = cursor.fetchone()

                    print("Valores actuales:")
                    print(f"Tipo de instalación: {tipo_instalacion_actual}")

                    nuevo_tipo_instalacion = input(f"Ingrese el nuevo tipo de instalación [Enter para mantener '{tipo_instalacion_actual}']: ")
                    if not nuevo_tipo_instalacion:
                        nuevo_tipo_instalacion = tipo_instalacion_actual 

                    cursor.callproc('sp_update_instalacion_y_montaje', (id_servicio, nuevo_tipo_instalacion))
                    conexion.commit()

                    for result in cursor.stored_results():
                        print(result.fetchone()[0])

                elif tipo_servicio == '4':
                    
                    cursor.execute("SELECT tipo_servicio_tecnico FROM SERVICIO_TECNICO WHERE ID_Servicio = %s", (id_servicio,))
                    (tipo_servicio_tecnico_actual,) = cursor.fetchone()

                    print("Valores actuales:")
                    print(f"Tipo de servicio técnico: {tipo_servicio_tecnico_actual}")

                    nuevo_tipo_servicio_tecnico = input(f"Ingrese el nuevo tipo de servicio técnico [Enter para mantener '{tipo_servicio_tecnico_actual}']: ")
                    if not nuevo_tipo_servicio_tecnico:
                        nuevo_tipo_servicio_tecnico = tipo_servicio_tecnico_actual

                    cursor.callproc('sp_update_servicio_tecnico', (id_servicio, nuevo_tipo_servicio_tecnico))
                    conexion.commit()

                    for result in cursor.stored_results():
                        print(result.fetchone()[0])

                else:
                    print("Opción no válida.")

                print("Seleccione el campo que desea editar:")
                print("1. Descripción")
                print("2. Costo del Servicio")
                print("3. Estado")
                print("4. Garantía")
                print("5. Fecha de Inicio")
                print("6. Fecha de Fin")
                print("7. ID Cliente")
                campo = input("Opción: ")

                nuevo_valor_descripcion = descripcion_actual
                nuevo_valor_costo = costo_servicio_actual
                nuevo_valor_estado = estado_actual
                nuevo_valor_garantia = garantia_actual
                nuevo_valor_fecha_inicio = fecha_inicio_actual
                nuevo_valor_fecha_fin = fecha_fin_actual
                nuevo_valor_id_cliente = id_cliente_actual

                if campo == '1':
                    nuevo_valor_descripcion = input("Ingrese la nueva descripción: ")
                elif campo == '2':
                    nuevo_valor_costo = input("Ingrese el nuevo costo del servicio: ")
                    nuevo_valor_costo = float(nuevo_valor_costo)
                elif campo == '3':
                    while True:
                        nuevo_valor_estado = input("Ingrese el nuevo estado del servicio (En progreso/Terminado) [Enter para dejarlo 'En progreso']: ")
                        if nuevo_valor_estado == "":
                            nuevo_valor_estado = "En progreso"
                        if nuevo_valor_estado in ["En progreso", "Terminado"]:
                            break
                        print("Entrada no válida. Intente nuevamente.")
                elif campo == '4':
                    nuevo_valor_garantia = input("Ingrese la nueva garantía (en meses): ")
                    nuevo_valor_garantia = int(nuevo_valor_garantia)
                elif campo == '5':
                    nuevo_valor_fecha_inicio = input("Ingrese la nueva fecha de inicio (YYYY-MM-DD): ")
                elif campo == '6':
                    nuevo_valor_fecha_fin = input("Ingrese la nueva fecha de fin (YYYY-MM-DD): ")
                elif campo == '7':
                    nuevo_valor_id_cliente = input("Ingrese el nuevo ID del cliente: ")
                    nuevo_valor_id_cliente = int(nuevo_valor_id_cliente)
                else:
                    print("Opción no válida.")
                    continue

                # Llamar al procedimiento almacenado para actualizar el servicio
                cursor.callproc('sp_update_servicio', (
                    id_servicio,
                    nuevo_valor_descripcion,
                    nuevo_valor_costo,
                    nuevo_valor_estado,
                    nuevo_valor_garantia,
                    nuevo_valor_fecha_inicio,
                    nuevo_valor_fecha_fin
                ))
                conexion.commit()
                for result in cursor.stored_results():
                    print(result.fetchone()[0])
                input("Servicio actualizado exitosamente...")
            else:
                print("Servicio no encontrado.")
                
        elif opcion == '4':
            # Eliminar servicio
            id_servicio = input("Ingrese el ID del servicio que desea eliminar: ")
            cursor.callproc('sp_delete_servicio', (id_servicio,))
            conexion.commit()

        elif opcion == '5':
            # Salir
            input("Saliendo del sistema de gestión de servicios...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

    cursor.close()

def gestionempleados(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Empleados ---")
        print("1. Añadir nuevo empleado")
        print("2. Consultar empleados")
        print("3. Editar empleado")
        print("4. Eliminar empleado")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir nuevo empleado
            nombre = input("Ingrese el nombre del empleado: ")
            cargo = input("Ingrese el cargo del empleado: ")
            correo = input("Ingrese el correo del empleado: ")

            query = """
            INSERT INTO EMPLEADO (nombre, cargo, correo)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nombre, cargo, correo))
            conexion.commit()
            input("Empleado añadido exitosamente.")

        elif opcion == '2':
            # Consultar empleados (mostrar todos)
            query = "SELECT * FROM EMPLEADO"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Empleados Registrados ---")
                for row in resultados:
                    id_empleado = row[0]
                    nombre = row[1]
                    cargo = row[2]
                    correo = row[3]

                    print(f"ID: {id_empleado} | Nombre: {nombre} | Cargo: {cargo} | Correo: {correo}\n")
                input("Consulta realizada correctamente...")
            else:
                print("No se encontraron empleados.")

        elif opcion == '3':
            # Editar empleado
            id_empleado = input("Ingrese el ID del empleado que desea editar: ")
            print("Seleccione el campo que desea editar:")
            print("1. Nombre")
            print("2. Cargo")
            print("3. Correo")
            campo = input("Opción: ")

            if campo == '1':
                nuevo_valor = input("Ingrese el nuevo nombre del empleado: ")
                query = "UPDATE EMPLEADO SET nombre = %s WHERE ID_Empleado = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese el nuevo cargo del empleado: ")
                query = "UPDATE EMPLEADO SET cargo = %s WHERE ID_Empleado = %s"
            elif campo == '3':
                nuevo_valor = input("Ingrese el nuevo correo del empleado: ")
                query = "UPDATE EMPLEADO SET correo = %s WHERE ID_Empleado = %s"
            else:
                print("Opción no válida.")
                continue

            cursor.execute(query, (nuevo_valor, id_empleado))
            conexion.commit()
            input("Empleado actualizado exitosamente...")

        elif opcion == '4':
            # Eliminar empleado
            id_empleado = input("Ingrese el ID del empleado que desea eliminar: ")
            query = "DELETE FROM EMPLEADO WHERE ID_Empleado = %s"
            cursor.execute(query, (id_empleado,))
            conexion.commit()
            input("Empleado eliminado exitosamente...")

        elif opcion == '5':
            # Salir
            input("Saliendo del sistema de gestión de empleados...")
            break

        else:
            print("Opción no válida. Intente de nuevo.")

    cursor.close()

def gestionMateriales(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Materiales ---")
        print("1. Añadir nuevo Material")
        print("2. Consultar Materiales")
        print("3. Editar Material")
        print("4. Eliminar Material")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir un nuevo material
            nombre_material = input("Ingrese el nombre del material: ")
            cursor.execute("SELECT ID_Inventario, marca, precio_unidad FROM INVENTARIO WHERE nombre = %s", (nombre_material,))
            material_existente = cursor.fetchone()

            if material_existente:
                id_inventario = material_existente[0]
                marca = material_existente[1]
                precio_unidad = material_existente[2]
                descripcion = input("Ingrese la descripción del material: ")

                # Llamar al procedimiento almacenado para insertar material
                cursor.callproc('sp_insert_material', (descripcion, marca, precio_unidad, id_inventario))
                conexion.commit()
                for result in cursor.stored_results():
                    print(result.fetchone()[0])
            else:
                for result in cursor.stored_results():
                    print(result.fetchone()[0])

        elif opcion == '2':
            # Mostrar los materiales
            query = "SELECT * FROM MATERIAL"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Materiales ---")
                for fila in resultados:
                    id_material = fila[0]
                    descripcion = fila[1]
                    marca = fila[2]
                    precio_unidad = fila[3]
                    id_inventario = fila[4]

                    print(f"ID: {id_material} | Descripción: {descripcion} | Marca: {marca} "
                          f"| Precio por Unidad: {precio_unidad:.2f} | ID Inventario: {id_inventario}\n")
                input("Consulta realizada correctamente...")
            else:
                print("No se encontraron materiales.")

        elif opcion == '3':
            id_material = input("Ingrese el ID del material que desea editar: ")

            cursor.execute(
                "SELECT descripcion, marca, precio_unidad FROM MATERIAL WHERE ID_Material = %s",
                (id_material,))
            material = cursor.fetchone()

            if material is None:
                print("Material no encontrado.")
                continue

            (descripcion_actual, marca_actual, precio_unidad_actual) = material

            print("Valores actuales:")
            print(f"Descripción: {descripcion_actual}")
            print(f"Marca: {marca_actual}")
            print(f"Precio por Unidad: {precio_unidad_actual:.2f}")

            print("Seleccione el campo que desea editar:")
            print("1. Descripción")
            print("2. Marca")
            print("3. Precio por Unidad")
            print("4. Cantidad de material")
            campo = input("Opción: ")

            nuevo_descripcion = descripcion_actual
            nuevo_marca = marca_actual
            nuevo_precio_unidad = precio_unidad_actual

            if campo == '1':
                nuevo_descripcion = input("Ingrese la nueva descripción: ")
            elif campo == '2':
                nuevo_marca = input("Ingrese la nueva marca: ")
            elif campo == '3':
                nuevo_precio_unidad = float(input("Ingrese el nuevo precio por unidad: "))
            elif campo == '4':
                print("Seleccione la operación que desea realizar:")
                print("1. Añadir cantidad")
                print("2. Quitar cantidad")
                operacion = input("Opción: ")

                if operacion == '1':
                    cantidad = int(input("Ingrese la cantidad a añadir: "))

                    # Actualizar el stock en la tabla inventario
                    query_update_stock = """
                    UPDATE INVENTARIO 
                    SET Stock = Stock + %s 
                    WHERE ID_Inventario = (
                        SELECT ID_Inventario 
                        FROM material 
                        WHERE ID_Material = %s
                    )
                    """
                    cursor.execute(query_update_stock, (cantidad, id_material))
                    conexion.commit()
                    input("Cantidad añadida exitosamente al inventario.")

                elif operacion == '2':
                    cantidad = int(input("Ingrese la cantidad a quitar: "))

                    # Verificar si hay suficiente stock antes de restar
                    query_check_stock = """
                    SELECT Stock 
                    FROM INVENTARIO 
                    WHERE ID_Inventario = (
                        SELECT ID_Inventario 
                        FROM material 
                        WHERE ID_Material = %s
                    )
                    """
                    cursor.execute(query_check_stock, (id_material,))
                    stock_actual = cursor.fetchone()[0]

                    if cantidad > stock_actual:
                        input("Error: La cantidad a quitar excede el stock disponible.")
                    else:
                        # Actualizar el stock en la tabla inventario
                        query_update_stock = """
                        UPDATE INVENTARIO 
                        SET Stock = Stock - %s 
                        WHERE ID_Inventario = (
                            SELECT ID_Inventario 
                            FROM material 
                            WHERE ID_Material = %s
                        )
                        """
                        cursor.execute(query_update_stock, (cantidad, id_material))
                        conexion.commit()
                        input("Cantidad quitada exitosamente del inventario.")

            else:
                print("Opción no válida.")
                continue

            # Llamar al procedimiento almacenado para actualizar material
            cursor.callproc('sp_update_material', [
                id_material,
                nuevo_descripcion,
                nuevo_marca,
                nuevo_precio_unidad
            ])
            conexion.commit()

            for result in cursor.stored_results():
                print(result.fetchone()[0])

        elif opcion == '4':
            # Eliminar material
            id_material = input("Ingrese el ID del material que desea eliminar: ")

            cursor.callproc('sp_delete_material', (id_material,))
            conexion.commit()
            
            for result in cursor.stored_results():
                print(result.fetchone()[0])

        elif opcion == '5':
            input("Saliendo del sistema de gestión de materiales...")
            break
        else:
            print("Opción inválida...")

    cursor.close()

def gestionInventario(conexion):
    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Inventario ---")
        print("1. Añadir nuevo Inventario")
        print("2. Consultar Inventarios")
        print("3. Editar Inventario")
        print("4. Eliminar Inventario")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir un nuevo inventario
            stock = int(input("Ingrese el stock del inventario: "))
            nombre = input("Ingrese el nombre del inventario: ")
            marca = input("Ingrese la marca del inventario: ")
            precio_unidad = float(input("Ingrese el precio por unidad: "))

            # Llamar al procedimiento almacenado para insertar inventario
            cursor.callproc('sp_insert_inventario', (nombre, marca, precio_unidad, stock))
            conexion.commit()
            for result in cursor.stored_results():
                print(result.fetchone()[0])
        
        elif opcion == '2':
            # Consultar inventarios
            query = "SELECT * FROM INVENTARIO"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Inventarios Registrados ---")
                for fila in resultados:
                    id_inventario = fila[0]
                    stock = fila[1]
                    nombre = fila[2]
                    marca = fila[3]
                    precio_unidad = fila[4]

                    print(f"ID: {id_inventario} | Stock: {stock} | Nombre: {nombre} "
                          f"Marca: {marca} | Precio Unidad: {precio_unidad}\n")
                input("Consulta realizada correctamente...")
            else:
                print("No se encontraron inventarios.")
        
        elif opcion == '3':

            id_inventario = input("Ingrese el ID del inventario que desea editar: ")

            # Obtener los valores actuales del inventario
            cursor.execute("SELECT nombre, marca, precio_unidad, stock FROM INVENTARIO WHERE ID_Inventario = %s", (id_inventario,))
            inventario_actual = cursor.fetchone()

            if inventario_actual:
                nombre_actual, marca_actual, precio_unidad_actual, stock_actual = inventario_actual

                print("Valores actuales:")
                print(f"Nombre: {nombre_actual}")
                print(f"Marca: {marca_actual}")
                print(f"Precio por Unidad: {precio_unidad_actual:.2f}")
                print(f"Stock: {stock_actual}")

                print("Seleccione el campo que desea editar:")
                print("1. Nombre")
                print("2. Marca")
                print("3. Precio por unidad")
                print("4. Stock")
                campo = input("Opción: ")

                nuevo_nombre = nombre_actual
                nueva_marca = marca_actual
                nuevo_precio_unidad = precio_unidad_actual
                nuevo_stock = stock_actual

                if campo == '1':
                    nuevo_nombre = input("Ingrese el nuevo nombre: ")
                elif campo == '2':
                    nueva_marca = input("Ingrese la nueva marca: ")
                elif campo == '3':
                    nuevo_precio_unidad = float(input("Ingrese el nuevo precio por unidad: "))
                elif campo == '4':
                    nuevo_stock = int(input("Ingrese el nuevo stock: "))
                else:
                    print("Opción incorrecta...")
                    continue

                # Llamar al procedimiento almacenado para actualizar inventario
                cursor.callproc('sp_update_inventario', (id_inventario, nuevo_nombre, nueva_marca, nuevo_precio_unidad, nuevo_stock))
                conexion.commit()
                for result in cursor.stored_results():
                    print(result.fetchone()[0])
            else:
                print("Inventario no encontrado.")
        
        elif opcion == '4':
            id_inventario = input("Ingrese el ID del inventario que desea eliminar: ")

            # Llamar al procedimiento almacenado para eliminar inventario
            cursor.callproc('sp_delete_inventario', (id_inventario,))
            conexion.commit()
            for result in cursor.stored_results():
                print(result.fetchone()[0])
                
        elif opcion == '5':
            # Salir
            input("Saliendo del sistema de gestión de inventarios...")
            break
        
        else:
            print("Opción inválida...")
    
    cursor.close()

def gestion_proveedor(conexion):
    """
    Función para gestionar las operaciones CRUD en la tabla 'proveedor'.

    Args:
        conexion: Conexión a la base de datos.
    """

    cursor = conexion.cursor()

    while True:
        print("\n--- Gestión de Proveedores ---")
        print("1. Añadir nuevo Proveedor")
        print("2. Consultar Proveedores")
        print("3. Editar Proveedor")
        print("4. Eliminar Proveedor")
        print("5. Salir")
        opcion = input("Seleccione una opción: ")

        if opcion == '1':
            # Añadir un nuevo proveedor
            nombre = input("Ingrese el nombre del proveedor: ")
            correo = input("Ingrese el correo electrónico: ")
            telefono = input("Ingrese el número de teléfono: ")
            disponibilidad = input("Ingrese la disponibilidad: ")

            query = """
            INSERT INTO PROVEEDOR (nombre, correo, telefono, disponibilidad)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, correo, telefono, disponibilidad))
            conexion.commit()
            print("Proveedor añadido exitosamente.")

        elif opcion == '2':
            # Consultar proveedores
            query = "SELECT * FROM PROVEEDOR"
            cursor.execute(query)
            resultados = cursor.fetchall()

            if resultados:
                print("\n--- Proveedores ---")
                for fila in resultados:
                    id_proveedor, nombre, correo, telefono, disponibilidad = fila
                    print(f"ID: {id_proveedor} | Nombre: {nombre} | Correo: {correo} | Teléfono: {telefono} | Disponibilidad: {disponibilidad}")
            else:
                print("No se encontraron proveedores.")

        elif opcion == '3':
            # Editar proveedor
            id_proveedor = input("Ingrese el ID del proveedor a editar: ")
            campo = input("Seleccione el campo a editar (nombre, correo, telefono, disponibilidad): ")
            nuevo_valor = input(f"Ingrese el nuevo valor para {campo}: ")

            query = f"UPDATE PROVEEDOR SET {campo} = %s WHERE ID_Proveedor = %s"
            cursor.execute(query, (nuevo_valor, id_proveedor))
            conexion.commit()
            print("Proveedor actualizado exitosamente.")

        elif opcion == '4':
            # Eliminar proveedor
            id_proveedor = input("Ingrese el ID del proveedor a eliminar: ")
            query = "DELETE FROM PROVEEDOR WHERE ID_Proveedor = %s"
            cursor.execute(query, (id_proveedor,))
            conexion.commit()
            print("Proveedor eliminado exitosamente.")

        elif opcion == '5':
            # Salir
            print("Saliendo del sistema de gestión de proveedores...")
            break
        else:
            print("Opción inválida.")

    cursor.close()
