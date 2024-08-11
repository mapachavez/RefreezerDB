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
                conexion.start_transaction()
                
                nombre = input("\nIntroduzca el nombre: ")
                direccion = input("Introduzca la direccion: ")
                mail = input("Introduzca el correo: ")
                telf = input("Introduzca el telefono: ")
                
                query_c = "INSERT INTO CLIENTE (nombre, direccion, correo, telefono) VALUES (%s, %s, %s, %s)"
                val_c = (nombre, direccion, mail, telf)
                cursor.execute(query_c, val_c)
                
                id_cliente = cursor.lastrowid
                
                tipo = ""
                while tipo == "":
                    tipo = input("""\n\t\tTipo de cliente:
                                
                            1. Cliente natural
                            2. Cliente empresa
                            
                        Inserte tipo de cliente: """)
                    
                    if tipo == "1":
                        cedula = input("Ingrese el numero de cedula: ")
                        query_cn = "INSERT INTO CLIENTE_NATURAL (ID_cliente, Cedula) VALUES (%s, %s)"
                        val_cn = (id_cliente, cedula)
                        cursor.execute(query_cn,val_cn)
                    elif tipo == "2":
                        ruc = input("Ingrese el ruc de la empresa: ")
                        query_ce = "INSERT INTO CLIENTE_EMPRESA (ID_cliente, RUC) VALUES (%s, %s)"
                        val_ce = (id_cliente, ruc)
                        cursor.execute(query_ce,val_ce)
                    else:
                        input("Opcion no válida. Intente nuevamente...")
                        tipo = ""
                
                # Confirmar la transacción si ambas inserciones son exitosas
                conexion.commit()
                input("\nINFO: Cliente insertado correctamente...\n")
            
            except mysql.connector.Error as err:
                print(f"Error: {err} \n")
                # Deshacer la transacción si ocurre un error
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

                    except mysql.connector.Error as err:
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
                        
                    except mysql.connector.Error as err:
                        print(f"Error: {err}")
                elif ocon =="3":
                    input("Regresando al menú anterior...\n")
                else:
                    input("Opcion no válida. Intente nuevamente...")
                    ocon = ""
                    
            cursor.close()
        elif opc == "3":
            print("\n------\t Modificar datos de clientes \t------")
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
            
            # Selección de la tabla a modificar
            while True:
                print("\nSeleccione la tabla que desea modificar:")
                print("1. Tabla CLIENTE")
                print("2. Tabla CLIENTE_NATURAL o CLIENTE_EMPRESA")
                
                tabla_seleccionada = input("Ingrese el número correspondiente a la tabla: ")
                
                if tabla_seleccionada in ['1', '2']:
                    break
                else:
                    print("Selección inválida. Por favor, intente de nuevo.")
                    
            if tabla_seleccionada == '1':
                # Modificación en la tabla CLIENTE
                while True:
                    print("\nSeleccione el campo a modificar en la tabla CLIENTE:")
                    print("1. Nombre")
                    print("2. Dirección")
                    print("3. Correo")
                    print("4. Teléfono")
                    
                    campo_seleccionado = input("Ingrese el número correspondiente al campo: ")
                    
                    campos = {
                        '1': 'nombre',
                        '2': 'direccion',
                        '3': 'correo',
                        '4': 'telefono'
                    }
                    
                    campo = campos.get(campo_seleccionado)
                    
                    if campo:
                        nuevo_valor = input(f"Ingrese el nuevo valor para {campo}: ")
                        consulta = f"UPDATE CLIENTE SET {campo} = %s WHERE ID_cliente = %s"
                        cursor.execute(consulta, (nuevo_valor, id_cliente))
                        print(f"\nRegistro en la tabla CLIENTE con ID {id_cliente} actualizado correctamente.")
                        break
                    else:
                        print("Selección de campo inválida. Por favor, intente de nuevo.")
            
            elif tabla_seleccionada == '2':
                # Modificación en la tabla CLIENTE_NATURAL o CLIENTE_EMPRESA
                if tipo_cliente == '1':
                    while True:
                        print("\nSeleccione el campo a modificar en la tabla CLIENTE_NATURAL:")
                        print("1. Cédula")
                        
                        seleccion = input("Ingrese el número correspondiente al campo: ")
                        
                        if seleccion == '1':
                            campo = 'Cedula'
                            tabla = 'CLIENTE_NATURAL'
                            break
                        else:
                            print("Selección de campo inválida. Por favor, intente de nuevo.")
                
                elif tipo_cliente == '2':
                    while True:
                        print("\nSeleccione el campo a modificar en la tabla CLIENTE_EMPRESA:")
                        print("1. RUC")
                        
                        seleccion = input("Ingrese el número correspondiente al campo: ")
                        
                        if seleccion == '1':
                            campo = 'RUC'
                            tabla = 'CLIENTE_EMPRESA'
                            break
                        else:
                            print("Selección de campo inválida. Por favor, intente de nuevo.")

                nuevo_valor = input(f"Ingrese el nuevo valor para {campo}: ")
                consulta = f"UPDATE {tabla} SET {campo} = %s WHERE ID_cliente = %s"
                cursor.execute(consulta, (nuevo_valor, id_cliente))
                print(f"\nRegistro en la tabla {tabla} con ID {id_cliente} actualizado correctamente.")
            #Aplicar los cambios
            conexion.commit()
            cursor.close()
            input("Aplicando cambios... \nPulse enter para continuar...")
        elif opc == "4":
            print("\n------\t Eliminar datos de clientes \t------")
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

            # Determinar la tabla específica según el tipo de cliente
            if tipo_cliente == '1':
                tabla_especifica = "CLIENTE_NATURAL"
            elif tipo_cliente == '2':
                tabla_especifica = "CLIENTE_EMPRESA"

            try:
                # Eliminar primero de la tabla específica
                consulta_especifica = f"DELETE FROM {tabla_especifica} WHERE ID_cliente = %s"
                cursor.execute(consulta_especifica, (id_cliente,))
                
                # Luego eliminar de la tabla CLIENTE
                consulta_cliente = "DELETE FROM CLIENTE WHERE ID_cliente = %s"
                cursor.execute(consulta_cliente, (id_cliente,))
                
                print(f"Cliente con ID {id_cliente} eliminado correctamente de las tablas CLIENTE y {tabla_especifica}.")

            except mysql.connector.Error as err:
                print(f"Error: {err}")
                
            #Aplicar los cambios
            conexion.commit()
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
                estado_aprobacion = input("Ingrese el estado de aprobación (Aprobado/No Aprobado) [Enter para 'No Aprobado']: ")
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

            query = """
            INSERT INTO proforma (fecha_emision, costo_mano_obra, subtotal, estado_aprobacion, calle, manzana, ciudad, visita_fecha, visita_hora, visita_observacion, ID_Cliente, ID_Proyecto)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (fecha_emision, costo_mano_obra, subtotal, estado_aprobacion, calle, manzana, ciudad, visita_fecha, visita_hora, visita_observacion, id_cliente, id_proyecto if id_proyecto else None))
            conexion.commit()
            input("Proforma añadida exitosamente.")

        elif opcion == '2':
            # Consultar proformas (mostrar todas)
            query = "SELECT * FROM proforma"
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
                    id_cliente = row[11]
                    id_proyecto = row[12] if row[12] else 'N/A'

                    print(f"ID: {id_proforma} | Fecha Emisión: {fecha_emision} | Costo Mano de Obra: {costo_mano_obra} | Subtotal: {subtotal} | "
                          f"Estado Aprobación: {estado_aprobacion} | Dirección: {calle}, {manzana}, {ciudad} | "
                          f"Fecha Visita: {visita_fecha} | Hora Visita: {visita_hora} | Observaciones: {visita_observacion} | "
                          f"ID Cliente: {id_cliente} | ID Proyecto: {id_proyecto}\n")
                input("Consulta realizada correctamente...")
            else:
                print("No se encontraron proformas.")
            

        elif opcion == '3':
            # Editar proforma
            id_proforma = input("Ingrese el ID de la proforma que desea editar: ")
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
            print("11. ID Cliente")
            print("12. ID Proyecto")
            campo = input("Opción: ")

            if campo == '1':
                nuevo_valor = input("Ingrese la nueva fecha de emisión (YYYY-MM-DD): ")
                query = "UPDATE proforma SET fecha_emision = %s WHERE ID_Proforma = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese el nuevo costo de mano de obra: ")
                query = "UPDATE proforma SET costo_mano_obra = %s WHERE ID_Proforma = %s"
            elif campo == '3':
                nuevo_valor = input("Ingrese el nuevo subtotal: ")
                query = "UPDATE proforma SET subtotal = %s WHERE ID_Proforma = %s"
            elif campo == '4':
                while True:
                    nuevo_valor = input("Ingrese el nuevo estado de aprobación (Aprobado/No Aprobado) [Enter para 'No Aprobado']: ")
                    if nuevo_valor == "":
                        nuevo_valor = "No Aprobado"
                    if nuevo_valor in ["Aprobado", "No Aprobado"]:
                        break
                    print("Entrada no válida. Intente nuevamente.")
                query = "UPDATE proforma SET estado_aprobacion = %s WHERE ID_Proforma = %s"
            elif campo == '5':
                nuevo_valor = input("Ingrese la nueva calle: ")
                query = "UPDATE proforma SET calle = %s WHERE ID_Proforma = %s"
            elif campo == '6':
                nuevo_valor = input("Ingrese la nueva manzana: ")
                query = "UPDATE proforma SET manzana = %s WHERE ID_Proforma = %s"
            elif campo == '7':
                nuevo_valor = input("Ingrese la nueva ciudad: ")
                query = "UPDATE proforma SET ciudad = %s WHERE ID_Proforma = %s"
            elif campo == '8':
                nuevo_valor = input("Ingrese la nueva fecha de visita (YYYY-MM-DD): ")
                query = "UPDATE proforma SET visita_fecha = %s WHERE ID_Proforma = %s"
            elif campo == '9':
                nuevo_valor = input("Ingrese la nueva hora de visita (HH:MM:SS): ")
                query = "UPDATE proforma SET visita_hora = %s WHERE ID_Proforma = %s"
            elif campo == '10':
                nuevo_valor = input("Ingrese las nuevas observaciones de la visita: ")
                query = "UPDATE proforma SET visita_observacion = %s WHERE ID_Proforma = %s"
            elif campo == '11':
                nuevo_valor = input("Ingrese el nuevo ID del cliente: ")
                query = "UPDATE proforma SET ID_Cliente = %s WHERE ID_Proforma = %s"
            elif campo == '12':
                nuevo_valor = input("Ingrese el nuevo ID del proyecto (puede dejarlo vacío): ")
                query = "UPDATE proforma SET ID_Proyecto = %s WHERE ID_Proforma = %s"
            else:
                print("Opción no válida.")
                continue

            cursor.execute(query, (nuevo_valor, id_proforma))
            conexion.commit()
            input("Proforma actualizada exitosamente...")

        elif opcion == '4':
            # Eliminar proforma
            id_proforma = input("Ingrese el ID de la proforma que desea eliminar: ")
            query = "DELETE FROM proforma WHERE ID_Proforma = %s"
            cursor.execute(query, (id_proforma,))
            conexion.commit()
            input("Proforma eliminada exitosamente...")

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
            INSERT INTO certificado (descripcion, fecha_vigencia, nombre, ID_Empleado)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (descripcion, fecha_vigencia, nombre, id_empleado))
            conexion.commit()
            print("Certificado añadido exitosamente.")

        elif opcion == '2':
            # Consultar certificados
            query = "SELECT * FROM certificado"
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
            query = "UPDATE certificado SET descripcion = %s WHERE ID_Certificado = %s"
            cursor.execute(query, (nueva_descripcion, id_certificado))
            conexion.commit()
            print("Certificado actualizado exitosamente.")

        elif opcion == '4':
            # Eliminar certificado
            id_certificado = input("Ingrese el ID del certificado que desea eliminar: ")
            query = "DELETE FROM certificado WHERE ID_Certificado = %s"
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
            SELECT ID_cliente FROM CLIENTE_EMPRESA WHERE ID_cliente = %s
            """
            cursor.execute(query_check_cliente_empresa, (id_cliente,))
            resultado = cursor.fetchone()

            if resultado and resultado[0] == id_cliente:
                # Si el cliente es una empresa, se solicitan los datos del proyecto
                nombre = input("Ingrese el nombre del proyecto: ")
                fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
                fecha_fin = input("Ingrese la fecha de finalización (YYYY-MM-DD): ")

                query = """
                INSERT INTO proyecto (nombre, fecha_inicio, fecha_fin, ID_cliente)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query, (nombre, fecha_inicio, fecha_fin, id_cliente))
                conexion.commit()
                input("Proyecto añadido exitosamente.")
            else:
                input("Error: El ID del cliente no corresponde a una empresa. No se puede crear el proyecto.")
        
        elif opcion == '2':
            # Mostrar los proyectos
            query = "SELECT * FROM proyecto"
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
                query = "UPDATE proyecto SET nombre = %s WHERE ID_Proyecto = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese la nueva fecha de inicio (YYYY-MM-DD): ")
                query = "UPDATE proyecto SET fecha_inicio = %s WHERE ID_Proyecto = %s"
            elif campo == '3':
                nuevo_valor = input("Ingrese la nueva fecha de fin (YYYY-MM-DD): ")
                query = "UPDATE proyecto SET fecha_fin = %s WHERE ID_Proyecto = %s"
            else:
                print("Opción incorrecta...")
                continue

            cursor.execute(query, (nuevo_valor, id_proyecto))
            conexion.commit()
            input("Proyecto actualizado exitosamente...")
        
        elif opcion == '4':
            # Eliminar el proyecto 
            id_proyecto = input("Ingrese el ID del proyecto que desea eliminar: ")
            query = "DELETE FROM proyecto WHERE ID_Proyecto = %s"
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
            costo_servicio = input("Ingrese el costo del servicio: ")

            while True:
                estado = input("Ingrese el estado del servicio (En progreso/Terminado) [Enter para dejarlo 'En progreso']: ")
                if estado == "":
                    estado = "En progreso"
                if estado in ["En progreso", "Terminado"]:
                    break
                print("Entrada no válida. Intente nuevamente.")

            garantia = input("Ingrese la garantía (en meses): ")
            fecha_inicio = input("Ingrese la fecha de inicio (YYYY-MM-DD): ")
            fecha_fin = input("Ingrese la fecha de fin (YYYY-MM-DD): ")
            id_cliente = input("Ingrese el ID del cliente: ")

            query = """
            INSERT INTO SERVICIO (descripcion, costo_servicio, estado, garantia, Fecha_inicio, Fecha_fin, ID_cliente)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            cursor.execute(query, (descripcion, costo_servicio, estado, garantia, fecha_inicio, fecha_fin, id_cliente))
            conexion.commit()

            id_servicio = cursor.lastrowid

            print("\nSeleccione el tipo de servicio que desea añadir:")
            print("1. Diseño y Fabricación")
            print("2. Mantenimiento")
            print("3. Instalación y Montaje")
            print("4. Servicio Técnico")
            tipo_servicio = input("Opción: ")

            if tipo_servicio == '1':
                tipo_diseno = input("Ingrese el tipo de diseño: ")
                query_tipo = """
                INSERT INTO diseño_y_fabricacion (ID_Servicio, tipo_diseno)
                VALUES (%s, %s)
                """
                cursor.execute(query_tipo, (id_servicio, tipo_diseno))

            elif tipo_servicio == '2':
                tipo_mantenimiento = input("Ingrese el tipo de mantenimiento: ")
                name_unidad_maquinaria = input("Ingrese el nombre de la unidad/maquinaria: ")
                query_tipo = """
                INSERT INTO mantenimiento (ID_Servicio, Tipo_Mantenimiento, Name_Unidad_Maquinaria)
                VALUES (%s, %s, %s)
                """
                cursor.execute(query_tipo, (id_servicio, tipo_mantenimiento, name_unidad_maquinaria))

            elif tipo_servicio == '3':
                tipo_instalacion = input("Ingrese el tipo de instalación: ")
                query_tipo = """
                INSERT INTO instalacion_y_montaje (ID_Servicio, tipo_instalacion)
                VALUES (%s, %s)
                """
                cursor.execute(query_tipo, (id_servicio, tipo_instalacion))

            elif tipo_servicio == '4':
                tipo_servicio_tecnico = input("Ingrese el tipo de servicio técnico: ")
                query_tipo = """
                INSERT INTO servicio_tecnico (ID_Servicio, tipo_servicio)
                VALUES (%s, %s)
                """
                cursor.execute(query_tipo, (id_servicio, tipo_servicio_tecnico))

            else:
                print("Opción no válida. Servicio no registrado en una tabla específica.")
                continue

            conexion.commit()
            input("Servicio añadido exitosamente.")

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

            print("\nSeleccione el tipo de servicio que desea editar:")
            print("1. Diseño y Fabricación")
            print("2. Mantenimiento")
            print("3. Instalación y Montaje")
            print("4. Servicio Técnico")
            tipo_servicio = input("Ingrese el numero de la opcion: ")

            if tipo_servicio == '1':
                nuevo_tipo_diseno = input("Ingrese el nuevo tipo de diseño: ")
                query_tipo = "UPDATE diseño_y_fabricacion SET tipo_diseno = %s WHERE ID_Servicio = %s"
                cursor.execute(query_tipo, (nuevo_tipo_diseno, id_servicio))

            elif tipo_servicio == '2':
                nuevo_tipo_mantenimiento = input("Ingrese el nuevo tipo de mantenimiento: ")
                nuevo_name_unidad_maquinaria = input("Ingrese el nuevo nombre de la unidad/maquinaria: ")
                query_tipo = """
                UPDATE mantenimiento 
                SET Tipo_Mantenimiento = %s, Name_Unidad_Maquinaria = %s 
                WHERE ID_Servicio = %s
                """
                cursor.execute(query_tipo, (nuevo_tipo_mantenimiento, nuevo_name_unidad_maquinaria, id_servicio))

            elif tipo_servicio == '3':
                nuevo_tipo_instalacion = input("Ingrese el nuevo tipo de instalación: ")
                query_tipo = "UPDATE instalacion_y_montaje SET tipo_instalacion = %s WHERE ID_Servicio = %s"
                cursor.execute(query_tipo, (nuevo_tipo_instalacion, id_servicio))

            elif tipo_servicio == '4':
                nuevo_tipo_servicio_tecnico = input("Ingrese el nuevo tipo de servicio técnico: ")
                query_tipo = "UPDATE servicio_tecnico SET tipo_servicio = %s WHERE ID_Servicio = %s"
                cursor.execute(query_tipo, (nuevo_tipo_servicio_tecnico, id_servicio))

            else:
                print("Opción no válida.")
                continue

            print("Seleccione el campo que desea editar:")
            print("1. Descripción")
            print("2. Costo del Servicio")
            print("3. Estado")
            print("4. Garantía")
            print("5. Fecha de Inicio")
            print("6. Fecha de Fin")
            print("7. ID Cliente")
            campo = input("Opción: ")

            if campo == '1':
                nuevo_valor = input("Ingrese la nueva descripción: ")
                query = "UPDATE servicio SET descripcion = %s WHERE ID_Servicio = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese el nuevo costo del servicio: ")
                query = "UPDATE servicio SET costo_servicio = %s WHERE ID_Servicio = %s"
            elif campo == '3':
                while True:
                    nuevo_valor = input("Ingrese el nuevo estado del servicio (En progreso/Terminado) [Enter para dejarlo 'En progreso']: ")
                    if nuevo_valor == "":
                        nuevo_valor = "En progreso"
                    if nuevo_valor in ["En progreso", "Terminado"]:
                        break
                    print("Entrada no válida. Intente nuevamente.")
                query = "UPDATE servicio SET estado = %s WHERE ID_Servicio = %s"
            elif campo == '4':
                nuevo_valor = input("Ingrese la nueva garantía (en meses): ")
                query = "UPDATE servicio SET garantia = %s WHERE ID_Servicio = %s"
            elif campo == '5':
                nuevo_valor = input("Ingrese la nueva fecha de inicio (YYYY-MM-DD): ")
                query = "UPDATE servicio SET Fecha_inicio = %s WHERE ID_Servicio = %s"
            elif campo == '6':
                nuevo_valor = input("Ingrese la nueva fecha de fin (YYYY-MM-DD): ")
                query = "UPDATE servicio SET Fecha_fin = %s WHERE ID_Servicio = %s"
            elif campo == '7':
                nuevo_valor = input("Ingrese el nuevo ID del cliente: ")
                query = "UPDATE servicio SET ID_cliente = %s WHERE ID_Servicio = %s"
            else:
                print("Opción no válida.")
                continue

            cursor.execute(query, (nuevo_valor, id_servicio))
            conexion.commit()
            input("Servicio actualizado exitosamente...")

        elif opcion == '4':
            # Eliminar servicio
            id_servicio = input("Ingrese el ID del servicio que desea eliminar: ")
            #eliminacion por tablas de servicio especificas
            tablas_servicios = ["diseño_y_fabricacion", "mantenimiento", "instalacion_y_montaje", "servicio_tecnico"]
            for tabla in tablas_servicios:
                query = f"DELETE FROM {tabla} WHERE ID_Servicio = %s"
                cursor.execute(query, (id_servicio,))
            #eliminacion de la tabla servicio general
            query = "DELETE FROM servicio WHERE ID_Servicio = %s"
            cursor.execute(query, (id_servicio,))
            conexion.commit()
            input("Servicio eliminado exitosamente de todas las tablas correspondientes...")

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
            INSERT INTO empleado (nombre, cargo, correo)
            VALUES (%s, %s, %s)
            """
            cursor.execute(query, (nombre, cargo, correo))
            conexion.commit()
            input("Empleado añadido exitosamente.")

        elif opcion == '2':
            # Consultar empleados (mostrar todos)
            query = "SELECT * FROM empleado"
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
                query = "UPDATE empleado SET nombre = %s WHERE ID_Empleado = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese el nuevo cargo del empleado: ")
                query = "UPDATE empleado SET cargo = %s WHERE ID_Empleado = %s"
            elif campo == '3':
                nuevo_valor = input("Ingrese el nuevo correo del empleado: ")
                query = "UPDATE empleado SET correo = %s WHERE ID_Empleado = %s"
            else:
                print("Opción no válida.")
                continue

            cursor.execute(query, (nuevo_valor, id_empleado))
            conexion.commit()
            input("Empleado actualizado exitosamente...")

        elif opcion == '4':
            # Eliminar empleado
            id_empleado = input("Ingrese el ID del empleado que desea eliminar: ")
            query = "DELETE FROM empleado WHERE ID_Empleado = %s"
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

            # Verificar si el material ya existe en la tabla inventario
            query_check_material = "SELECT ID_Inventario, marca, precio_unidad FROM inventario WHERE nombre = %s"
            cursor.execute(query_check_material, (nombre_material,))
            material_existente = cursor.fetchone()

            if material_existente:
                # Si el material existe, se asignan los datos automáticamente
                id_inventario = material_existente[0]
                marca = material_existente[1]
                precio_unidad = material_existente[2]

                # Sumar +1 al stock en la tabla inventario
                query_update_stock = "UPDATE inventario SET Stock = Stock + 1 WHERE ID_Inventario = %s"
                cursor.execute(query_update_stock, (id_inventario,))
                conexion.commit()

                # Insertar el material en la tabla material
                query_insert_material = """
                INSERT INTO material (descripcion, marca, precio_unidad, ID_Inventario)
                VALUES (%s, %s, %s, %s)
                """
                descripcion = input("Ingrese la descripción del material: ")
                cursor.execute(query_insert_material, (descripcion, marca, precio_unidad, id_inventario))
                conexion.commit()
                input("Material añadido exitosamente con datos existentes en el inventario.")
            else:
                # Si el material no existe, se piden los datos y se crean los registros
                descripcion = input("Ingrese la descripción del material: ")
                marca = input("Ingrese la marca del material: ")
                precio_unidad = input("Ingrese el precio por unidad del material: ")
                
                # Crear un nuevo registro en inventario
                query_insert_inventario = """
                INSERT INTO inventario (Stock, nombre, marca, precio_unidad)
                VALUES (1, %s, %s, %s)
                """
                cursor.execute(query_insert_inventario, (nombre_material, marca, precio_unidad))
                conexion.commit()
                
                # Obtener el ID_Inventario recién creado
                id_inventario = cursor.lastrowid

                # Insertar el material en la tabla material
                query_insert_material = """
                INSERT INTO material (descripcion, marca, precio_unidad, ID_Inventario)
                VALUES (%s, %s, %s, %s)
                """
                cursor.execute(query_insert_material, (descripcion, marca, precio_unidad, id_inventario))
                conexion.commit()
                input("Material añadido exitosamente como nuevo inventario.")

        elif opcion == '2':
            # Mostrar los materiales
            query = "SELECT * FROM material"
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
            print("Seleccione el campo que desea editar:")
            print("1. Descripción")
            print("2. Marca")
            print("3. Precio por Unidad")
            print("4. cantidad de material")
            campo = input("Opción: ")

            if campo == '1':
                nuevo_valor = input("Ingrese la nueva descripción: ")
                query = "UPDATE material SET descripcion = %s WHERE ID_Material = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese la nueva marca: ")
                query = "UPDATE material SET marca = %s WHERE ID_Material = %s"
            elif campo == '3':
                nuevo_valor = float(input("Ingrese el nuevo precio por unidad: "))
                query = "UPDATE material SET precio_unidad = %s WHERE ID_Material = %s"
            elif campo == '4':
                print("Seleccione la operación que desea realizar:")
                print("1. Añadir cantidad")
                print("2. Quitar cantidad")
                operacion = input("Opción: ")

                if operacion == '1':
                    cantidad = int(input("Ingrese la cantidad a añadir: "))

                    # Actualizar el stock en la tabla inventario
                    query_update_stock = """
                    UPDATE inventario 
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
                    FROM inventario 
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
                        UPDATE inventario 
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
                print("Opción incorrecta...")
                continue

            cursor.execute(query, (nuevo_valor, id_material))
            conexion.commit()
            input("Material actualizado exitosamente...")

        elif opcion == '4':
            # Eliminar material
            id_material = input("Ingrese el ID del material que desea eliminar: ")
            # Verificar si existen registros dependientes en servicio_material
            query_check_dependents = "SELECT COUNT(*) FROM servicio_material WHERE ID_Material = %s"
            cursor.execute(query_check_dependents, (id_material,))
            dependientes = cursor.fetchone()[0]

            if dependientes > 0:
                    input("No se puede eliminar el material porque hay registros dependientes en servicio_material.")
            else:
                    # Obtener el ID_Inventario antes de eliminar el material
                    cursor.execute("SELECT ID_Inventario FROM material WHERE ID_Material = %s", (id_material,))
                    id_inventario = cursor.fetchone()[0]

                    # Eliminar el material
                    query_delete_material = "DELETE FROM material WHERE ID_Material = %s"
                    cursor.execute(query_delete_material, (id_material,))
                    conexion.commit()
                    input("Material eliminado exitosamente.")

                    # Restar 1 al Stock del inventario asociado
                    query_update_stock = "UPDATE inventario SET Stock = Stock - 1 WHERE ID_Inventario = %s"
                    cursor.execute(query_update_stock, (id_inventario,))
                    conexion.commit()
                    input("Stock actualizado.")

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
            stock = input("Ingrese el stock del inventario: ")
            nombre = input("Ingrese el nombre del inventario: ")
            marca = input("Ingrese la marca del inventario: ")
            precio_unidad = input("Ingrese el precio por unidad: ")

            query = """
            INSERT INTO inventario (Stock, nombre, marca, precio_unidad)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (stock, nombre, marca, precio_unidad))
            conexion.commit()
            input("Inventario añadido exitosamente.")
        
        elif opcion == '2':
            # Consultar inventarios
            query = "SELECT * FROM inventario"
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
            # Editar inventario
            id_inventario = input("Ingrese el ID del inventario que desea editar: ")
            print("Seleccione el campo que desea editar:")
            print("1. Stock")
            print("2. Nombre")
            print("3. Marca")
            print("4. Precio por unidad")
            campo = input("Opción: ")

            if campo == '1':
                nuevo_valor = input("Ingrese el nuevo stock: ")
                query = "UPDATE inventario SET Stock = %s WHERE ID_Inventario = %s"
            elif campo == '2':
                nuevo_valor = input("Ingrese el nuevo nombre: ")
                query = "UPDATE inventario SET nombre = %s WHERE ID_Inventario = %s"
            elif campo == '3':
                nuevo_valor = input("Ingrese la nueva marca: ")
                query = "UPDATE inventario SET marca = %s WHERE ID_Inventario = %s"
            elif campo == '4':
                nuevo_valor = input("Ingrese el nuevo precio por unidad: ")
                query = "UPDATE inventario SET precio_unidad = %s WHERE ID_Inventario = %s"
            else:
                print("Opción incorrecta...")
                continue

            cursor.execute(query, (nuevo_valor, id_inventario))
            conexion.commit()
            input("Inventario actualizado exitosamente...")
        
        elif opcion == '4':
            # Eliminar inventario
            id_inventario = input("Ingrese el ID del inventario que desea eliminar: ")
            query = "DELETE FROM inventario WHERE ID_Inventario = %s"
            cursor.execute(query, (id_inventario,))
            conexion.commit()
            input("El inventario se ha eliminado exitosamente...")

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
            INSERT INTO proveedor (nombre, correo, telefono, disponibilidad)
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (nombre, correo, telefono, disponibilidad))
            conexion.commit()
            print("Proveedor añadido exitosamente.")

        elif opcion == '2':
            # Consultar proveedores
            query = "SELECT * FROM proveedor"
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

            query = f"UPDATE proveedor SET {campo} = %s WHERE ID_Proveedor = %s"
            cursor.execute(query, (nuevo_valor, id_proveedor))
            conexion.commit()
            print("Proveedor actualizado exitosamente.")

        elif opcion == '4':
            # Eliminar proveedor
            id_proveedor = input("Ingrese el ID del proveedor a eliminar: ")
            query = "DELETE FROM proveedor WHERE ID_Proveedor = %s"
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
